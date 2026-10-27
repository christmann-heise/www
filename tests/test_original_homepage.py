"""Regression checks for the Original homepage and retained draft previews."""
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public/christmann-heise-designs"

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class OriginalHomepage(unittest.TestCase):
    def test_homepage_semantics_and_assets(self):
        page = (PUBLIC / "03-Original/index.html").read_text(encoding="utf-8")
        doc = Tags()
        doc.feed(page)
        self.assertEqual(sum(tag == "h1" for tag, _ in doc.tags), 1)
        self.assertTrue(any(tag == "a" and attrs.get("href") == "#hauptinhalt" for tag, attrs in doc.tags))
        self.assertTrue(any(attrs.get("id") == "hauptinhalt" for _, attrs in doc.tags))
        self.assertTrue(any(tag == "nav" and attrs.get("aria-label") == "Hauptnavigation" for tag, attrs in doc.tags))
        self.assertIn("original-home-enhancements.css", page)
        self.assertTrue((PUBLIC / "03-Original/assets/original-home-enhancements.css").is_file())

    def test_canonical_homepage_is_original(self):
        root = (ROOT / "public/index.html").read_text(encoding="utf-8")
        self.assertIn("module-header", root)
        self.assertNotIn("Designvorschau · Drei Varianten", root)

    def test_only_three_previews_are_built(self):
        for route in ("04-Arcana", "05-Agnes", "06-Blunix"):
            self.assertFalse((PUBLIC / route).exists(), route)
        for filename in ("01-Ruhig-Salbei.html", "02-Editorial-Bordeaux.html"):
            self.assertTrue((PUBLIC / filename).is_file())

if __name__ == "__main__":
    unittest.main()
