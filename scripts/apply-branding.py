"""Apply the same evidenced branding and public Notara embed to both older drafts."""
import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def apply():
    brand = (ROOT / 'shared/original-brand.css').read_text(encoding='utf8')
    fonts_dir = ROOT / 'christmann-heise-designs/03-Original/assets'
    font_css = (fonts_dir / 'original-fonts.css').read_text(encoding='utf8')
    def embed(match):
        filename = match[1]
        font = (fonts_dir / filename).read_bytes()
        return 'url(data:font/ttf;base64,' + base64.b64encode(font).decode() + ')'
    font_css = re.sub(r'url\(([^)]+)\)', embed, font_css)
    notara = (ROOT / 'shared/notara-public.js').read_text(encoding='utf8')
    block = '<!-- original-brand:start --><style>' + font_css + '\n' + brand + '</style><script>' + notara + '</script><!-- original-brand:end -->'
    for name in ('01-Ruhig-Salbei.html', '02-Editorial-Bordeaux.html'):
        path = ROOT / 'christmann-heise-designs' / name
        text = path.read_text(encoding='utf8')
        assets = json.loads((ROOT / 'christmann-heise-designs/03-Original/assets-manifest.json').read_text(encoding='utf8'))
        for person, suffix in [('Silke Christmann','NotarinnenSC-e1534960144126.jpg'),('Hannah-Silvia Heise','NotarinnenHH-e1534960164368.jpg')]:
            entry = next(x for x in assets if x['original'].endswith(suffix))
            image = ROOT / 'christmann-heise-designs/03-Original' / entry['file']
            if not image.exists():
                continue
            src = 'data:image/jpeg;base64,' + base64.b64encode(image.read_bytes()).decode()
            for initials in ['SC','HH']:
                before = '<div class="portrait" role="img" aria-label="' + person + '"><span class="portrait-letter" aria-hidden="true">' + initials + '</span></div>'
                after = '<div class="portrait"><img src="' + src + '" alt="' + person + '" width="668" height="1000"></div>'
                text = text.replace(before,after).replace(json.dumps(before,ensure_ascii=False)[1:-1],json.dumps(after,ensure_ascii=False)[1:-1])
        text = re.sub(r'<!-- original-brand:start -->[\s\S]*?<!-- original-brand:end -->', '', text)
        text = re.sub(r'(<meta name="theme-color" content=")[^"]+', r'\g<1>#7a3674', text)
        path.write_text(text.replace('</head>', block + '</head>', 1), encoding='utf8', newline='\n')


if __name__ == '__main__':
    apply()
