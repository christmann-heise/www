"""Build the preview index and three genuine Hugo sites. No network is required."""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hugo", default="hugo")
    parser.add_argument("--destination", default="public")
    parser.add_argument("--base-url", default="https://christmann-heise.github.io/www/")
    args = parser.parse_args()
    destination = (ROOT / args.destination).resolve()
    if destination == ROOT or ROOT not in destination.parents:
        raise SystemExit("Destination must be a separate directory inside the repository")
    destination.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "scripts/build-original.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/apply-branding.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "christmann-heise-designs/build-comparison.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/prepare-hugo.py"], cwd=ROOT, check=True)
    shutil.copyfile(ROOT / "index.html", destination / "index.html")
    previews = destination / "christmann-heise-designs"
    previews.mkdir(exist_ok=True)
    for name in ("01-Ruhig-Salbei.html", "02-Editorial-Bordeaux.html", "Christmann-Heise-Designvergleich.html"):
        shutil.copyfile(ROOT / "christmann-heise-designs" / name, previews / name)
    for site, route in (("original", "03-Original"), ("agnes", "05-Agnes"), ("blunix", "06-Blunix")):
        subprocess.run([args.hugo, "--source", str(ROOT / "hugo" / site),
                        "--destination", str(previews / route),
                        "--baseURL", args.base_url.rstrip("/") + "/christmann-heise-designs/" + route + "/"],
                       cwd=ROOT, check=True)
    (destination / ".nojekyll").write_text("", encoding="utf-8")
    print("Built five previews; variants 3, 5 and 6 rendered by Hugo")


if __name__ == "__main__":
    main()
