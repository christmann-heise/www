from pathlib import Path
import shutil, subprocess, re, hashlib, json

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'christmann-heise'
original=SOURCE/'Christmann-Heise-Vorschau.html'
saved=ROOT/'01-Ruhig-Salbei.html'
assert saved.read_bytes()==original.read_bytes(), 'Originalentwurf darf nicht verändert werden.'
projects=ROOT/'projekte'
projects.mkdir(exist_ok=True)

editorial_hero='''<section class="editorial-hero"><div class="wrap"><p class="eyebrow">Christmann &amp; Heise · Rechtsanwältinnen &amp; Notarinnen · Darmstadt</p><h1 class="editorial-title">Wichtige Fragen.<br>Persönlich <em>geklärt.</em></h1><div class="editorial-rule" aria-hidden="true"></div><div class="editorial-bottom"><p class="lead">Manche Entscheidungen brauchen einen klaren Blick und ein vertrauensvolles Gespräch. Wir begleiten Sie mit rechtlicher Erfahrung und Zeit für Ihr Anliegen.</p><div class="actions"><a class="button primary" href="@@termin-vorbereiten/">Notartermin vorbereiten <span aria-hidden="true">↗</span></a><a class="button" href="@@rechtsanwaeltinnen/">Anwaltliche Beratung <span aria-hidden="true">↗</span></a></div></div><div class="editorial-caption"><span>Silke Christmann &amp; Hannah-Silvia Heise</span><span>Haardtring 369 · Darmstadt</span></div></div></section>'''
digital_hero='''<section class="digital-hero"><div class="wrap"><div class="digital-grid"><div><p class="eyebrow">Rechtsanwältinnen &amp; Notarinnen in Darmstadt</p><h1>Wichtige Fragen.<br><span>Persönlich geklärt.</span></h1><p class="lead">Manche Entscheidungen brauchen einen klaren Blick und ein vertrauensvolles Gespräch. Wir begleiten Sie mit rechtlicher Erfahrung und Zeit für Ihr Anliegen.</p><div class="actions"><a class="button primary" href="@@termin-vorbereiten/">Notartermin vorbereiten <span aria-hidden="true">↗</span></a><a class="button" href="@@rechtsanwaeltinnen/">Anwaltliche Beratung <span aria-hidden="true">↗</span></a></div></div><aside class="quick-panel" aria-label="Direkt zu Ihrem Anliegen"><p class="eyebrow">Ihr Anliegen</p><h2>Wo dürfen wir helfen?</h2><a href="@@notarinnen/immobilien/"><span class="shortcut-icon" aria-hidden="true">01</span><span class="shortcut-label">Immobilie kaufen &amp; übertragen</span><span aria-hidden="true">↗</span></a><a href="@@notarinnen/vorsorge/"><span class="shortcut-icon" aria-hidden="true">02</span><span class="shortcut-label">Vorsorge regeln</span><span aria-hidden="true">↗</span></a><a href="@@notarinnen/erben/"><span class="shortcut-icon" aria-hidden="true">03</span><span class="shortcut-label">Erben &amp; vererben</span><span aria-hidden="true">↗</span></a><a href="@@notarinnen/"><span class="shortcut-label">Alle notariellen Anliegen</span><span aria-hidden="true">↗</span></a></aside></div><div class="digital-meta"><span>Silke Christmann &amp; Hannah-Silvia Heise</span><span>Haardtring 369 · Darmstadt</span><span>Beratung · Notariat · Mediation</span></div></div></section>'''

for key,css,hero,filename in [
    ('02-Editorial-Bordeaux','editorial.css',editorial_hero,'02-Editorial-Bordeaux.html'),
    ('03-Klar-Kobaltblau','digital.css',digital_hero,'03-Klar-Kobaltblau.html')]:
    dest=projects/key
    if dest.exists():shutil.rmtree(dest)
    shutil.copytree(SOURCE,dest,ignore=shutil.ignore_patterns('__pycache__'))
    style=dest/'assets/site.css'
    style.write_text(style.read_text()+'\n'+(ROOT/css).read_text())
    build=dest/'scripts/build.py'
    text=build.read_text()
    injection='\n# Design variant: preserve content; change the home layout.\nimport re\nsections = re.findall(r"<section\\b.*?</section>", home, re.S)\n'
    if key.startswith('02'):
        injection+='home = '+repr(hero)+' + sections[2] + sections[1] + sections[3] + sections[4]\n'
    else:
        injection+='home = '+repr(hero)+' + "<div class=\\\"intro-strip\\\"><div class=\\\"wrap\\\"><span>Rechtliche Beratung</span><span>Notarielle Gestaltung</span><span>Einvernehmliche Konfliktlösung</span></div></div>" + "".join(sections[1:])\n'
    target="layout('', 'Rechtsanwältinnen & Notarinnen in Darmstadt'"
    assert target in text
    text=text.replace(target,injection+'\n'+target,1)
    # Match browser chrome colour to the design rather than the base theme.
    text=text.replace('content="#454d44"','content="'+('#692d3d' if key.startswith('02') else '#234ad4')+'"')
    build.write_text(text)
    note='\n\nDesignalternative '+key+'. Gleiche Inhalte wie Variante 1; andere Typografie, Farbe und Anordnung. Markenfarben und Originalbilder sind weiterhin unbestätigt.\n'
    (dest/'README.md').write_text((dest/'README.md').read_text()+note)
    subprocess.run(['python3',str(build)],check=True)
    shutil.copyfile(dest/'Christmann-Heise-Vorschau.html',ROOT/filename)

# Keep a complete untouched source snapshot for variant 1 too.
base=projects/'01-Ruhig-Salbei'
if base.exists():shutil.rmtree(base)
shutil.copytree(SOURCE,base,ignore=shutil.ignore_patterns('__pycache__'))
(ROOT/'varianten.json').write_text(json.dumps({
    'date':'2026-10-24',
    'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
    'variants':[
      {'file':'01-Ruhig-Salbei.html','name':'Ruhig · Salbei','description':'Bestehender Entwurf, unverändert. Serifenschrift, Architekturillustration und Anliegenraster.'},
      {'file':'02-Editorial-Bordeaux.html','name':'Editorial · Bordeaux','description':'Große Serifentypografie, zentrierter Einstieg, Partnerinnen vor den Anliegen, listenartige Themenführung.'},
      {'file':'03-Klar-Kobaltblau.html','name':'Klar · Kobaltblau','description':'Serifenlose Typografie, blauer Einstieg, direkter Anliegenzugang und klar gegliederte Karten.'}
    ],
    'limitations':['Originalbilder und Logo noch nicht verfügbar','Farben sind Designvorschläge, nicht verifizierte Markenfarben','Rechtstexte und Kontaktdaten vor Veröffentlichung prüfen','Keine Veröffentlichung oder Domainänderung']
},ensure_ascii=False,indent=2))
print('Original erhalten; zwei vollständige Designalternativen erstellt.')
