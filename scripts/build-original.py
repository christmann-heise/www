"""Reproduce the seven archived original pages, without rewriting their content.

Only hosting/resource paths and preview runtime integrations are adapted.
The archive source files remain byte-for-byte intact.
"""
import hashlib
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "christmann-heise-designs/03-Original"
SOURCE = ROOT / "docs/archive-original"
PAGES = {"": "startseite-2026-01-13", **{p: p for p in (
    "rechtsanwaeltinnen", "notarinnen", "mediatorin", "kontakt", "impressum", "datenschutz")}}
manifest = json.loads((OUT / "assets-manifest.json").read_text(encoding="utf-8"))
assets = {x["original"]: x for x in manifest}
missing = []


def attr(tag, key):
    m = re.search(r"\b" + re.escape(key) + r"\s*=\s*([\"'])(.*?)\1", tag, re.S | re.I)
    return html.unescape(m[2]) if m else ""


def resource(url, prefix):
    clean = html.unescape(url).split("?")[0]
    item = assets.get(clean)
    if item and not item.get("missing") and (OUT / item["file"]).exists():
        return prefix + item["file"]
    missing.append(clean)
    return prefix + "missing/" + hashlib.sha256(clean.encode()).hexdigest()[:12] + "-" + Path(urlsplit(clean).path).name


def render(page, name):
    source = (SOURCE / (name + ".html.txt")).read_bytes().decode("utf-8")
    prefix = "../" if page else ""

    def script(match):
        tag, code = match[1], match[2]
        src = attr(tag, "src")
        if src == "https://app.notara.de/js/notary-datasheet-widget.js":
            return ""
        if src:
            clean = src.split("?")[0]
            item = assets.get(clean)
            if item and not item.get("missing"):
                return re.sub(r"\bsrc=([\"']).*?\1", 'src="' + prefix + item["file"] + '"', match[0], count=1, flags=re.S)
            return ""
        if "window.cookieconsent.initialise" in code:
            # Sandboxed comparison frames cannot access cookies. The original
            # banner remains active on the standalone archived page.
            return match[0].replace('function(){window.cookieconsent.initialise', 'function(){if(window.top!==window.self)return;window.cookieconsent.initialise')
        if "new NotaryDatasheetWidget" in code:
            return ""
        return ""

    # Keep original visual/menu scripts and public Notara widget. Analytics,
    # reCAPTCHA and WordPress backend submission scripts are not run in preview.
    rendered = re.sub(r"(<script\b[^>]*>)([\s\S]*?)</script>", script, source, flags=re.I)

    def link(match):
        tag = match[0]
        if attr(tag, "rel") != "stylesheet":
            return tag
        url = attr(tag, "href")
        target = prefix + "assets/original-fonts.css" if "fonts.googleapis.com" in url else resource(url, prefix)
        return re.sub(r"\bhref=([\"']).*?\1", 'href="' + target + '"', tag, count=1, flags=re.S)

    rendered = re.sub(r"<link\b[^>]*>", link, rendered, flags=re.I)

    def image(match):
        tag = match[0]
        for key in ("src", "data-background"):
            url = attr(tag, key)
            if "christmann-heise.de/" in url:
                target = resource(url, prefix)
                tag = re.sub(r"\b" + key + r"=([\"']).*?\1", key + '="' + target + '"', tag, count=1, flags=re.S)
        return tag

    rendered = re.sub(r"<[^>]+(?:\bsrc=|data-background=)[^>]*>", image, rendered)

    def anchor(match):
        tag = match[0]
        url = attr(tag, "href")
        parsed = urlsplit(url)
        if parsed.hostname not in (None, "christmann-heise.de", "www.christmann-heise.de") or not parsed.path.startswith("/"):
            # Original wordmark points to the domain without a trailing slash.
            if parsed.hostname not in ("christmann-heise.de", "www.christmann-heise.de") or parsed.path:
                return tag
        target_page = parsed.path.strip("/")
        if target_page not in PAGES:
            return tag
        target = prefix + (target_page + "/" if target_page else "./")
        if parsed.fragment:
            target += "#" + parsed.fragment
        return re.sub(r"\bhref=([\"']).*?\1", 'href="' + target + '"', tag, count=1, flags=re.S)

    rendered = re.sub(r"<a\b[^>]*>", anchor, rendered, flags=re.I)
    # Homepage-only accessibility and responsive improvements. Preserve every
    # word of the archived content and the untouched archival source files.
    if not page:
        rendered = rendered.replace('<section class="module-header default-height">',
                                    '<section class="module-header default-height" id="hauptinhalt">', 1)
        rendered = rendered.replace('<body class="home ',
                                    '<body class="home ', 1)
        rendered = rendered.replace('<!-- Preloader-->',
                                    '<a class="skip-to-content" href="#hauptinhalt">Zum Inhalt springen</a>\n\t\t<!-- Preloader-->', 1)
        rendered = rendered.replace('<div class="inner-navigation">',
                                    '<nav class="inner-navigation" aria-label="Hauptnavigation">', 1)
        rendered = rendered.replace('</ul></div>\n\t\t\t</div>\n\t\t</header>',
                                    '</ul></nav>\n\t\t\t</div>\n\t\t</header>', 1)
        rendered = rendered.replace('<a class="show-menu-btn" href="#">',
                                    '<a class="show-menu-btn" href="#" aria-label="Menü öffnen">', 1)
        rendered = rendered.replace('<a class="close-menu" href="#">',
                                    '<a class="close-menu" href="#" aria-label="Menü schließen">', 1)
        rendered = rendered.replace('<div class="overlay-menu font-alt">',
                                    '<div class="overlay-menu font-alt" aria-label="Mobile Navigation">', 1)
        # One H1 per page; visual styling remains on the existing h4 classes.
        rendered = rendered.replace('<h1 class="h4 font-alt">', '<p class="h4 font-alt">', 2)
        rendered = rendered.replace('</h1><p class="h4 font-alt">', '</h1><p class="h4 font-alt">', 1)
        rendered = rendered.replace('</h1></div></div></div></section>',
                                    '</p></div></div></div></section>', 1)
        rendered = rendered.replace('</h1><p class="h4 font-alt">Notarinnen',
                                    '</p><p class="h4 font-alt">Notarinnen', 1)
        rendered = rendered.replace('</head>',
                                    '<link rel="stylesheet" href="assets/original-home-enhancements.css"></head>', 1)
    # Submission is intercepted before any old or preview-origin backend request.
    runtime = '<script src="' + prefix + 'assets/preview-runtime.js"></script><script src="' + prefix + 'assets/notara-public.js" defer></script>'
    rendered = rendered.replace("</head>", '<meta name="robots" content="noindex,nofollow">' + runtime + "</head>")
    target = OUT / page / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8", newline="\n")


def main():
    shutil.copyfile(ROOT / 'shared/notara-public.js', OUT / 'assets/notara-public.js')
    shutil.copyfile(ROOT / 'shared/original-home-enhancements.css', OUT / 'assets/original-home-enhancements.css')
    # The archived map loader has no working Maps API integration in a static
    # preview. Preserve its markup; guard the optional API, without inventing a map.
    custom = OUT / assets["https://christmann-heise.de/wp-content/themes/vortex/assets/js/custom.min.js"]["file"]
    original_js = custom.read_text(encoding="utf-8")
    custom.write_text(original_js.replace('if(d.length>0){', 'if(d.length>0&&typeof google!=="undefined"){'), encoding="utf-8", newline="\n")
    # Imported Vortex CSS must point to the locally saved original template.
    style = assets["https://christmann-heise.de/wp-content/themes/vortex/style.css"]
    template = assets.get("https://christmann-heise.de/wp-content/themes/vortex/assets/css/template.min.css")
    if not template:
        template = {"file": "assets/template.min.css"}
        target = OUT / template["file"]
        target.write_bytes((SOURCE / "template.min.css").read_bytes())
    p = OUT / style["file"]
    css = (SOURCE / "theme-style.css").read_bytes().decode("utf-8")
    p.write_text(css.replace("assets/css/template.min.css", Path(template["file"]).name), encoding="utf-8", newline="\n")
    for page, name in PAGES.items():
        render(page, name)
    (OUT / "missing-assets.json").write_text(json.dumps(sorted(set(missing)), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(PAGES), "missing_assets": len(set(missing))}))


if __name__ == "__main__":
    main()
