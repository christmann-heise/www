"""Verify content preservation and preview navigation in the built Hugo output."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["", "rechtsanwaeltinnen", "notarinnen", "mediatorin", "kontakt", "impressum", "datenschutz"]
ROUTES = ["03-Original"]


class Node:
    def __init__(self, tag="", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self, excluded_class=None):
        if self.tag in ("script", "style"):
            return ""
        if excluded_class and excluded_class in self.attrs.get("class", "").split():
            return ""
        return "".join(c if isinstance(c, str) else c.text(excluded_class) for c in self.children)

    def find_class(self, name):
        result = [self] if name in self.attrs.get("class", "").split() else []
        for child in self.children:
            if isinstance(child, Node):
                result.extend(child.find_class(name))
        return result


class Document(HTMLParser):
    VOID = set("area base br col embed hr img input link meta param source track wbr".split())

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def original_text(text, *, without_legacy_contact_form=False):
    doc = Document(text).root
    nodes = doc.find_class("module-header") + doc.find_class("fw-page-builder-content")
    excluded = "wpcf7" if without_legacy_contact_form else None
    return re.sub(r"\s+", " ", " ".join(n.text(excluded) for n in nodes)).strip()


def verify_icon_fonts(destination="public"):
    """Reject the missing symbol font that previously rendered literal zeros."""
    evidence = json.loads((ROOT / "docs/ORIGINAL-SYMBOLE-2026-10-28.json").read_text(encoding="utf-8"))
    for base in (ROOT / destination, ROOT / destination / "christmann-heise-designs/03-Original"):
        css_path = base / "assets/5c3a0d53e995-linea-icons.css"
        css = css_path.read_text(encoding="utf-8")
        referenced = {
            (css_path.parent / urlsplit(url).path).resolve()
            for url in re.findall(r'url\([\"\']?([^\)\"\']+)', css)
        }
        for item in evidence["fonts"]:
            font = base / item["file"]
            if font.resolve() not in referenced or not font.is_file():
                raise AssertionError("Missing original icon font: " + str(font))
            if hashlib.sha256(font.read_bytes()).hexdigest() != item["sha256"]:
                raise AssertionError("Original icon font changed: " + str(font))


def verify_form_runtime(destination="public"):
    """Prevent the preview-wide submit interceptor from reaching publication."""
    for base in (ROOT / destination, ROOT / destination / "christmann-heise-designs/03-Original"):
        if (base / "assets/preview-runtime.js").exists():
            raise AssertionError("Preview form blocker shipped: " + str(base))
        for slug in PAGES:
            page = base / slug / "index.html"
            scripts = re.findall(r'<script\b[^>]*\bsrc\s*=\s*[\"\']([^\"\']+)',
                                 page.read_text(encoding="utf-8"), re.I)
            names = {Path(urlsplit(src).path).name for src in scripts}
            if "preview-runtime.js" in names:
                raise AssertionError("Preview form blocker loaded: " + str(page))
            if "notara-public.js" not in names:
                raise AssertionError("Public Notara loader missing: " + str(page))
            if slug == "kontakt" and re.search(r'<form\b', page.read_text(encoding="utf-8"), re.I):
                raise AssertionError("WordPress contact form still present: " + str(page))


def verify(destination="public"):
    verify_icon_fonts(destination)
    verify_form_runtime(destination)
    out = ROOT / destination / "christmann-heise-designs"
    checked = []
    # The canonical homepage is Original, never the obsolete six-way chooser.
    root_home = (ROOT / destination / "index.html").read_text(encoding="utf-8")
    if "module-header" not in root_home or "Christmann &amp; Heise" not in root_home:
        raise AssertionError("Site root is not the Original homepage")
    if "Designvorschau · Drei Varianten" in root_home:
        raise AssertionError("Preview chooser incorrectly installed at site root")
    for slug in PAGES:
        root_file = ROOT / destination / slug / "index.html"
        if not root_file.is_file():
            raise AssertionError("Missing canonical Original page: " + str(root_file))
        source = ROOT / "docs/archive-original" / ((slug or "startseite-2026-01-13") + ".html.txt")
        if original_text(root_file.read_text(encoding="utf-8"), without_legacy_contact_form=slug == "kontakt") != original_text(source.read_text(encoding="utf-8"), without_legacy_contact_form=slug == "kontakt"):
            raise AssertionError("Canonical Original text changed: " + slug)
    expected_pages = {('index.html' if not p else p + '/index.html') for p in PAGES}
    for route in ROUTES:
        actual_pages = {p.relative_to(out / route).as_posix() for p in (out / route).rglob('*.html')}
        if actual_pages != expected_pages:
            raise AssertionError('Unexpected or missing pages: ' + route + ' ' + str(sorted(actual_pages ^ expected_pages)))
    for page in PAGES:
        source = ROOT / "docs/archive-original" / ((page or "startseite-2026-01-13") + ".html.txt")
        expected = original_text(source.read_text(encoding="utf-8"), without_legacy_contact_form=page == "kontakt")
        if not expected:
            raise AssertionError("No source content: " + page)
        for route in ROUTES:
            target = out / route / page / "index.html"
            actual = original_text(target.read_text(encoding="utf-8"), without_legacy_contact_form=page == "kontakt")
            if actual != expected:
                raise AssertionError(f"Original text changed: {route}/{page}")
            checked.append({"route": route + "/" + page, "content_sha256": hashlib.sha256(actual.encode()).hexdigest()})
    # Earlier HTML variants are preserved exactly, including their original typography.
    for name in ["01-Ruhig-Salbei.html", "02-Editorial-Bordeaux.html"]:
        if (out / name).read_bytes() != (ROOT / "christmann-heise-designs" / name).read_bytes():
            raise AssertionError("Earlier variant changed: " + name)
    comparison = (out / "Christmann-Heise-Designvergleich.html").read_text(encoding="utf-8")
    if (out / '03-Klar-Kobaltblau.html').exists():
        raise AssertionError('Deleted proposal is still published')
    for index in range(3):
        if f'data-index="{index}"' not in comparison:
            raise AssertionError("Missing preview choice: " + str(index + 1))
    print(json.dumps({"verified_original_pages": len(checked), "original_impressum_unchanged": True,
                      "preview_choices": 3, "checks": checked}, ensure_ascii=False, indent=2))
    return checked


if __name__ == "__main__":
    verify()
