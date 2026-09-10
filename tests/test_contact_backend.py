from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "backend" / "dpn-contact.service"
API = ROOT / "backend" / "contact_api.py"


class ContactBackendSafetyTests(unittest.TestCase):
    def test_contact_api_is_loopback_only_and_size_bounded(self) -> None:
        tree = ast.parse(API.read_text(encoding="utf-8"))
        constants: dict[str, object] = {}
        for node in tree.body:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue
            try:
                constants[target.id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue

        self.assertEqual(constants.get("HOST"), "127.0.0.1")
        self.assertEqual(constants.get("PORT"), 8091)
        self.assertEqual(constants.get("RATE_LIMIT"), 5)
        self.assertEqual(constants.get("RATE_WINDOW"), 600)

        source = API.read_text(encoding="utf-8")
        self.assertIn('length > 65536', source)
        self.assertIn('timeout=12', source)
        self.assertIn('"Cache-Control", "no-store"', source)
        self.assertIn('"X-Content-Type-Options", "nosniff"', source)

    def test_systemd_service_keeps_strict_sandbox(self) -> None:
        text = SERVICE.read_text(encoding="utf-8")
        required_lines = {
            "User=www-data",
            "Group=www-data",
            "EnvironmentFile=/etc/datenpflege-nord-contact.env",
            "NoNewPrivileges=true",
            "PrivateTmp=true",
            "PrivateDevices=true",
            "ProtectHome=true",
            "ProtectSystem=strict",
            "ProtectControlGroups=true",
            "ProtectKernelModules=true",
            "ProtectKernelTunables=true",
            "ProtectKernelLogs=true",
            "ProtectClock=true",
            "RestrictSUIDSGID=true",
            "LockPersonality=true",
            "MemoryDenyWriteExecute=true",
            "CapabilityBoundingSet=",
            "AmbientCapabilities=",
            "RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6",
            "SystemCallArchitectures=native",
            "UMask=0077",
        }
        lines = {line.strip() for line in text.splitlines()}
        self.assertEqual(required_lines - lines, set())

        self.assertNotIn("User=root", lines)
        self.assertNotIn("0.0.0.0", text)


if __name__ == "__main__":
    unittest.main()
