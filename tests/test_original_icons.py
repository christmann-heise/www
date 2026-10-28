"""The public build must contain the symbol fonts referenced by original CSS."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_site_icons", ROOT / "scripts/verify-site.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class OriginalIcons(unittest.TestCase):
    def test_canonical_and_preview_icon_fonts(self):
        guard.verify_icon_fonts()

    def test_missing_woff_is_rejected(self):
        font = ROOT / "public/fonts/linea-basic-10.woff"
        before = font.read_bytes()
        try:
            font.unlink()
            with self.assertRaisesRegex(AssertionError, "Missing original icon font"):
                guard.verify_icon_fonts()
        finally:
            font.write_bytes(before)


if __name__ == "__main__":
    unittest.main()
