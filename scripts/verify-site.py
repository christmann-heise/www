"""Verify content preservation and preview navigation in the built Hugo output."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["", "rechtsanwaeltinnen", "notarinnen", "mediatorin", "kontakt", "impressum", "datenschutz"]
ROUTES = ["03-Original", "04-Arcana", "05-Agnes", "06-Blunix"]


class Node:
    def __init__(self, tag="", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        if self.tag in ("script", "style"):
            return ""
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

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


def original_text(text):
    doc = Document(text).root
    nodes = doc.find_class("module-header") + doc.find_class("fw-page-builder-content")
    return re.sub(r"\s+", " ", " ".join(n.text() for n in nodes)).strip()


def verify(destination="public"):
    out = ROOT / destination / "christmann-heise-designs"
    checked = []
    expected_pages = {('index.html' if not p else p + '/index.html') for p in PAGES}
    for route in ROUTES:
        actual_pages = {p.relative_to(out / route).as_posix() for p in (out / route).rglob('*.html')}
        if actual_pages != expected_pages:
            raise AssertionError('Unexpected or missing pages: ' + route + ' ' + str(sorted(actual_pages ^ expected_pages)))
    for page in PAGES:
        source = ROOT / "docs/archive-original" / ((page or "startseite-2026-01-13") + ".html.txt")
        expected = original_text(source.read_text(encoding="utf-8"))
        if not expected:
            raise AssertionError("No source content: " + page)
        for route in ROUTES:
            target = out / route / page / "index.html"
            actual = original_text(target.read_text(encoding="utf-8"))
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
    for index in range(6):
        if f'data-index="{index}"' not in comparison:
            raise AssertionError("Missing preview choice: " + str(index + 1))
    print(json.dumps({"verified_original_pages": len(checked), "original_impressum_unchanged": True,
                      "preview_choices": 6, "checks": checked}, ensure_ascii=False, indent=2))
    return checked


if __name__ == "__main__":
    verify()
