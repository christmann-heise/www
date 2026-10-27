"""Prove the content guard rejects a changed legal page and accepts the build."""
import contextlib
import importlib.util
import io
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_site", ROOT / "scripts/verify-site.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class OriginalContentGuard(unittest.TestCase):
    def test_built_content_is_identical(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(len(guard.verify()), 14)

    def test_changed_legal_name_is_rejected(self):
        target = ROOT / "public/christmann-heise-designs/06-Blunix/impressum/index.html"
        before = target.read_bytes()
        try:
            text = before.decode("utf-8")
            text = text.replace("Christmann und Heise", "UNAPPROVED NAME")
            self.assertNotEqual(text.encode("utf-8"), before)
            target.write_bytes(text.encode("utf-8"))
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(AssertionError, "Original text changed"):
                guard.verify()
        finally:
            target.write_bytes(before)


if __name__ == "__main__":
    unittest.main()
