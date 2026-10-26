# Christmann & Heise – Website-Entwurf

Erste statische Neufassung für die Migration von christmann-heise.de. Stand: 24.10.2026. Nicht veröffentlicht. Original-Domain und DNS wurden nicht geändert.

## Vorschau

`Christmann-Heise-Vorschau.html` direkt öffnen. Für alle Seiten zusammen:

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory dist
```

Dann http://localhost:8000 aufrufen. Python 3.10 oder neuer, keine Paketinstallation erforderlich. Alternativ den Inhalt von `dist/` auf einem beliebigen statischen Vorschauhosting bereitstellen.

## Enthalten

- Responsive Startseite, anwaltliche Profile, Notarinnen, fünf notarielle Themenseiten, Mediation, Terminvorbereitung und Kontakt.
- Bestehende Hauptpfade bleiben erhalten: `/rechtsanwaeltinnen/`, `/notarinnen/`, `/mediatorin/`, `/kontakt/`, `/impressum/`, `/datenschutz/`.
- Bedienung per Tastatur, sichtbare Fokusmarkierung, Sprunglink, mobiles Menü, reduzierte Bewegung, lokale Systemschriften.
- Echte Kontaktlinks und externe Routenplanung erst auf Klick. Keine Analysewerkzeuge oder externen Skripte.
- Notara konfigurierbar in `site.json`. Ohne verifizierte URL öffnet die Terminvorbereitung den Kanzleikontakt; es wird kein fremdes Notariat verlinkt.
- Sitemap, 404, Vorschauschutz per noindex und manuell auslösbarer GitHub-Pages-Workflow.

## Originalmaterial und Grenzen

Texte und Original-Porträtadressen wurden aus den öffentlich abrufbaren Seiten erfasst. Der Download von HTML, Bildern und Stylesheets scheiterte in dieser Umgebung mit HTTP 403; der Recherchezugriff auf die Bildadressen mit HTTP 401. Deshalb sind die Porträts noch nicht als Bilddateien enthalten. Es wurden keine Ersatzpersonen oder Stockfotos verwendet. Die Initialenflächen sind ein temporärer Ersatz. Die abstrakte Architekturillustration ist neu erstellt und zeigt kein Gebäude der Kanzlei.

Die vorhandene Markenfarbe und das Original-Logo konnten nicht verifiziert werden. Die Vorschau verwendet daher vorläufige, zurückhaltende Graphit-, Salbei- und Cremetöne sowie eine textliche Namensdarstellung. Dies ist keine Bestätigung der bestehenden Corporate Identity.

Zum Nachladen der Originale in einer Umgebung mit Zugriff:

```sh
python3 scripts/fetch-originals.py
python3 scripts/build.py
```

Das Skript sichert die sieben Hauptseiten, die beiden bekannten Porträts und gefundene lokale Bild- und Stylesheetressourcen. Verzeichnisse und SHA-256-Werte stehen in `sources/download-manifest.json`. CSS-Hintergrundbilder, dynamische Inhalte, Downloads und weitere Unterseiten müssen nach erfolgreichem Abruf zusätzlich inventarisiert werden. Eine vollständige Sicherung der bestehenden WordPress-Installation ist dies nicht.

## Freigabe und GitHub Pages

Siehe `docs/UEBERGABE.md`. Die Vorschau enthält unvollständige, ausdrücklich als Entwurf markierte Rechtstexte. Sie darf in diesem Stand nicht als produktive Kanzleiseite veröffentlicht werden. Der Produktionsbuild sperrt solange Markenmaterial, Kontaktdaten, Hosting und Rechtstexte nicht bestätigt sind.

```sh
python3 scripts/build.py --production
```

Der Workflow ist ausschließlich manuell auslösbar und baut die Vorschau. Das Ziel-Repository wurde noch nicht festgelegt. Es wurde kein vorhandenes fremdes Projekt geändert. `CNAME` wird nur beim freigegebenen Produktionsbuild erstellt. Den Domainumzug und die E-Mail-DNS-Einträge getrennt behandeln.


Designalternative 03-Klar-Kobaltblau. Gleiche Inhalte wie Variante 1; andere Typografie, Farbe und Anordnung. Markenfarben und Originalbilder sind weiterhin unbestätigt.
