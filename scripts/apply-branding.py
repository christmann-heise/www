"""Apply the same evidenced branding and public Notara embed to both older drafts."""
import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_portraits(markup, assets, role='Notarinnen'):
    """Replace decoded HTML, including the HTML used after hash navigation."""
    for person, initials in [('Silke Christmann', 'SC'), ('Hannah-Silvia Heise', 'HH')]:
        suffix = role + initials + '-e'
        entry = next(x for x in assets if suffix in x['original'])
        image = ROOT / 'christmann-heise-designs/03-Original' / entry['file']
        src = 'data:image/jpeg;base64,' + base64.b64encode(image.read_bytes()).decode()
        before = '<div class="portrait" role="img" aria-label="' + person + '"><span class="portrait-letter" aria-hidden="true">' + initials + '</span></div>'
        after = '<div class="portrait"><img src="' + src + '" alt="' + person + '" width="668" height="1000"></div>'
        markup = markup.replace(before, after)
    return markup


def replace_route_portraits(text, assets):
    # This is JSON embedded in JavaScript. Escaped string replacements missed
    # closing tags (\/) and left the router's HTML with the old placeholders.
    marker = 'const previewRoutes='
    start = text.index(marker) + len(marker)
    routes, length = json.JSONDecoder().raw_decode(text[start:])
    for route, page in routes.items():
        role = 'Rechtsanwaeltinnen' if route == '/rechtsanwaeltinnen/' else 'Notarinnen'
        page['html'] = replace_portraits(page['html'], assets, role)
    encoded = json.dumps(routes, ensure_ascii=False).replace('</', '<\\/')
    return text[:start] + encoded + text[start + length:]


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
        text = replace_route_portraits(text, assets)
        text = replace_portraits(text, assets)
        text = re.sub(r'<!-- original-brand:start -->[\s\S]*?<!-- original-brand:end -->', '', text)
        text = re.sub(r'(<meta name="theme-color" content=")[^"]+', r'\g<1>#7a3674', text)
        path.write_text(text.replace('</head>', block + '</head>', 1), encoding='utf8', newline='\n')


if __name__ == '__main__':
    apply()
