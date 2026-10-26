"""Prepare Hugo content from the preserved original HTML, without rewriting text."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "christmann-heise-designs/04-Original"
VARIANTS = [("original", "04-Original", None), ("arcana", "05-Arcana", "arcana"),
            ("agnes", "06-Agnes", "agnes"), ("blunix", "07-Blunix", "blunix")]
PAGES = ["", "rechtsanwaeltinnen", "notarinnen", "mediatorin", "kontakt", "impressum", "datenschutz"]
LABELS = ["Startseite", "Rechtsanwältinnen", "Notarinnen", "Mediatorin", "Kontakt"]


def prepare():
    for site, route, theme in VARIANTS:
        directory = ROOT / "hugo" / site
        directory.mkdir(parents=True, exist_ok=True)
        config = "baseURL = 'https://christmann-heise.github.io/www/christmann-heise-designs/" + route + "/'\n"
        config += "title = 'Christmann & Heise'\nlocale = 'de'\ndefaultContentLanguage = 'de'\n"
        config += "disableKinds = ['taxonomy', 'term', 'RSS', 'sitemap', 'section', '404']\n"
        if theme:
            config += f"theme = '{theme}'\nthemesDir = '../themes'\n"
        config += "[security]\nallowContent = ['^text/html$']\n"
        config += "[params]\nshow_post_dates = false\n"
        config += "[params.footer.contact_form]\nenabled = false\n"
        config += "[[module.mounts]]\nsource = 'static'\ntarget = 'static'\n"
        config += "[[module.mounts]]\nsource = '../../christmann-heise-designs/04-Original/assets'\ntarget = 'static/assets'\n"
        for weight, (slug, label) in enumerate(zip(PAGES, LABELS)):
            config += f"[[menus.main]]\nname = '{label}'\npageRef = '/{slug}'\nweight = {weight + 1}\n"
        (directory / "hugo.toml").write_text(config, encoding="utf-8", newline="\n")
        heads = {}
        for page in PAGES:
            doc = (SOURCE / page / "index.html").read_text(encoding="utf-8")
            head = re.search(r"<head>([\s\S]*?)</head>", doc, re.I)[1]
            body = re.search(r"(<body\b[\s\S]*?</body>)", doc, re.I)[1]
            title = html.unescape(re.sub(r"<[^>]*>", "", re.search(r'<section class="module-header[^>]*>[\s\S]*?<h1[^>]*>([\s\S]*?)</h1>', body)[1]))
            source_name = page or "startseite"
            if site == "original":
                content = body
                heads[source_name] = head
            else:
                content = re.search(r'(<section class="module-header[\s\S]*?)\s*<footer\b', body)[1]
                # The original copy is retained; only layout wrappers are themed.
                content = re.sub(r'<script\b[\s\S]*?</script>', '', content, flags=re.I)
                content = re.sub(r'\bid="map"', 'data-original-id="map"', content)
            target = directory / "content" / (page + ".html" if page else "_index.html")
            target.parent.mkdir(parents=True, exist_ok=True)
            front = json.dumps({"title": title, "layout": "original" if site == "original" else "kanzlei",
                                "source": source_name}, ensure_ascii=False, indent=2)
            target.write_text(front + "\n" + content + "\n", encoding="utf-8", newline="\n")
        if site == "original":
            (directory / "data").mkdir(exist_ok=True)
            (directory / "data/heads.json").write_text(json.dumps(heads, ensure_ascii=False), encoding="utf-8")
        print(f"Prepared {site}: {len(PAGES)} unchanged source pages")


if __name__ == "__main__":
    prepare()
