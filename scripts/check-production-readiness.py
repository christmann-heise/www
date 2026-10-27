"""Read-only release gate for the future public Kanzlei website.

This intentionally blocks production while required legal/content approvals are missing.
It does not modify original legal texts or deploy anything.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKERS = [
    ("datenschutz", "The archived privacy page contains only the avalex shortcode; an approved complete privacy notice is required."),
    ("legal-approval", "Impressum, liability text, professional disclosures and contact details need explicit professional approval."),
    ("functionality", "Contact routes and Notara integration must be checked with approved non-confidential test data."),
    ("visual-accessibility", "Desktop/mobile visual, keyboard, accessibility and performance review is outstanding."),
    ("domain-launch", "Production domain, redirects, security and email DNS must be separately approved."),
]

def main():
    status = {
        "source_variant": "03-Original",
        "publication_approved": False,
        "remaining_previews": ["01-Ruhig-Salbei", "02-Editorial-Bordeaux"],
        "blockers": [{"id": key, "reason": reason} for key, reason in BLOCKERS],
        "note": "This is a development checklist, not a certification or a production release.",
    }
    print(json.dumps(status, ensure_ascii=False, indent=2))
    raise SystemExit(1)

if __name__ == "__main__":
    main()
