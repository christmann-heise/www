#!/usr/bin/env python3
"""Build a dependency-free static site. Python 3.10+, no external packages."""
from pathlib import Path
from html import escape as esc
from urllib.parse import urlparse
import argparse, json, shutil, sys

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'site.json').read_text())
OUT = ROOT / 'dist'
PRODUCTION = '--production' in sys.argv
if PRODUCTION:
    required = ['brand_verified', 'legal_reviewed', 'contact_verified', 'hosting_confirmed']
    missing = [key for key in required if CFG.get(key) is not True]
    missing += [str(p) for p in ['assets/christmann.jpg','assets/heise.jpg','assets/logo.svg'] if not (ROOT / p).is_file()]
    if missing:
        sys.exit('Produktionsbuild gesperrt. Offen: ' + ', '.join(missing))
NOTARA = CFG.get('notara_url', '').strip()
if NOTARA and (urlparse(NOTARA).scheme != 'https' or urlparse(NOTARA).hostname not in ('app.notara.de', 'notara.de')):
    sys.exit('notara_url muss eine bestätigte HTTPS-Adresse von notara.de oder app.notara.de sein.')
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'assets', OUT / 'assets')

NAV = [('rechtsanwaeltinnen/','Rechtsanwältinnen'),('notarinnen/','Notarinnen'),('mediatorin/','Mediation'),('kontakt/','Kontakt')]
PAGES = []

def layout(slug, title, description, body):
    depth = len([p for p in slug.split('/') if p])
    prefix = '../' * depth if depth else './'
    def url(path=''): return prefix + path
    current = slug.split('/')[0]
    links = ''.join(f'<a href="{url(p)}"' + (' aria-current="page"' if p.split('/')[0]==current else '') + (' class="nav-contact"' if p=='kontakt/' else '') + f'>{label}</a>' for p,label in NAV)
    mark = ('<img class="original-logo" src="'+url('assets/logo.svg')+'" alt="Christmann &amp; Heise – Rechtsanwältinnen &amp; Notarinnen">') if (ROOT/'assets/logo.svg').is_file() else '<strong>Christmann &amp; Heise</strong><small>Rechtsanwältinnen &amp; Notarinnen</small>'
    canonical = CFG['domain'].rstrip('/') + '/' + slug
    robots = 'index, follow' if PRODUCTION else 'noindex, nofollow'
    html = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} | Christmann &amp; Heise</title><meta name="description" content="{esc(description)}"><meta name="robots" content="{robots}"><meta name="theme-color" content="#234ad4"><meta property="og:title" content="{esc(title)} | Christmann &amp; Heise"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="website"><meta property="og:locale" content="de_DE"><meta property="og:url" content="{canonical}"><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="{url('assets/site.css')}"><script src="{url('assets/site.js')}" defer></script></head>
<body><a class="skip" href="#inhalt">Zum Inhalt springen</a><div class="topline"><div class="wrap"><span>Darmstadt <span class="location-short">· persönlich für Sie da</span></span><a href="tel:+49615139212000">06151 3921 2000</a></div></div>
<header class="site-header"><div class="wrap header-inner"><a class="wordmark" href="{url()}" aria-label="Christmann und Heise – Startseite">{mark}</a><button class="menu-button" type="button" aria-expanded="false" aria-controls="navigation">Menü</button><nav class="nav" id="navigation" aria-label="Hauptnavigation">{links}</nav></div></header>
<main id="inhalt" tabindex="-1">{body.replace('@@', prefix)}</main>
<footer class="footer"><div class="wrap"><div class="footer-top"><a class="wordmark" href="{url()}">{mark}</a><div class="footer-links"><a href="{url('kontakt/')}">Kontakt &amp; Anfahrt</a><a href="{url('impressum/')}">Impressum</a><a href="{url('datenschutz/')}">Datenschutz</a></div></div><div class="footer-bottom"><span>Christmann &amp; Heise · Rechtsanwältinnen in Partnerschaft · Notarinnen</span><span>Haardtring 369 · 64295 Darmstadt</span></div></div></footer>
<div class="mobile-cta" aria-label="Schneller Kontakt"><a href="tel:+49615139212000">Anrufen</a><a href="{url('termin-vorbereiten/')}">Termin vorbereiten</a></div></body></html>'''
    path = OUT / slug / 'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html)
    PAGES.append(slug)

def button(text, target, primary=True):
    return f'<a class="button{" primary" if primary else ""}" href="{esc(target, quote=True)}">{text}<span class="arrow" aria-hidden="true">↗</span></a>'

def heading(label,title,intro):
    return f'<section class="page-heading"><div class="wrap"><div class="breadcrumb"><a href="@@">Startseite</a> / {label}</div><p class="eyebrow">Christmann &amp; Heise · Darmstadt</p><h1>{title}</h1><p class="lead">{intro}</p></div></section>'

def portrait(key, name, initials):
    if (ROOT / f'assets/{key}.jpg').is_file():
        return f'<div class="portrait"><img src="@@assets/{key}.jpg" alt="{name}" width="500" height="650" loading="lazy"></div>'
    # Typographic fallback; never request an unavailable remote image from a visitor's browser.
    return f'<div class="portrait" role="img" aria-label="{name}"><span class="portrait-letter" aria-hidden="true">{initials}</span></div>'

PEOPLE = [
 ('christmann','Silke Christmann','SC','Rechtsanwältin &amp; Notarin','Fachanwältin für Miet- und Wohnungseigentumsrecht','Miet- und Wohnungseigentumsrecht, allgemeines Zivilrecht und Betreuungsrecht. Notarielle Schwerpunkte: Grundstücks- und Immobilienrecht sowie Handels- und Gesellschaftsrecht.'),
 ('heise','Hannah-Silvia Heise','HH','Rechtsanwältin &amp; Notarin · Mediatorin','','Familienrecht, Erbrecht und Betreuungsrecht. Notarielle Schwerpunkte: Erbrecht, Familienrecht und Vorsorge. Weitere Tätigkeiten: Mediation und Testamentsvollstreckung.')
]

def person_cards():
    return '<div class="people">'+''.join(f'<article class="person">{portrait(key,name,initials)}<div><h3>{name}</h3><p class="role">{role}</p><p>{special or "Familienrecht · Erbrecht · Mediation"}</p><a class="text-link" href="@@rechtsanwaeltinnen/#{key}">Persönliches Profil ↗</a></div></article>' for key,name,initials,role,special,desc in PEOPLE)+'</div>'

TOPICS = [
 ('immobilien','Immobilie kaufen &amp; übertragen','Kauf, Schenkung und Übertragung von Grundbesitz.','Immobilien'),
 ('vorsorge','Vorsorge regeln','General- und Vorsorgevollmacht, Betreuungs- und Patientenverfügung.','Vorsorge'),
 ('erben','Erben &amp; vererben','Testament, Erbvertrag und Nachlassgestaltung.','Erbrecht'),
 ('gesellschaft','Unternehmen gestalten','Gründung, Gesellschaftsverträge und Registerangelegenheiten.','Gesellschaftsrecht'),
 ('familie','Familie &amp; Partnerschaft','Ehevertrag und Vereinbarungen für gemeinsame Lebenswege.','Familienrecht'),
 ('mediation','Konflikte gemeinsam lösen','Mediation für Familie, Erbschaft und Zusammenarbeit.','Mediation')
]

def topics():
    return '<div class="topic-grid">'+''.join(f'<a class="topic" href="@@{("mediatorin/" if key=="mediation" else "notarinnen/"+key+"/")}"><span class="number">0{i+1} / {label}</span><h3>{title}</h3><div class="topic-bottom"><p>{desc}</p><span class="arrow" aria-hidden="true">↗</span></div></a>' for i,(key,title,desc,label) in enumerate(TOPICS))+'</div>'

def contact_section():
    return '''<section class="section contact-section"><div class="wrap contact-grid"><div class="contact-copy"><p class="eyebrow">Der erste Schritt ist ein Gespräch</p><h2>Was dürfen wir<br>für Sie klären?</h2><p>Beschreiben Sie uns Ihr Anliegen. Gemeinsam klären wir, wer Sie unterstützt und wie es weitergeht.</p><a class="text-link" href="@@kontakt/">Kontakt &amp; Anfahrt ↗</a></div><div class="contact-card"><h3>Wir freuen uns auf Sie.</h3><address>Christmann &amp; Heise<br>Haardtring 369<br>64295 Darmstadt</address><div class="contact-links"><a href="tel:+49615139212000">06151 3921 2000</a><a href="mailto:kanzlei@christmann-heise.de">kanzlei@christmann-heise.de</a></div><p>Mandantenparkplätze stehen Ihnen direkt an der Kanzlei zur Verfügung.</p></div></div></section>'''

home = '''<section class="hero"><div class="wrap hero-grid"><div><p class="eyebrow">Rechtsanwältinnen &amp; Notarinnen in Darmstadt</p><h1>Wichtige Fragen.<br>Persönlich <em>geklärt.</em></h1><p class="lead">Manche Entscheidungen brauchen einen klaren Blick und ein vertrauensvolles Gespräch. Wir begleiten Sie mit rechtlicher Erfahrung und Zeit für Ihr Anliegen.</p><div class="actions">'''+button('Notartermin vorbereiten','@@termin-vorbereiten/')+button('Anwaltliche Beratung','@@rechtsanwaeltinnen/',False)+'''</div><p class="hero-note">Silke Christmann &amp; Hannah-Silvia Heise · <a href="@@kontakt/">Haardtring 369, Darmstadt</a></p></div><div class="hero-art"><img src="@@assets/architecture.svg" width="500" height="440" alt="" fetchpriority="high"><span class="art-caption">Klarheit. Vertrauen. Perspektive.</span></div></div></section>
<div class="intro-strip"><div class="wrap"><span>Rechtliche Beratung</span><span>Notarielle Gestaltung</span><span>Einvernehmliche Konfliktlösung</span></div></div>
<section class="section"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Ihr Anliegen im Mittelpunkt</p><h2>Was möchten Sie regeln?</h2></div><p>Ein guter Anfang: der passende Weg zu Ihrer Frage.</p></div>'''+topics()+'''</div></section>
<section class="section about-section"><div class="wrap"><div class="about-intro"><div><p class="eyebrow">Die Menschen hinter der Kanzlei</p><h2>Zwei Perspektiven.<br>Ein persönlicher Anspruch.</h2></div><p>Seit der Gründung im Jahr 2011 beraten wir private und unternehmerische Mandantschaft in Darmstadt. Im persönlichen Gespräch entwickeln wir Lösungen, die zu Ihrer Situation passen.</p></div>'''+person_cards()+'''</div></section>
<section class="section"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Gut vorbereitet</p><h2>Ihr Weg zum Notartermin.</h2></div><a class="text-link" href="@@termin-vorbereiten/">Zur Terminvorbereitung ↗</a></div><div class="steps"><article class="step"><span>01</span><h3>Anliegen schildern</h3><p>Teilen Sie uns mit, was Sie regeln möchten und wer beteiligt ist.</p></article><article class="step"><span>02</span><h3>Unterlagen abstimmen</h3><p>Wir klären mit Ihnen, welche Angaben und Dokumente für Ihren Vorgang gebraucht werden.</p></article><article class="step"><span>03</span><h3>Persönlich besprechen</h3><p>Offene Fragen besprechen wir gemeinsam und stimmen die nächsten Schritte ab.</p></article></div></div></section>'''+contact_section()

# Design variant: preserve content; change the home layout.
import re
sections = re.findall(r"<section\b.*?</section>", home, re.S)
home = '<section class="digital-hero"><div class="wrap"><div class="digital-grid"><div><p class="eyebrow">Rechtsanwältinnen &amp; Notarinnen in Darmstadt</p><h1>Wichtige Fragen.<br><span>Persönlich geklärt.</span></h1><p class="lead">Manche Entscheidungen brauchen einen klaren Blick und ein vertrauensvolles Gespräch. Wir begleiten Sie mit rechtlicher Erfahrung und Zeit für Ihr Anliegen.</p><div class="actions"><a class="button primary" href="@@termin-vorbereiten/">Notartermin vorbereiten <span aria-hidden="true">↗</span></a><a class="button" href="@@rechtsanwaeltinnen/">Anwaltliche Beratung <span aria-hidden="true">↗</span></a></div></div><aside class="quick-panel" aria-label="Direkt zu Ihrem Anliegen"><p class="eyebrow">Ihr Anliegen</p><h2>Wo dürfen wir helfen?</h2><a href="@@notarinnen/immobilien/"><span class="shortcut-icon" aria-hidden="true">01</span><span class="shortcut-label">Immobilie kaufen &amp; übertragen</span><span aria-hidden="true">↗</span></a><a href="@@notarinnen/vorsorge/"><span class="shortcut-icon" aria-hidden="true">02</span><span class="shortcut-label">Vorsorge regeln</span><span aria-hidden="true">↗</span></a><a href="@@notarinnen/erben/"><span class="shortcut-icon" aria-hidden="true">03</span><span class="shortcut-label">Erben &amp; vererben</span><span aria-hidden="true">↗</span></a><a href="@@notarinnen/"><span class="shortcut-label">Alle notariellen Anliegen</span><span aria-hidden="true">↗</span></a></aside></div><div class="digital-meta"><span>Silke Christmann &amp; Hannah-Silvia Heise</span><span>Haardtring 369 · Darmstadt</span><span>Beratung · Notariat · Mediation</span></div></div></section>' + "<div class=\"intro-strip\"><div class=\"wrap\"><span>Rechtliche Beratung</span><span>Notarielle Gestaltung</span><span>Einvernehmliche Konfliktlösung</span></div></div>" + "".join(sections[1:])

layout('', 'Rechtsanwältinnen & Notarinnen in Darmstadt', 'Christmann & Heise in Darmstadt: Rechtsanwältinnen, Notarinnen und Mediation. Persönliche Beratung, Kontakt und Vorbereitung Ihres Notartermins.', home)

profiles = heading('Rechtsanwältinnen','Erfahrung trifft<br>persönliche Beratung.','Silke Christmann und Hannah-Silvia Heise unterstützen private und unternehmerische Mandantschaft mit unterschiedlichen fachlichen Schwerpunkten.')
profiles += '<section class="section"><div class="wrap">'
for key,name,initials,role,special,desc in PEOPLE:
    profiles += f'<article class="profile-full" id="{key}">{portrait(key,name,initials)}<div class="prose"><p class="eyebrow">{role}</p><h2>{name}</h2>'+ (f'<h3>{special}</h3>' if special else '')+f'<p>{desc}</p><p>Welcher Weg für Ihr Anliegen passt, klären wir gerne im persönlichen Gespräch.</p>'+button('Beratung anfragen','@@kontakt/')+'</div></article>'
profiles += '</div></section>'+contact_section()
layout('rechtsanwaeltinnen/','Rechtsanwältinnen', 'Die Rechtsanwältinnen Silke Christmann und Hannah-Silvia Heise: persönliche Profile und fachliche Schwerpunkte in Darmstadt.',profiles)

layout('notarinnen/','Notarinnen', 'Notarinnen Silke Christmann und Hannah-Silvia Heise in Darmstadt: Immobilien, Vorsorge, Erbrecht, Gesellschaftsrecht und Familie.',heading('Notarinnen','Heute Klarheit schaffen.<br>Für das, was kommt.','Wir stehen Ihnen für Beurkundungen, Beglaubigungen und weitere notarielle Tätigkeiten zur Verfügung. Hier finden Sie den Einstieg zu Ihrem Anliegen.')+'<section class="section"><div class="wrap">'+topics()+'</div></section>'+contact_section())

TOPIC_COPY = {
 'immobilien':('Immobilien sind persönliche Entscheidungen.','Ob Sie ein Haus kaufen, eine Wohnung übertragen oder eine Schenkung planen: Wir begleiten die notarielle Gestaltung Ihres Vorhabens.','Welche Immobilie ist betroffen? Wer ist beteiligt? Gibt es bereits Unterlagen zu Ihrem Vorhaben?'),
 'vorsorge':('Den eigenen Willen frühzeitig festhalten.','Wir unterstützen Sie bei General- und Vorsorgevollmachten sowie Betreuungs- und Patientenverfügungen. Ihre persönliche Situation steht dabei im Mittelpunkt.','Welche Regelungen wünschen Sie? Wer soll Sie unterstützen können? Gibt es bereits bestehende Dokumente?'),
 'erben':('Persönliche Wünsche klar gestalten.','Testament und Erbvertrag bieten Möglichkeiten, die eigene Nachfolge zu gestalten. Wir besprechen Ihre Vorstellungen und die dazu passende notarielle Regelung.','Wer gehört zu Ihrer Familie? Welche Wünsche haben Sie für die Nachfolge? Bestehen bereits letztwillige Verfügungen?'),
 'gesellschaft':('Eine gute Grundlage für Ihr Unternehmen.','Wir begleiten notarielle Vorgänge im Handels- und Gesellschaftsrecht, etwa bei Gründung und gesellschaftsrechtlichen Veränderungen.','Was möchten Sie gründen oder verändern? Wer ist beteiligt? Welche Gesellschaftsunterlagen liegen vor?'),
 'familie':('Gemeinsame Lebenswege bewusst regeln.','Wir besprechen mit Ihnen notarielle Vereinbarungen für Ehe und Partnerschaft und begleiten die Gestaltung Ihrer persönlichen Regelungen.','Was möchten Sie miteinander vereinbaren? Welche bestehende Regelung soll berücksichtigt werden?')
}
for key,title,desc,label in TOPICS[:-1]:
    sub,copy,prep = TOPIC_COPY[key]
    body = heading(label,title,desc)+f'<section class="section"><div class="wrap content-grid"><div class="prose"><h2>{sub}</h2><p>{copy}</p><h2>Vor dem ersten Gespräch</h2><p>{prep}</p><p>Welche Unterlagen konkret benötigt werden, stimmen wir individuell mit Ihnen ab.</p><a class="backlink" href="@@notarinnen/">← Alle notariellen Anliegen</a></div><aside class="side-note"><p class="eyebrow">Ihr nächster Schritt</p><h2>Sprechen wir darüber.</h2><p>Schildern Sie uns Ihr Anliegen und vereinbaren Sie mit uns das weitere Vorgehen.</p>'+button('Termin vorbereiten','@@termin-vorbereiten/')+'</aside></div></section>'
    layout('notarinnen/'+key+'/',label+' · Notarinnen',desc.replace('&amp;','&'),body)

mediation = heading('Mediation','Gemeinsam wieder<br>ins Gespräch kommen.','Hannah-Silvia Heise begleitet Sie als Mediatorin auf dem Weg zu einer selbstbestimmten, einvernehmlichen Lösung.')+'''<section class="section"><div class="wrap content-grid"><div class="prose"><h2>Raum für neue Perspektiven.</h2><p>In einem vertrauensvollen Rahmen können alle Beteiligten ihren Konflikt und dessen Hintergründe besprechen. Ziel ist eine gemeinsame, konkrete Vereinbarung.</p><h2>Anlässe für eine Mediation</h2><ul><li>Familienkonflikte, Trennung und Scheidung</li><li>Sorge, Umgang und Unterhalt</li><li>Vermögens- und Hausratsaufteilung</li><li>Erbschaftsstreitigkeiten</li><li>Konflikte im Betrieb oder im Team</li></ul><p>Voraussetzung sind Gesprächsbereitschaft und der Wille aller Beteiligten, eine einvernehmliche Lösung zu suchen.</p></div><aside class="side-note"><p class="eyebrow">Ihre Ansprechpartnerin</p><h2>Hannah-Silvia Heise</h2><p>Rechtsanwältin &amp; Notarin<br>Mediatorin</p>'''+button('Gespräch anfragen','@@kontakt/')+'</aside></div></section>'
layout('mediatorin/','Mediation', 'Mediation in Darmstadt mit Hannah-Silvia Heise: gemeinsam Lösungen für familiäre, erbrechtliche und betriebliche Konflikte finden.',mediation)

notara_block = '<div class="service-banner"><div><h3>Ihr Anliegen online vorbereiten.</h3><p>Über unsere digitalen Datenblätter bei Notara.</p></div>'+button('Datenblatt bei Notara öffnen',NOTARA,False)+'</div>' if NOTARA else '<div class="service-banner"><div><h3>Wir helfen Ihnen beim Einstieg.</h3><p>Kontaktieren Sie uns für die passende Vorbereitung Ihres Vorgangs.</p></div>'+button('Kanzlei kontaktieren','@@kontakt/',False)+'</div>'
prepare = heading('Termin vorbereiten','Ein guter Termin beginnt<br>mit guter Vorbereitung.','Schildern Sie uns Ihr Vorhaben. Gemeinsam stimmen wir ab, welche Informationen wir benötigen und wie es weitergeht.')+'<section class="section"><div class="wrap"><div class="steps"><article class="step"><span>01</span><h3>Ihr Vorhaben</h3><p>Was möchten Sie regeln? Wer ist beteiligt? Bestehen bereits Vereinbarungen?</p></article><article class="step"><span>02</span><h3>Ihre Unterlagen</h3><p>Halten Sie vorhandene Dokumente bereit. Die konkrete Zusammenstellung klären wir mit Ihnen.</p></article><article class="step"><span>03</span><h3>Ihr Kontakt</h3><p>Rufen Sie uns an. Wir besprechen die Vorbereitung und vereinbaren das weitere Vorgehen.</p></article></div>'+notara_block+'''<div class="details-list"><details><summary>Welche Unterlagen werden benötigt?</summary><p>Das hängt von Ihrem Anliegen ab. Wir teilen Ihnen mit, welche Angaben und Dokumente für die Vorbereitung Ihres Vorgangs erforderlich sind.</p></details><details><summary>Wie vereinbare ich einen Termin?</summary><p>Sie erreichen uns telefonisch unter <a href="tel:+49615139212000">06151 3921 2000</a> oder per E-Mail an <a href="mailto:kanzlei@christmann-heise.de">kanzlei@christmann-heise.de</a>.</p></details></div></div></section>'''
layout('termin-vorbereiten/','Notartermin vorbereiten','Bereiten Sie Ihren Notartermin bei Christmann & Heise in Darmstadt vor. Informationen zu Anliegen, Unterlagen und Kontakt.',prepare)

layout('kontakt/','Kontakt & Anfahrt','Christmann & Heise, Haardtring 369, 64295 Darmstadt. Telefon, E-Mail und Informationen zur Anfahrt.',heading('Kontakt','Wir freuen uns<br>auf Ihr Anliegen.','Persönlich erreichbar in Darmstadt. Vereinbaren Sie Ihren Termin mit unserer Kanzlei.')+contact_section()+'''<section class="section"><div class="wrap prose"><h2>Ihre Anfahrt</h2><p>Haardtring 369, 64295 Darmstadt. Mandantenparkplätze befinden sich direkt an der Kanzlei.</p><a class="button" href="https://www.google.com/maps/search/?api=1&amp;query=Haardtring+369+64295+Darmstadt" rel="noopener noreferrer" target="_blank">Route in Google Maps öffnen ↗</a><p>Die Karte öffnet sich erst nach Ihrem Klick auf einer externen Website.</p></div></section>''')

legal = heading('Impressum','Impressum','Angaben zur Kanzlei.')+'''<section class="section"><div class="wrap prose"><div class="draft-note">Entwurfsstand: Die rechtlichen Angaben müssen vor Veröffentlichung von der Kanzlei aktualisiert und freigegeben werden. Dies ist keine veröffentlichungsfertige Fassung.</div><h2>Christmann und Heise</h2><p>Rechtsanwältinnen in Partnerschaft<br>Haardtring 369<br>64295 Darmstadt<br>kanzlei@christmann-heise.de</p><h2>Partnerinnen</h2><p>Silke Christmann, Rechtsanwältin und Notarin<br>Hannah-Silvia Heise, Rechtsanwältin und Notarin</p><h2>Register</h2><p>Sitz: Darmstadt<br>Partnerschaftsregister des Amtsgerichts Frankfurt am Main<br>Registernummer: PR 2000</p><p>Diese Angaben stammen aus dem bestehenden Internetauftritt. Die vollständigen Berufs-, Aufsichts-, Versicherungs- und Verantwortlichkeitsangaben sind vor Veröffentlichung zu aktualisieren.</p><a href="https://christmann-heise.de/impressum/">Bisheriges Impressum aufrufen (bestehende Website)</a></div></section>'''
layout('impressum/','Impressum','Entwurfsstand der rechtlichen Angaben von Christmann und Heise.',legal)
privacy = heading('Datenschutz','Datenschutz','Informationen zum Datenschutz.')+'''<section class="section"><div class="wrap prose"><div class="draft-note">Entwurfsstand: Die Datenschutzhinweise für das endgültige Hosting und die aktivierten Dienste müssen vor Veröffentlichung erstellt und freigegeben werden.</div><h2>Stand der Vorschau</h2><p>Diese Fassung lädt Schriften, Gestaltung und Skripte lokal. Sie enthält keine eingebettete Karte, keine Analysewerkzeuge und kein Kontaktformular. Externe Websites werden über Links aufgerufen.</p><h2>Vor Veröffentlichung zu ergänzen</h2><p>Verantwortliche, Hosting und Zugriffsprotokolle, Kontaktaufnahme, Betroffenenrechte und gegebenenfalls Notara. Diese Erläuterung ersetzt keine vollständige Datenschutzerklärung.</p></div></section>'''
layout('datenschutz/','Datenschutz','Entwurfsstand der Datenschutzinformationen für den neuen Internetauftritt.',privacy)
layout('404/','Seite nicht gefunden','Die gewünschte Seite konnte nicht gefunden werden.',heading('Seite nicht gefunden','Hier geht es weiter.','Die gesuchte Seite ist unter dieser Adresse nicht verfügbar.')+'<section class="section"><div class="wrap">'+button('Zur Startseite','@@')+'</div></section>')
# A project Pages 404 needs repository-relative URLs rather than assuming a root domain.
shutil.copyfile(OUT/'404/index.html',OUT/'404.html')
text = (OUT/'404.html').read_text().replace('../','./')
(OUT/'404.html').write_text(text)
(OUT/'.nojekyll').touch()
(OUT/'robots.txt').write_text('User-agent: *\n'+('Allow: /\nSitemap: '+CFG['domain']+'/sitemap.xml\n' if PRODUCTION else 'Disallow: /\n'))
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+CFG['domain']+'/'+s+'</loc></url>' for s in PAGES if s!='404/')+'</urlset>')
if PRODUCTION: (OUT/'CNAME').write_text(urlparse(CFG['domain']).hostname+'\n')
# Portable, self-contained start page for direct opening without a local server.
preview = (OUT/'index.html').read_text()
preview = preview.replace('<link rel="stylesheet" href="./assets/site.css">','<style>'+(ROOT/'assets/site.css').read_text()+'</style>')
preview = preview.replace('<script src="./assets/site.js" defer></script>','')
preview = preview.replace('</body>','<script>'+(ROOT/'assets/site.js').read_text()+'</script></body>')
import base64, re
for path in sorted((ROOT/'assets').iterdir()):
    if path.suffix in ('.svg','.jpg','.png'):
        mime = {'.svg':'image/svg+xml','.jpg':'image/jpeg','.png':'image/png'}[path.suffix]
        preview = preview.replace('./assets/'+path.name,'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode())
# Make all pages usable inside one portable preview without a server.
from urllib.parse import urljoin, urlsplit
def portable(text, slug):
    def local_link(match):
        raw = match[1]
        u = urlsplit(raw)
        if u.scheme or u.netloc or raw.startswith('data:'): return match[0]
        resolved = urlsplit(urljoin('https://preview.local/'+slug,raw))
        return 'href="#'+resolved.path+('#'+resolved.fragment if resolved.fragment else '')+'"'
    text = re.sub(r'href="([^"]*)"', local_link, text)
    for asset in (ROOT/'assets').iterdir():
        if asset.suffix not in ('.jpg','.png','.svg'): continue
        mime={'.svg':'image/svg+xml','.jpg':'image/jpeg','.png':'image/png'}[asset.suffix]
        text=re.sub(r'src="(?:\.\./|\./)*assets/'+re.escape(asset.name)+'"','src="data:'+mime+';base64,'+base64.b64encode(asset.read_bytes()).decode()+'"',text)
    return text
preview = portable(preview, '')
routes = {}
for slug in PAGES:
    raw = (OUT/slug/'index.html').read_text()
    routes['/'+slug]={'html':portable(re.search(r'<main[^>]*>(.*?)</main>',raw,re.S)[1],slug),'title':re.search(r'<title>(.*?)</title>',raw)[1]}
route_js = '''<script>
const previewRoutes=ROUTES;
function showPreviewRoute(){
 const bits=(location.hash.slice(1)||'/').split('#');
 const route=previewRoutes[bits[0]];
 if(!route)return;
 document.querySelector('main').innerHTML=route.html;
 const decoder=document.createElement('textarea');decoder.innerHTML=route.title;document.title=decoder.value;
 document.querySelectorAll('#navigation a').forEach(a=>{if(a.getAttribute('href')==='#'+bits[0])a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
 if(bits[1])requestAnimationFrame(()=>document.getElementById(bits[1])?.scrollIntoView());else window.scrollTo(0,0);
}
window.addEventListener('hashchange',showPreviewRoute);showPreviewRoute();
</script>'''.replace('ROUTES',json.dumps(routes,ensure_ascii=False).replace('</','<\\/'))
preview=preview.replace('</body>',route_js+'</body>')
(ROOT/'Christmann-Heise-Vorschau.html').write_text(preview)
print(f'{len(PAGES)} Seiten erstellt: {OUT}. Modus: '+('Produktion' if PRODUCTION else 'Vorschau (noindex)'))
