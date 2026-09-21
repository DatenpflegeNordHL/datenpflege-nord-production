#!/usr/bin/env python3
import json
import os
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock

HOST = "127.0.0.1"
PORT = 8091

DEOMAIL_URL = "https://api.deomail.com/v1/send"
API_KEY = os.environ["DEOMAIL_API_KEY"]

MAIL_FROM = "kontakt@datenpflege-nord.de"
MAIL_TO = "kontakt@datenpflege-nord.de"

ALLOWED_ORIGINS = {
    "https://datenpflege-nord.de",
    "https://www.datenpflege-nord.de",
}

TOPICS = {
    "software": "Softwareentwicklung",
    "data": "Datenpflege",
    "website": "Website",
    "automation": "Automatisierung",
    "other": "Sonstiges",
}

PROMOS = {
    "new_customer_75": "75 % Neukundenrabatt",
}

EMAIL_RE = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,190}$")

RATE_LIMIT = 5
RATE_WINDOW = 600
requests_by_ip = defaultdict(deque)
rate_lock = Lock()


def limited(ip):
    now = time.time()

    with rate_lock:
        q = requests_by_ip[ip]

        while q and now - q[0] > RATE_WINDOW:
            q.popleft()

        if len(q) >= RATE_LIMIT:
            return True

        q.append(now)
        return False


class Handler(BaseHTTPRequestHandler):
    server_version = "DPNContact/1.0"

    def json_response(self, status, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()

        self.wfile.write(raw)

    def client_ip(self):
        return (
            self.headers.get("X-Real-IP")
            or self.headers.get("CF-Connecting-IP")
            or self.client_address[0]
        ).split(",")[0].strip()

    def do_GET(self):
        if self.path == "/health":
            return self.json_response(200, {"ok": True})

        return self.json_response(
            404,
            {"ok": False, "error": "not_found"}
        )

    def do_POST(self):
        if self.path != "/api/contact":
            return self.json_response(
                404,
                {"ok": False, "error": "not_found"}
            )

        origin = self.headers.get("Origin")

        if origin and origin not in ALLOWED_ORIGINS:
            return self.json_response(
                403,
                {"ok": False, "error": "origin_not_allowed"}
            )

        ip = self.client_ip()

        if limited(ip):
            return self.json_response(
                429,
                {"ok": False, "error": "rate_limited"}
            )

        if "application/json" not in (
            self.headers.get("Content-Type") or ""
        ):
            return self.json_response(
                415,
                {"ok": False, "error": "json_required"}
            )

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self.json_response(
                400,
                {"ok": False, "error": "bad_length"}
            )

        if length <= 0 or length > 65536:
            return self.json_response(
                413,
                {"ok": False, "error": "payload_too_large"}
            )

        try:
            data = json.loads(self.rfile.read(length))
        except Exception:
            return self.json_response(
                400,
                {"ok": False, "error": "invalid_json"}
            )

        # Honeypot für simple Formular-Bots
        if str(data.get("website", "")).strip():
            return self.json_response(200, {"ok": True})

        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip()
        topic_key = str(data.get("topic", "other")).strip()
        message = str(data.get("message", "")).strip()
        promo_key = str(data.get("promo", "")).strip()

        if not (2 <= len(name) <= 120):
            return self.json_response(
                400,
                {"ok": False, "error": "invalid_name"}
            )

        if not EMAIL_RE.match(email) or len(email) > 254:
            return self.json_response(
                400,
                {"ok": False, "error": "invalid_email"}
            )

        if topic_key not in TOPICS:
            return self.json_response(
                400,
                {"ok": False, "error": "invalid_topic"}
            )

        if not (5 <= len(message) <= 5000):
            return self.json_response(
                400,
                {"ok": False, "error": "invalid_message"}
            )

        if promo_key and promo_key not in PROMOS:
            return self.json_response(
                400,
                {"ok": False, "error": "invalid_promo"}
            )

        topic = TOPICS[topic_key]
        promo = PROMOS.get(promo_key)

        subject = f"Website-Anfrage: {topic}"

        promo_line = f"Aktion: {promo} ({promo_key})\n\n" if promo else ""
        text = (
            "Neue Anfrage über datenpflege-nord.de\n\n"
            f"Name: {name}\n"
            f"E-Mail: {email}\n"
            f"Thema: {topic}\n\n"
            f"{promo_line}"
            "Nachricht:\n"
            f"{message}\n"
        )

        payload = json.dumps({
            "from": MAIL_FROM,
            "to": [MAIL_TO],
            "subject": subject,
            "text": text,
            "fingerprint": False
        }, ensure_ascii=False).encode("utf-8")

        req = urllib.request.Request(
            DEOMAIL_URL,
            data=payload,
            method="POST",
            headers={
                "X-API-Key": API_KEY,
                "Content-Type": "application/json",
                "User-Agent": "DatenpflegeNord-Contact/1.0"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            if not result.get("success"):
                raise RuntimeError("DeoMail success=false")

        except urllib.error.HTTPError as exc:
            print(
                f"DeoMail HTTP error: {exc.code}",
                flush=True
            )

            return self.json_response(
                502,
                {"ok": False, "error": "mail_delivery_failed"}
            )

        except Exception as exc:
            print(
                f"DeoMail error: {type(exc).__name__}",
                flush=True
            )

            return self.json_response(
                502,
                {"ok": False, "error": "mail_delivery_failed"}
            )

        return self.json_response(200, {"ok": True})


if __name__ == "__main__":
    print(
        f"DPN Contact API läuft auf {HOST}:{PORT}",
        flush=True
    )

    ThreadingHTTPServer(
        (HOST, PORT),
        Handler
    ).serve_forever()
