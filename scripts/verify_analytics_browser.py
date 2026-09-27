"""Real Chromium acceptance; collection is fulfilled locally, never sent to GA.

Test tooling only: pip install playwright (CI pins the tested version).
Run: python scripts/verify_analytics_browser.py --output /tmp/consent-qa.json
DPN_CHROMIUM_EXECUTABLE can select an existing Chromium installation.
No contact submissions; local server serves only release allowlisted files.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sys
import threading
from urllib.parse import urlsplit, parse_qs
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'ops/deploy'))
import check_asset_versions as assets
PATHS = ['/', '/en/', '/softwareentwicklung-luebeck/', '/ki-automatisierung-luebeck/', '/website-showcase/', '/datenschutz/']
WIDTHS = [320, 360, 390, 430, 768, 1024, 1440, 1920]
KEY = 'dpn-analytics-consent'

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path.lstrip('/')
        if not path or path.endswith('/'): path += 'index.html'
        if path not in self.allowed and not (ROOT / path).is_dir():
            self.send_error(404); return
        super().do_GET()
    def end_headers(self):
        self.send_header('Content-Security-Policy', self.csp)
        super().end_headers()
    def log_message(self, *args): pass


def run(output):
    Handler.allowed = {p.relative_to(ROOT).as_posix() for p in assets.public_files(ROOT)}
    Handler.csp = (ROOT / 'ops/cloudflare/content-security-policy.txt').read_text().strip()
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    base = f'http://127.0.0.1:{server.server_port}'
    results = {'scope': 'local candidate; real Google script; intercepted collection', 'cases': [], 'responsive': [], 'requests': []}
    def check(value, label):
        if not value: raise AssertionError(label)
    with sync_playwright() as p:
        options = {'args': ['--no-sandbox']}
        if os.getenv('DPN_CHROMIUM_EXECUTABLE'): options['executable_path'] = os.environ['DPN_CHROMIUM_EXECUTABLE']
        b = p.chromium.launch(**options)
        def context(**kwargs):
            c = b.new_context(**kwargs)
            requests = []; errors = []; failures = []; intercepted_aborts = []
            def intercept(route):
                host = urlsplit(route.request.url).hostname or ''
                if host == 'api.github.com':
                    # Repeated viewport tests must not exhaust GitHub's public API.
                    route.fulfill(status=200, content_type='application/json', body='[]' if '/events/' in route.request.url else '{"public_repos": 0, "followers": 0}')
                elif host.endswith('google-analytics.com') or host.endswith('analytics.google.com'):
                    route.fulfill(status=200, body='')
                elif host == 'www.googletagmanager.com' and '/gtag/js' not in route.request.url:
                    route.fulfill(status=200, body='')
                elif '/api/contact' in route.request.url and route.request.method != 'GET':
                    raise AssertionError('Contact submission forbidden')
                else: route.continue_()
            c.route('**/*', intercept)
            c.on('request', lambda r: requests.append(r.url))
            def page_events(page):
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                def failed(r):
                    # Chromium may cancel mocked keepalive/beacon responses. These
                    # intercepted analytics requests never reach Google's servers.
                    if 'google-analytics.com/g/collect' in r.url and r.failure == 'net::ERR_ABORTED':
                        intercepted_aborts.append(r.url)
                    else: failures.append({'url':r.url,'failure':r.failure})
                page.on('requestfailed', failed)
                page.on('response', lambda r: failures.append({'url':r.url,'status':r.status}) if r.status >= 400 else None)
            c.on('page', page_events)
            return c, requests, errors, failures, intercepted_aborts
        def google(requests): return [u for u in requests if 'google-analytics.com' in u or 'googletagmanager.com' in u or 'analytics.google.com' in u]
        def ga_cookies(c): return [x['name'] for x in c.cookies() if x['name'].startswith('_ga')]
        def wait_collection(page, req):
            for _ in range(150):
                if any('google-analytics.com/g/collect' in u and parse_qs(urlsplit(u).query).get('tid')==['G-NHB0PGPYTW'] for u in req): return
                page.wait_for_timeout(100)
            raise AssertionError('No collection request within 15 seconds')
        def accept(page): page.locator('[data-analytics-decision="accepted"]').click()
        def reject(page): page.locator('[data-analytics-decision="denied"]').click()
        def settings(page): page.locator('.analytics-consent-settings').click()
        def counts(page):
            return page.evaluate("""() => ({scripts: [...document.scripts].filter(s=>s.src.includes('googletagmanager.com/gtag/js')).length, configs: (window.dataLayer||[]).filter(a=>a[0]==='config'&&a[1]==='G-NHB0PGPYTW').length})""")
        try:
            for path in PATHS:
                c, req, err, fail, intercepted_aborts = context()
                page = c.new_page(); page.goto(base+path); page.wait_for_timeout(1000)
                check(page.locator('#analytics-consent').is_visible(), path+' fresh UI')
                check(not google(req) and not ga_cookies(c), path+' no analytics before consent')
                check(page.locator('h1').is_visible(), path+' content available')
                # Keyboard decline, no preselected consent.
                page.locator('[data-analytics-decision="denied"]').focus(); page.keyboard.press('Enter')
                page.reload(); page.wait_for_timeout(500)
                check(not page.locator('#analytics-consent').is_visible(), path+' denied persisted')
                check(not google(req) and not ga_cookies(c), path+' denied no analytics')
                settings(page); accept(page)
                page.wait_for_function("window.dataLayer && window.dataLayer.some(a=>a[0]==='config')")
                wait_collection(page, req)
                page.wait_for_timeout(500)
                check(counts(page)=={'scripts':1,'configs':1}, path+' single initialization')
                check(any('google-analytics.com/g/collect' in u and parse_qs(urlsplit(u).query).get('tid')==['G-NHB0PGPYTW'] for u in req), path+' real collection attempt')
                check(bool(ga_cookies(c)), path+' real GA cookies after accept')
                # Reaccept and duplicate asset execution must not initialize twice.
                settings(page); accept(page)
                page.evaluate("""async () => {const s=document.createElement('script');s.src=[...document.scripts].find(s=>s.src.includes('/analytics-consent.js')).src;document.head.append(s);await new Promise(r=>s.onload=r);} """)
                check(counts(page)=={'scripts':1,'configs':1}, path+' duplicate guard')
                req.clear(); page.reload(); wait_collection(page, req); page.wait_for_timeout(500)
                check(not page.locator('#analytics-consent').is_visible(), path+' acceptance persisted')
                check(counts(page)=={'scripts':1,'configs':1}, path+' reload single initialization')
                results['requests'].extend(google(req))
                check(sum('google-analytics.com/g/collect' in u and parse_qs(urlsplit(u).query).get('tid')==['G-NHB0PGPYTW'] and parse_qs(urlsplit(u).query).get('en')==['page_view'] for u in req)==1, path+' single pageview after reload')
                # Revocation causes clean document; future interactions send nothing.
                settings(page); req.clear()
                with page.expect_navigation(): reject(page)
                page.wait_for_timeout(700)
                page.evaluate('window.scrollTo(0,document.body.scrollHeight)');page.wait_for_timeout(700)
                check(not google(req) and not ga_cookies(c), path+' revoked no requests/cookies')
                check(not err and not fail, path+' browser errors: '+str(err+fail))
                results.setdefault('intercepted_beacon_aborts', []).extend(intercepted_aborts)
                results['cases'].append({'path':path,'fresh':'PASS','reject':'PASS','accept':'PASS','duplicate':'PASS','reload':'PASS','revoke':'PASS','errors':err,'failures':fail})
                c.close()
            for path in PATHS:
                for width in WIDTHS:
                    c, req, err, fail, intercepted_aborts = context(viewport={'width':width,'height':900}, reduced_motion='reduce')
                    page=c.new_page();page.goto(base+path)
                    metrics=page.evaluate("""() => {const d=document.querySelector('#analytics-consent').getBoundingClientRect();return {overflow:document.documentElement.scrollWidth>innerWidth,dialogFits:d.left>=0&&d.right<=innerWidth&&d.top>=0&&d.bottom<=innerHeight};}""")
                    check(not metrics['overflow'] and metrics['dialogFits'], f'{path} width {width}: {metrics}')
                    for value in ['denied','accepted']:
                        button=page.locator('[data-analytics-decision="'+value+'"]');button.scroll_into_view_if_needed()
                        check(button.is_visible(), 'button visible')
                        box=button.bounding_box();check(box['y']>=0 and box['y']+box['height']<=900, 'button within viewport')
                        check(button.evaluate('(b)=>{const r=b.getBoundingClientRect();return b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));}'), 'button unobscured')
                    reject(page)
                    # Service pages intentionally hide the desktop nav at 620px.
                    # Their home/brand and breadcrumb links retain navigation.
                    home=page.locator('header a[href="/"]').first
                    check(home.is_visible(), f'{path} home navigation visible {width}')
                    home.focus();check(home.evaluate('(a)=>document.activeElement===a'), 'home link keyboard reachable')
                    # Existing mobile toggle, where present, remains usable.
                    toggles=page.locator('button[aria-expanded]')
                    for i in range(toggles.count()):
                        toggle=toggles.nth(i)
                        if toggle.is_visible():
                            toggle.click();check(toggle.get_attribute('aria-expanded')=='true','navigation opens');toggle.click()
                    page.locator('.analytics-consent-settings').focus();page.keyboard.press('Enter')
                    check(page.locator('#analytics-consent').is_visible(), 'keyboard reopen')
                    check(not err and not fail, f'{path} {width}: {err+fail}')
                    results['responsive'].append({'path':path,'width':width,'result':'PASS',**metrics})
                    c.close()
            # Storage blocked or corrupt: fail closed and remain usable.
            for seed in ['blocked', 'corrupt']:
                c, req, err, fail, intercepted_aborts=context()
                if seed=='blocked': c.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked storage')}})")
                else: c.add_init_script("if(location.protocol === 'http:') localStorage.setItem('dpn-analytics-consent','unexpected')")
                page=c.new_page();page.goto(base+'/');reject(page)
                check(not google(req) and not ga_cookies(c) and not err,'storage fallback '+seed+': '+str(err))
                settings(page);accept(page);page.wait_for_timeout(2500)
                check(counts(page)=={'scripts':1,'configs':1},'storage fallback accept')
                settings(page)
                with page.expect_navigation(): reject(page)
                req.clear();page.wait_for_timeout(500);check(not google(req) and not err,'storage fallback revoke')
                results['cases'].append({'storage':seed,'result':'PASS'});c.close()
            # Cross-tab revocation of an active analytics document.
            c, req, err, fail, intercepted_aborts=context();one=c.new_page();one.goto(base+'/');accept(one);wait_collection(one, req)
            req.clear()
            two=c.new_page();two.goto(base+'/en/');wait_collection(two, req);two.wait_for_timeout(500);settings(two);req.clear()
            with one.expect_navigation():
                with two.expect_navigation():reject(two)
            one.wait_for_timeout(700)
            check(not google(req) and not ga_cookies(c) and not err,'cross-tab revocation: '+str({'requests':google(req),'cookies':ga_cookies(c),'errors':err}))
            results['cases'].append({'cross_tab_revoke':'PASS'});c.close()
            # Slow script delivery followed by immediate revocation.
            c, req, err, fail, intercepted_aborts=context()
            pending = []
            c.route('**/gtag/js?*', lambda route: pending.append(route))
            page=c.new_page();page.goto(base+'/');accept(page);page.wait_for_timeout(100)
            check(bool(pending), 'Google script held in flight')
            settings(page)
            with page.expect_navigation():reject(page)
            for route in pending: route.abort()
            req.clear();page.wait_for_timeout(500)
            check(not google(req) and not ga_cookies(c),'in-flight revoke')
            results['cases'].append({'in_flight_revoke':'PASS'});c.close()
            for path in ['/', '/en/']:
                c, req, err, fail, intercepted_aborts=context(java_script_enabled=False)
                page=c.new_page();page.goto(base+path)
                check(page.locator('a[href="mailto:kontakt@datenpflege-nord.de"]').count()>0, 'no-JS email link')
                check(page.locator('form').get_attribute('action')=='mailto:kontakt@datenpflege-nord.de','no-JS mailto form')
                check(not google(req),'no-JS no Google')
                results['cases'].append({'no_js':path,'result':'PASS'});c.close()
            results['result']='PASS'
        finally:
            b.close();server.shutdown();server.server_close();thread.join()
            Path(output).write_text(json.dumps(results,indent=2))
    print(json.dumps({'result':results['result'],'cases':len(results['cases']),'responsive':len(results['responsive']),'output':str(output)}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',default='/tmp/dpn-consent-qa.json');args=parser.parse_args();run(args.output)
