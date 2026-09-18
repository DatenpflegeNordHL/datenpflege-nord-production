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
        for session in ("dpn-hero-layout", "dpn-hero-reduced", "dpn-hero-nojs"):
            subprocess.run([BROWSER, "--session", session, "close"], capture_output=True, text=True)
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def browser(self, session, *args):
        return subprocess.check_output(
            [BROWSER, "--session", session, *args], text=True
        ).strip()

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
            overlay:getComputedStyle(document.querySelector(".hero"),"::before").backgroundImage,
            summary:document.querySelector(".hero-summary").textContent.trim(),
            entity:document.querySelector(".hero-entity").textContent.trim(),
            ctas:document.querySelectorAll(".hero-pills a").length,
            typeText:document.querySelector("#typeText").textContent.trim(),
            reduce:matchMedia("(prefers-reduced-motion: reduce)").matches
          };
        })()'''
        return json.loads(self.browser(session, "eval", script))

    def test_hero_layout_at_required_viewports(self):
        session = "dpn-hero-layout"
        desktop = None
        for width, height in ((1440, 1000), (390, 844), (320, 720)):
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
                self.assertNotEqual(state["overlay"], "none")
                self.assertTrue(state["summary"])
                self.assertTrue(state["entity"])
                self.assertEqual(state["ctas"], 2)
                if width == 1440:
                    desktop = state
        self.assertIsNotNone(desktop)
        self.assertTrue(desktop["sourceAttr"].startswith("/assets/hero/mainframe-hero.mp4?v="))
        print("HERO_BROWSER_QA_PASS: 1440/390/320 layout, overlay and desktop lazy video source verified")

    def test_reduced_motion_keeps_static_poster(self):
        session = "dpn-hero-reduced"
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
