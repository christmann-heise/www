"""Prevent themes from dropping the original branding or mandatory Notara embed."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OriginalBranding(unittest.TestCase):
    def test_shared_public_embed_has_original_identifier(self):
        loader = (ROOT / 'shared/notara-public.js').read_text(encoding='utf8')
        self.assertIn("'1499', 'popup'", loader)
        self.assertIn('https://app.notara.de/js/notary-datasheet-widget.js', loader)
        self.assertIn("widgetOpenButtonColor: '#7a3674'", loader)

    def test_all_five_variants_include_notara_and_original_fonts(self):
        base = ROOT / 'public/christmann-heise-designs'
        for name in ['01-Ruhig-Salbei.html','02-Editorial-Bordeaux.html']:
            page = (base / name).read_text(encoding='utf8')
            self.assertIn('original-brand:start', page)
            self.assertIn('new NotaryDatasheetWidget', page)
            self.assertIn('Dosis', page)
        for name in ['03-Original','05-Agnes','06-Blunix']:
            for route in ['', 'rechtsanwaeltinnen','notarinnen','mediatorin','kontakt','impressum','datenschutz']:
                page = (base / name / route / 'index.html').read_text(encoding='utf8')
                self.assertIn('assets/notara-public.js', page)
                self.assertIn('original-fonts.css', page)
                if name != '03-Original':
                    self.assertIn('original-brand.css', page)

    def test_recovered_original_portraits_match_preserved_source_bytes(self):
        import hashlib,json
        evidence = json.loads((ROOT / 'docs/ORIGINALBILDER-2026-10-26.json').read_text(encoding='utf8'))
        for item in evidence:
            image = ROOT / 'christmann-heise-designs/03-Original' / item['file']
            self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), item['sha256'])
