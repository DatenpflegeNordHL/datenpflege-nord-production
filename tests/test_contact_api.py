"""Contract tests for structured contact promotions without sending mail."""
import importlib.util
import http.client
import json
import os
from pathlib import Path
from threading import Thread
from http.server import ThreadingHTTPServer
from unittest import TestCase, mock


ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("DEOMAIL_API_KEY", "test-key")
spec = importlib.util.spec_from_file_location("dpn_contact_api", ROOT / "backend/contact_api.py")
contact_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contact_api)


class ContactApiTests(TestCase):
    def setUp(self):
        contact_api.requests_by_ip.clear()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), contact_api.Handler)
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def post(self, extra=None):
        body = {
            "name": "QA Test",
            "email": "qa@example.com",
            "topic": "website",
            "message": "Test request without external delivery.",
            "website": "",
        }
        body.update(extra or {})
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        connection.request(
            "POST",
            "/api/contact",
            body=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        response = connection.getresponse()
        result = response.status, json.loads(response.read())
        connection.close()
        return result

    @mock.patch.object(contact_api.urllib.request, "urlopen")
    def test_promo_is_validated_and_added_to_internal_mail(self, deliver):
        deliver.return_value.__enter__.return_value.read.return_value = b'{"success":true}'
        status, response = self.post({"promo": "new_customer_75"})
        self.assertEqual((status, response), (200, {"ok": True}))
        provider_payload = json.loads(deliver.call_args.args[0].data)
        self.assertIn("Aktion: 75 % Neukundenrabatt (new_customer_75)", provider_payload["text"])
        self.assertNotIn("promo", provider_payload)

    @mock.patch.object(contact_api.urllib.request, "urlopen")
    def test_normal_request_without_promo_still_works(self, deliver):
        deliver.return_value.__enter__.return_value.read.return_value = b'{"success":true}'
        status, response = self.post()
        self.assertEqual((status, response), (200, {"ok": True}))
        provider_payload = json.loads(deliver.call_args.args[0].data)
        self.assertNotIn("Aktion:", provider_payload["text"])

    @mock.patch.object(contact_api.urllib.request, "urlopen")
    def test_unknown_promo_is_rejected_before_delivery(self, deliver):
        status, response = self.post({"promo": "unverified_offer"})
        self.assertEqual((status, response), (400, {"ok": False, "error": "invalid_promo"}))
        deliver.assert_not_called()
