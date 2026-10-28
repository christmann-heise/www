"""A preview submission blocker must never reappear in the public website."""
import importlib.util
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = os.environ.get("SITE_TEST_DESTINATION", "public")
spec = importlib.util.spec_from_file_location("verify_site_forms", ROOT / "scripts/verify-site.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class FormRuntime(unittest.TestCase):
    def test_public_pages_keep_notara_without_preview_blocker(self):
        guard.verify_form_runtime(DESTINATION)

    def test_reintroduced_blocker_script_is_rejected(self):
        page = ROOT / DESTINATION / "kontakt/index.html"
        before = page.read_bytes()
        try:
            text = before.decode("utf-8").replace(
                "</head>", '<script src="../assets/preview-runtime.js"></script></head>')
            page.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "Preview form blocker loaded"):
                guard.verify_form_runtime(DESTINATION)
        finally:
            page.write_bytes(before)

    def test_reintroduced_contact_form_is_rejected(self):
        page = ROOT / DESTINATION / "kontakt/index.html"
        before = page.read_bytes()
        try:
            page.write_text(before.decode("utf-8").replace(
                "</body>", '<form class="wpcf7-form" method="post"></form></body>'), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "WordPress contact form still present"):
                guard.verify_form_runtime(DESTINATION)
        finally:
            page.write_bytes(before)

    def test_contact_address_changes_remain_rejected(self):
        page = ROOT / DESTINATION / "kontakt/index.html"
        before = page.read_bytes()
        try:
            text = before.decode("utf-8").replace("Haardtring 369", "UNAPPROVED ADDRESS")
            self.assertNotEqual(text.encode("utf-8"), before)
            page.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "Canonical Original text changed: kontakt"):
                guard.verify(DESTINATION)
        finally:
            page.write_bytes(before)


if __name__ == "__main__":
    unittest.main()
