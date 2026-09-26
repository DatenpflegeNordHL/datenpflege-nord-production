"""Real-browser acceptance checks for the Golden homepage hero."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]
BROWSER = os.environ.get("DPN_AGENT_BROWSER")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(BROWSER, "set DPN_AGENT_BROWSER for actual hero browser QA")
class HeroBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = partial(QuietHandler, directory=str(ROOT))
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/"

    @classmethod
    def tearDownClass(cls):
        for session in ("dpn-hero-layout", "dpn-hero-promo", "dpn-contact-flow", "dpn-hero-reduced", "dpn-hero-nojs", "dpn-consent"):
            subprocess.run([BROWSER, "--session", session, "close"], capture_output=True, text=True)
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def browser(self, session, *args):
        return subprocess.check_output(
            [BROWSER, "--session", session, *args], text=True
        ).strip()

    def prepare_necessary_consent(self, session):
        self.browser(session, "open", self.url)
        self.browser(session, "eval", r'''(()=>{
          localStorage.setItem("dpn_consent_v1", JSON.stringify({
            version: 1,
            analytics: false,
            savedAt: Date.now()
          }));
          return "ok";
        })()''')

    def hero_state(self, session):
        script = r'''(()=>{
          const header=document.querySelector("header").getBoundingClientRect();
          const copy=document.querySelector(".hero-copy").getBoundingClientRect();
          const video=document.querySelector("#heroVideo");
          const source=video.querySelector("source");
          return {
            innerWidth,
            scrollWidth:document.documentElement.scrollWidth,
            headerBottom:header.bottom,
            copyTop:copy.top,
            copyRight:copy.right,
            heroVideo:!!video,
            ariaHidden:video.getAttribute("aria-hidden"),
            poster:video.getAttribute("poster"),
            sourceAttr:source.getAttribute("src"),
            dataSrc:source.getAttribute("data-src"),
            videoZ:getComputedStyle(video).zIndex,
            videoDisplay:getComputedStyle(video).display,
            overlay:getComputedStyle(document.querySelector(".hero"),"::before").backgroundImage,
            summary:document.querySelector(".hero-summary").textContent.trim(),
            entity:document.querySelector(".hero-entity").textContent.trim(),
            ctas:document.querySelectorAll(".hero-pills a").length,
            promoTag:document.querySelector("#promoPill").tagName,
            promoExpanded:document.querySelector("#promoPill").getAttribute("aria-expanded"),
            showcaseHref:document.querySelector(".hero-showcase-card").getAttribute("href"),
            typeText:document.querySelector("#typeText").textContent.trim(),
            reduce:matchMedia("(prefers-reduced-motion: reduce)").matches,
            finePointer:matchMedia("(pointer:fine)").matches
          };
        })()'''
        return json.loads(self.browser(session, "eval", script))

    def test_hero_layout_at_required_viewports(self):
        session = "dpn-hero-layout"
        self.prepare_necessary_consent(session)
        desktop = None
        for width, height in ((1440, 1000), (1024, 900), (768, 900), (430, 900), (390, 844), (360, 800), (320, 720)):
            with self.subTest(width=width):
                self.browser(session, "set", "viewport", str(width), str(height))
                self.browser(session, "open", self.url)
                self.browser(session, "wait", "700")
                state = self.hero_state(session)
                self.assertEqual(state["innerWidth"], width)
                self.assertLessEqual(state["scrollWidth"], width)
                self.assertGreaterEqual(state["copyTop"], state["headerBottom"])
                self.assertLessEqual(state["copyRight"], width + 0.5)
                self.assertTrue(state["heroVideo"])
                self.assertEqual(state["ariaHidden"], "true")
                self.assertTrue(state["poster"].startswith("/assets/hero/mainframe-poster.jpg?v="))
                self.assertTrue(state["dataSrc"].startswith("/assets/hero/mainframe-hero.mp4?v="))
                self.assertEqual(state["videoZ"], "-4")
                self.assertEqual(state["videoDisplay"], "block")
                self.assertNotEqual(state["overlay"], "none")
                self.assertTrue(state["summary"])
                self.assertTrue(state["entity"])
                self.assertEqual(state["ctas"], 2)
                self.assertEqual(state["promoTag"], "BUTTON")
                self.assertEqual(state["promoExpanded"], "false")
                self.assertEqual(state["showcaseHref"], "/website-showcase/")
                if width == 1440:
                    desktop = state
        self.assertIsNotNone(desktop)
        if desktop["finePointer"]:
            self.assertTrue(desktop["sourceAttr"].startswith("/assets/hero/mainframe-hero.mp4?v="))
        else:
            self.assertIsNone(desktop["sourceAttr"])
        print("HERO_BROWSER_QA_PASS: 1440/1024/768/430/390/360/320 layout, CTA hierarchy, legacy-copy veil and video visibility verified")

    def test_promo_pointer_keyboard_escape_and_outside_close(self):
        session = "dpn-hero-promo"
        self.prepare_necessary_consent(session)
        self.browser(session, "set", "viewport", "390", "844")
        self.browser(session, "open", self.url)
        self.browser(session, "wait", "500")

        self.browser(session, "click", "#promoPill")
        opened = json.loads(self.browser(session, "eval", '''(()=>{
          const pill=document.querySelector("#promoPill");
          const info=document.querySelector("#promoInfo");
          const box=info.getBoundingClientRect();
          return {expanded:pill.getAttribute("aria-expanded"),hidden:info.hidden,right:box.right,width:innerWidth,tag:pill.tagName};
        })()'''))
        self.assertEqual(opened["tag"], "BUTTON")
        self.assertEqual(opened["expanded"], "true")
        self.assertFalse(opened["hidden"])
        self.assertLessEqual(opened["right"], opened["width"])

        self.browser(session, "press", "Escape")
        self.assertEqual(self.browser(session, "get", "attr", "#promoPill", "aria-expanded"), "false")

        focus_state = json.loads(self.browser(session, "eval", '''(()=>{
          const pill=document.querySelector("#promoPill"); pill.blur(); pill.focus();
          return {expanded:pill.getAttribute("aria-expanded"),hidden:document.querySelector("#promoInfo").hidden};
        })()'''))
        self.assertEqual(focus_state, {"expanded": "true", "hidden": False})
        self.browser(session, "press", "Tab")
        self.assertEqual(self.browser(session, "get", "attr", "#promoPill", "aria-expanded"), "false")

        self.browser(session, "click", "#promoPill")
        self.browser(session, "click", ".brand")
        self.assertEqual(self.browser(session, "get", "attr", "#promoPill", "aria-expanded"), "false")
        print("PROMO_INTERACTION_QA_PASS: pointer/tap, focus, Escape, blur and outside close verified")

    def test_contact_payload_carries_promo_and_showcase_prefill_survives(self):
        session = "dpn-contact-flow"
        self.prepare_necessary_consent(session)
        self.browser(session, "set", "viewport", "390", "844")
        self.browser(session, "open", self.url)
        self.browser(session, "wait", "800")
        self.browser(session, "eval", '''(()=>{window.fetch=async(url,init)=>{window.__contactRequest={url,body:JSON.parse(init.body)};return new Response('{"ok":true}',{status:200,headers:{"Content-Type":"application/json"}})}})()''')
        self.browser(session, "fill", "#name", "QA Test")
        self.browser(session, "fill", "#email", "qa@example.com")
        self.browser(session, "select", "#topic", "website")
        self.browser(session, "fill", "#message", "Browser integration test")
        self.browser(session, "eval", 'document.querySelector("#contactForm").requestSubmit()')
        self.browser(session, "wait", "700")
        request = json.loads(self.browser(session, "eval", "window.__contactRequest"))
        self.assertEqual(request["url"], "/api/contact")
        self.assertEqual(request["body"]["promo"], "new_customer_75")
        self.assertEqual(request["body"]["message"], "Browser integration test")

        self.browser(session, "open", f"{self.url}?topic=website&design=quiet-luxury&designName=Quiet%20Luxury#kontakt")
        self.browser(session, "wait", "300")
        context = json.loads(self.browser(session, "eval", '''({topic:document.querySelector("#topic").value,message:document.querySelector("#message").value,search:location.search})'''))
        self.assertEqual(context["topic"], "website")
        self.assertIn("Quiet Luxury", context["message"])
        self.assertEqual(context["search"], "")
        print("CONTACT_FLOW_QA_PASS: normal fields, structured promo payload and showcase prefill verified")

    def test_consent_blocks_analytics_until_explicit_choice(self):
        session = "dpn-consent"
        self.browser(session, "network", "route", "**/googletagmanager.com/**", "--abort")
        self.browser(session, "network", "route", "**/google-analytics.com/**", "--abort")
        self.browser(session, "open", self.url)
        self.browser(session, "eval", 'localStorage.removeItem("dpn_consent_v1")')
        self.browser(session, "open", self.url)
        self.browser(session, "wait", "300")

        initial = json.loads(self.browser(session, "eval", r'''(()=>{
          const dialog=document.querySelector("#dpn-consent-dialog");
          return {
            open:!!dialog?.open,
            googleScript:!!document.querySelector('script[src*="googletagmanager.com"]'),
            gaCookie:document.cookie.split(/;/).some(part=>part.trim().startsWith("_ga")),
            choice:localStorage.getItem("dpn_consent_v1")
          };
        })()'''))
        self.assertEqual(initial, {
            "open": True,
            "googleScript": False,
            "gaCookie": False,
            "choice": None,
        })

        self.browser(session, "click", "#dpn-consent-dialog button:first-of-type")
        rejected = json.loads(self.browser(session, "eval", r'''(()=>{
          const saved=JSON.parse(localStorage.getItem("dpn_consent_v1"));
          return {
            open:document.querySelector("#dpn-consent-dialog").open,
            analytics:saved.analytics,
            googleScript:!!document.querySelector('script[src*="googletagmanager.com"]')
          };
        })()'''))
        self.assertEqual(rejected, {
            "open": False,
            "analytics": False,
            "googleScript": False,
        })

        self.browser(session, "click", "[data-dpn-consent-settings]")
        self.browser(session, "click", "#dpn-consent-dialog button:nth-of-type(2)")
        self.browser(session, "wait", "100")
        accepted = json.loads(self.browser(session, "eval", r'''(()=>{
          const saved=JSON.parse(localStorage.getItem("dpn_consent_v1"));
          return {
            open:document.querySelector("#dpn-consent-dialog").open,
            analytics:saved.analytics,
            googleScript:!!document.querySelector('script[src*="googletagmanager.com"]')
          };
        })()'''))
        self.assertEqual(accepted, {
            "open": False,
            "analytics": True,
            "googleScript": True,
        })

        self.browser(session, "click", "[data-dpn-consent-settings]")
        self.browser(session, "click", "#dpn-consent-dialog button:first-of-type")
        self.browser(session, "wait", "300")
        revoked = json.loads(self.browser(session, "eval", r'''(()=>{
          const saved=JSON.parse(localStorage.getItem("dpn_consent_v1"));
          return {
            analytics:saved.analytics,
            googleScript:!!document.querySelector('script[src*="googletagmanager.com"]'),
            gaCookie:document.cookie.split(/;/).some(part=>part.trim().startsWith("_ga"))
          };
        })()'''))
        self.assertEqual(revoked, {
            "analytics": False,
            "googleScript": False,
            "gaCookie": False,
        })
        print("CONSENT_QA_PASS: GA4 blocked before consent, reject respected, accept gated, revocation reloads clean")

    def test_reduced_motion_keeps_static_poster(self):
        session = "dpn-hero-reduced"
        self.prepare_necessary_consent(session)
        self.browser(session, "set", "viewport", "1440", "1000")
        self.browser(session, "set", "media", "light", "reduced-motion")
        self.browser(session, "open", self.url)
        self.browser(session, "wait", "400")
        state = self.hero_state(session)
        self.assertTrue(state["reduce"])
        self.assertIsNone(state["sourceAttr"])
        self.assertTrue(state["poster"].startswith("/assets/hero/mainframe-poster.jpg?v="))
        self.assertTrue(state["typeText"])
        print("HERO_REDUCED_MOTION_PASS: MP4 source remains unloaded and poster stays available")

    def test_no_js_fallback_keeps_content_and_poster(self):
        session = "dpn-hero-nojs"
        self.prepare_necessary_consent(session)
        self.browser(session, "open", "about:blank")
        self.browser(session, "network", "route", "**/assets/home-de.js*", "--abort")
        self.browser(session, "set", "viewport", "390", "844")
        self.browser(session, "open", self.url)
        self.browser(session, "wait", "400")
        state = self.hero_state(session)
        self.assertIsNone(state["sourceAttr"])
        self.assertTrue(state["poster"].startswith("/assets/hero/mainframe-poster.jpg?v="))
        self.assertTrue(state["typeText"])
        self.assertTrue(state["summary"])
        self.assertTrue(state["entity"])
        self.assertEqual(state["ctas"], 2)
        self.assertLessEqual(state["scrollWidth"], 390)
        print("HERO_NO_JS_PASS: content and static poster remain usable with home JS blocked")


if __name__ == "__main__":
    unittest.main()
