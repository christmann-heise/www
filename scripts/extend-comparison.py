"""Add the four requested Hugo variants without modifying the first three HTML files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = [("04-Original", "Original / Archiv", "Originale Gestaltung und sieben belegte Originalseiten."),
            ("05-Arcana", "Hugo Arcana", "Arcana mit den belegten Originalinhalten."),
            ("06-Agnes", "Hugo Agnes", "Agnes mit den belegten Originalinhalten."),
            ("07-Blunix", "Hugo Blunix", "Blunix mit den belegten Originalinhalten.")]


def extend(text):
    if 'data-index="6"' in text:
        return text
    cards = "\n".join('<button class="choice" type="button" data-index="' + str(i) + '" aria-pressed="false"><div class="mini mini-original"><strong>Christmann &amp; Heise</strong><p>Rechtsanwältinnen in Partnerschaft<br>Notarinnen</p></div><div class="choice-copy"><div class="choice-name"><span>' + route[:2] + ' · ' + label + '</span><span>Hugo</span></div><p>' + description + '</p></div></button>' for i, (route, label, description) in enumerate(VARIANTS, 3))
    text = text.replace('</div><div class="toolbar">', cards + '</div><div class="toolbar">', 1)
    text = text.replace('repeat(3,1fr)', 'repeat(4,minmax(0,1fr))')
    text = text.replace('</style>', '.mini-original{background:#fff;color:#7a3674;text-align:center;padding-top:35px}.mini-original strong{font:normal 20px Georgia,serif}.mini-original p{font-size:10px}@media(max-width:1000px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:480px){.cards{grid-template-columns:1fr}.mini-original{padding-top:20px}}\n</style>', 1)
    text = text.replace('Drei Designrichtungen', 'Sieben Varianten')
    text = text.replace('Drei Designrichtungen mit denselben Kanzleiinhalten.', 'Drei bisherige Entwürfe und vier Hugo-Varianten auf Basis der archivierten Originalseiten.')
    text = text.replace('Alle Entwürfe &amp; Quellcode ↓', 'Bisheriges Quellarchiv ↓')
    start = text.index('<div class="note">')
    end = text.index('</div></main>', start)
    text = text[:start] + '<div class="note"><strong>Vorschau:</strong> Varianten 1–3 sind die bisherigen Entwürfe. Varianten 4–7 verwenden die sieben gesicherten Originalseiten; Firmenname, Impressum und Haftungsangaben werden nicht neu formuliert. Mehrere Originalbilder und der vollständige nachgeladene Datenschutztext sind im Archiv nicht verfügbar. Das Kontaktformular übermittelt in der Vorschau keine Daten. Das eingebettete Quellarchiv ist der frühere Arbeitsstand; die aktuellen Hugo-Projekte liegen im GitHub-Repository.' + text[end:]
    extra = "\n".join("urls.push(new URL('" + route + "/',location.href).href);labels.push('" + route[:2] + ' · ' + label + "');variants.push({file:'" + route + "/index.html'});" for route, label, _ in VARIANTS)
    text = text.replace("const frame=document.getElementById('preview');", extra + "\nconst frame=document.getElementById('preview');")
    text = text.replace("frame.src=urls[index];", "document.getElementById('save').hidden=index>=3;frame.src=urls[index];")
    text = text.replace("'Variante '+(index+1)+' · neue Designalternative'", "(index>=3?'Variante '+(index+1)+' · Hugo · archivierte Originalinhalte':'Variante '+(index+1)+' · bisheriger Entwurf')")
    return text


if __name__ == '__main__':
    p = ROOT / 'christmann-heise-designs/Christmann-Heise-Designvergleich.html'
    p.write_text(extend(p.read_text(encoding='utf8')), encoding='utf8', newline='\n')
