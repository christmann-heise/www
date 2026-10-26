"""Add the four requested Hugo variants to the two remaining earlier drafts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = [("03-Original", "Original / Archiv", "Originale Gestaltung und sieben belegte Originalseiten."),
            ("04-Arcana", "Hugo Arcana", "Arcana mit den belegten Originalinhalten."),
            ("05-Agnes", "Hugo Agnes", "Agnes mit den belegten Originalinhalten."),
            ("06-Blunix", "Hugo Blunix", "Blunix mit den belegten Originalinhalten.")]


def extend(text):
    if 'data-index="5"' in text:
        return text
    cards = "\n".join('<button class="choice" type="button" data-index="' + str(i) + '" aria-pressed="false"><div class="mini mini-original"><strong>Christmann &amp; Heise</strong><p>Rechtsanwältinnen in Partnerschaft<br>Notarinnen</p></div><div class="choice-copy"><div class="choice-name"><span>' + route[:2] + ' · ' + label + '</span><span>Hugo</span></div><p>' + description + '</p></div></button>' for i, (route, label, description) in enumerate(VARIANTS, 2))
    text = text.replace('</div><div class="toolbar">', cards + '</div><div class="toolbar">', 1)
    text = text.replace('repeat(3,1fr)', 'repeat(4,minmax(0,1fr))')
    text = text.replace('</style>', '.mini-original{background:#fff;color:#7a3674;text-align:center;padding-top:35px}.mini-original strong{font:normal 20px Georgia,serif}.mini-original p{font-size:10px}@media(max-width:1000px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:480px){.cards{grid-template-columns:1fr}.mini-original{padding-top:20px}}\n</style>', 1)
    text = text.replace('Drei Designrichtungen mit denselben Kanzleiinhalten.', 'Zwei bisherige Entwürfe und vier Hugo-Varianten. Alle verwenden Originalschriften, Originalfarben und Notara.')
    text = text.replace('Drei Designrichtungen', 'Sechs Varianten')
    text = text.replace('Ruhig / Salbei', 'Ruhig').replace('Editorial / Bordeaux', 'Editorial')
    text = text.replace('Serifenschrift, sanfte Farben und ein Raster für die Anliegen.', 'Bestehender Aufbau mit Originalschriften und Originalfarben.')
    text = text.replace('Große Typografie, Partnerinnen im Vordergrund und Themen als Liste.', 'Editorial-Aufbau mit Originalschriften und Originalfarben.')
    text = text.replace('Alle Entwürfe &amp; Quellcode ↓', 'Bisheriges Quellarchiv ↓')
    start = text.index('<div class="note">')
    end = text.index('</div></main>', start)
    text = text[:start] + '<div class="note"><strong>Vorschau:</strong> Varianten 1–2 sind die früheren Entwürfe mit gemeinsamer Originalgestaltung; ihre Texte sind weiterhin Entwurfsstand. Varianten 3–6 verwenden die sieben gesicherten Originalseiten einschließlich unverändertem Impressum. Notara ist in allen Varianten eingebunden. Fehlende Originalbilder werden nicht erfunden. Das Kontaktformular übermittelt in der Vorschau keine Daten.' + text[end:]
    extra = "\n".join("urls.push(new URL('" + route + "/',location.href).href);labels.push('" + route[:2] + ' · ' + label + "');variants.push({file:'" + route + "/index.html'});" for route, label, _ in VARIANTS)
    text = text.replace("const frame=document.getElementById('preview');", extra + "\nconst frame=document.getElementById('preview');")
    text = text.replace("frame.src=urls[index];", "document.getElementById('save').hidden=index>=2;frame.src=urls[index];")
    text = text.replace("'Variante '+(index+1)+' · neue Designalternative'", "(index>=2?'Variante '+(index+1)+' · Hugo · archivierte Originalinhalte':'Variante '+(index+1)+' · bisheriger Entwurf')")
    return text


if __name__ == '__main__':
    p = ROOT / 'christmann-heise-designs/Christmann-Heise-Designvergleich.html'
    p.write_text(extend(p.read_text(encoding='utf8')), encoding='utf8', newline='\n')
