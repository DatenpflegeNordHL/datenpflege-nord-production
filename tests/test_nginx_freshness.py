"""Isolated nginx candidate and real-browser freshness acceptance tests.

Uses only loopback, a temporary webroot, pid/log files and a contact stub.
Never reloads nginx, touches /srv, or contacts the production backend.
Set DPN_AGENT_BROWSER to an installed agent-browser executable for browser gate.
"""
import contextlib
import hashlib
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'ops/deploy'))
import check_asset_versions as assets

class ContactStub(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"fixture":true}')
    do_POST=do_GET
    def log_message(self,*a):pass

def port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]

class Candidate:
    def __init__(self,base):
        self.root=base/'public';self.root.mkdir()
        for p in assets.public_files(ROOT):
            dest=self.root/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        self.base=base
        self.stub=ThreadingHTTPServer(('127.0.0.1',0),ContactStub)
        self.thread=threading.Thread(target=self.stub.serve_forever,daemon=True);self.thread.start()
        self.processes=[];self.ports={}
        for name in ['baseline','candidate']:
            directory=base/name;directory.mkdir()
            text=(ROOT/'ops/nginx/datenpflege-nord.baseline.conf').read_text()
            if name=='candidate':
                target=directory/'datenpflege-nord.conf';target.write_text(text)
                subprocess.run(['patch','--silent',str(target),str(ROOT/'ops/nginx/datenpflege-nord-html-freshness.patch')],check=True)
                text=target.read_text()
            p=port();self.ports[name]=p
            text=text.replace('server_name datenpflege-nord.de;', 'server_name datenpflege-nord.de localhost 127.0.0.1;')
            text=text.replace('127.0.0.1:8080',f'127.0.0.1:{p}').replace('/srv/datenpflege-nord/current',str(self.root))
            text=text.replace('127.0.0.1:8091',f'127.0.0.1:{self.stub.server_port}')
            text=text.replace('/var/log/nginx/datenpflege-nord.access.log',str(directory/'access.log')).replace('/var/log/nginx/datenpflege-nord.error.log',str(directory/'error.log'))
            config=directory/'nginx.conf'
            config.write_text(f'pid {directory}/nginx.pid;\nerror_log {directory}/startup.log;\nevents {{}}\nhttp {{\ninclude /etc/nginx/mime.types;\nlog_format freshness \'$uri $args $status $http_if_none_match $http_if_modified_since\';\naccess_log {directory}/all.log freshness;\n'+text.replace('access_log '+str(directory/'access.log')+';','access_log '+str(directory/'access.log')+' freshness;')+'\n}\n')
            subprocess.run(['nginx','-t','-p',str(directory),'-c',str(config)],check=True,capture_output=True,text=True)
            process=subprocess.Popen(['nginx','-p',str(directory),'-c',str(config),'-g','daemon off;'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            self.processes.append(process)
            for _ in range(50):
                if process.poll() is not None:raise RuntimeError(process.stderr.read().decode())
                try:self.get(name,'/healthz');break
                except OSError:time.sleep(.05)
            else:raise RuntimeError('Isolated nginx did not start')
    def get(self,name,path,headers=None,method='GET'):
        conn=http.client.HTTPConnection('127.0.0.1',self.ports[name],timeout=5)
        conn.request(method,path,headers={'Host':'datenpflege-nord.de',**(headers or {})})
        r=conn.getresponse();result=(r.status,dict(r.getheaders()),r.read(),r.getheaders());conn.close();return result
    def close(self):
        for p in self.processes:
            p.terminate();p.wait(timeout=5);p.stderr.close()
        self.stub.shutdown();self.stub.server_close();self.thread.join()

@unittest.skipUnless(shutil.which('nginx'),'nginx is required')
class NginxFreshnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='dpn-nginx-freshness-')
        cls.c=Candidate(Path(cls.temp.name))
    @classmethod
    def tearDownClass(cls):
        cls.c.close();cls.temp.cleanup()

    def test_html_revalidates_with_validators_304_and_security_headers(self):
        for path in ['/', '/en/', '/softwareentwicklung-luebeck/', '/index.html','/webentwicklung-luebeck/','/ki-automatisierung-luebeck/','/impressum/','/datenschutz/','/missing.html']:
            with self.subTest(path=path):
                status,headers,_,_=self.c.get('candidate',path)
                self.assertEqual(status,404 if path=='/missing.html' else 200)
                self.assertEqual(headers.get('Cache-Control'),'no-cache')
                for name in ['X-Content-Type-Options','Referrer-Policy','X-Frame-Options']:
                    self.assertEqual(headers.get(name),self.c.get('baseline',path)[1].get(name))
                    self.assertTrue(headers.get(name))
                if status==200:
                    self.assertIn('ETag',headers);self.assertIn('Last-Modified',headers)
                    for validator in [{'If-None-Match':headers['ETag']},{'If-Modified-Since':headers['Last-Modified']}]:
                        s,h,body,_=self.c.get('candidate',path,validator)
                        self.assertEqual(s,304);self.assertEqual(body,b'');self.assertEqual(h['Cache-Control'],'no-cache')
                        self.assertEqual(h['X-Content-Type-Options'],'nosniff')

    def test_non_html_policies_and_contact_route_unchanged(self):
        for path in ['/assets/home.css','/assets/home-de.js','/favicon.svg',
                     '/assets/profile/dustin-zander.webp',
                     '/og-datenpflege-nord.png','/robots.txt','/sitemap.xml','/healthz','/api/contact']:
            with self.subTest(path=path):
                before=self.c.get('baseline',path);after=self.c.get('candidate',path)
                self.assertEqual(before[0],after[0]);self.assertEqual(before[2],after[2])
                for key in ['Cache-Control','ETag','Last-Modified','Content-Type','X-Content-Type-Options','Referrer-Policy','X-Frame-Options']:
                    self.assertEqual([v for k,v in before[3] if k==key],[v for k,v in after[3] if k==key])
        self.assertEqual(self.c.get('candidate','/og-datenpflege-nord.png')[1]['Cache-Control'],'no-cache, no-store, must-revalidate')
        self.assertEqual(self.c.get('candidate','/api/contact',method='POST')[1]['Cache-Control'],'no-store')

    @unittest.skipUnless(os.environ.get('DPN_AGENT_BROWSER'),'set DPN_AGENT_BROWSER for actual browser gate')
    def test_browser_normal_reuse_and_changed_release_without_cache_clear(self):
        directory=self.c.root/'probe';directory.mkdir(exist_ok=True)
        (directory/'leaf.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="2" height="2"><rect width="2" height="2" fill="red"/></svg>')
        (directory/'fixed.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        (directory/'style.css').write_text('body{background-image:url(leaf.svg)}')
        (directory/'index.html').write_text('<!doctype html><html><head><link rel="stylesheet" href="style.css"></head><body>release-one<img src="leaf.svg"><img id="fixed" src="fixed.svg"></body></html>')
        assets.generate(directory)
        url=f'http://127.0.0.1:{self.c.ports["candidate"]}/probe/'
        command=[os.environ['DPN_AGENT_BROWSER'],'--session','dpn-freshness-fixture']
        def browser(*args):return subprocess.check_output(command+list(args),text=True).strip()
        def state():
            return json.loads(browser('eval','({html:document.body.textContent,css:document.querySelector("link").href,image:document.querySelector("img").src,fixed:document.querySelector("#fixed").src})'))
        try:
            browser('open',url);first=state()
            browser('open',url);second=state();self.assertEqual(first,second)
            log=self.c.base/'candidate/access.log'
            time.sleep(.1)
            lines=log.read_text().splitlines()
            self.assertTrue(any(line.startswith('/probe/index.html ') and ' 304 ' in line for line in lines),lines)
            old_log=len(lines)
            # Change meaningful HTML and a leaf, without clearing browser cache.
            (directory/'leaf.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="2" height="2"><rect width="2" height="2" fill="blue"/></svg>')
            p=directory/'index.html';p.write_text(p.read_text().replace('release-one','release-two-new-content'))
            assets.generate(directory)
            os.utime(p,(time.time()+2,time.time()+2)) # Fixture validator changes even on coarse nginx mtime.
            browser('open',url);changed=state()
            self.assertIn('release-two-new-content',changed['html'])
            self.assertNotEqual(first['image'],changed['image']);self.assertNotEqual(first['css'],changed['css']);self.assertEqual(first['fixed'],changed['fixed'])
            time.sleep(.1);new_lines=log.read_text().splitlines()[old_log:]
            digest=hashlib.sha256((directory/'leaf.svg').read_bytes()).hexdigest()
            self.assertTrue(any('/probe/leaf.svg v='+digest+' 200 ' in line for line in new_lines),new_lines)
            received=json.loads(browser('eval','(async()=>{const r=await fetch(document.querySelector("img").src);return await r.text()})()'))
            self.assertIn('blue',received)
            cached_old=json.loads(browser('eval','(async()=>{const r=await fetch('+json.dumps(first['image'])+');return await r.text()})()'))
            self.assertIn('red',cached_old) # Old query URL remains browser-cached after source changes.
            # Old version stayed cacheable (seven days) and unchanged bytes keep their URL.
            self.assertIn('max-age=604800',self.c.get('candidate','/probe/'+first['image'].split('/probe/')[1])[1]['Cache-Control'])
            print('BROWSER_FRESHNESS_PASS: normal HTML navigation reached 304; changed HTML and leaf/CSS URLs fetched; unchanged URL retained; no cache clearing.')
        finally:browser('close')

if __name__=='__main__':unittest.main()
