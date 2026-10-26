# Hugo-Varianten und öffentliche Sicherheitsprüfung

## Beauftragter Umfang

Hugo ist die Zieltechnik. Die drei bisherigen Entwürfe bleiben unverändert. Hinzu kommen vier echte Hugo-Projekte mit jeweils denselben sieben Originalseiten: Original/Vortex (4), Arcana (5), Agnes (6), Blunix (7). Keine Theme-Demotexte, Beispielfirmen, Beispielpreise oder zusätzlichen Leistungsseiten werden ausgegeben. Firmenname, Impressum und Haftungsangaben bleiben unverändert.

## Herkunft

| Variante | Herkunft | Fester Stand |
|---|---|---|
| 4 | archiviertes WordPress-Theme Vortex 1.0.3 von 2Theme, mit Bootstrap 3.3.7 | gesicherte Originalseiten und Stylesheets unter `archive-original/` |
| 5 | https://github.com/half-duplex/hugo-arcana | `20ee7d0ada2c5bc14941f4e36e8e355c536256f9` |
| 6 | https://github.com/dchucks/agnes-hugo-theme | `daed40f54b75eb617ff4dfcd3f6d6977ed652f51` |
| 7 | https://github.com/Blunix-GmbH/hugo-theme-blunix | `b6f8c12dc47042362e2a28af54d344459eeafb8a` |

Theme-Quellen und Lizenzen liegen unter `hugo/themes/`. Beispiele und nicht benötigte Demo-Inhalte wurden nicht in die Ausgabe übernommen. Die thematischen Layouts sind nur dort angepasst, wo die unveränderten Originaltexte, die echte Kanzleibezeichnung, die vorhandene Navigation und die relative GitHub-Pages-Adresse eingebunden werden müssen. Arcana behält den sichtbaren HTML5-UP-/Theme-Herkunftshinweis.

Die Website wird mit Hugo 0.168.0 gebaut. Arcana benötigt Dart Sass; festgelegt ist 1.106.1. Die Werkzeuge werden im Workflow anhand festgelegter SHA-256-Werte geprüft. Themes und Styles liegen lokal im Repository; der Inhaltsbuild ruft keine Quellen nach. Theme-Schriftdateien werden lokal ausgeliefert.

## Inhaltstreue

`scripts/build-original.py` passt technische Ressourcen- und Vorschaupfade an, formuliert aber keine Inhalte neu. `scripts/prepare-hugo.py` übernimmt daraus die sieben Seiten in die vier Hugo-Projekte. `scripts/build-site.py` erzeugt die veröffentlichbare Ausgabe unter `public/`.

`scripts/verify-site.py` vergleicht die vollständigen Haupttexte und Überschriften aller 28 Hugo-Seiten mit den gesicherten Originalseiten. Das schließt das gesamte Impressum und die dort enthaltenen Haftungsangaben ein. Die beiden Tests prüfen einen gültigen Build und die Erkennung einer absichtlich verfälschten Firmenbezeichnung im Impressum.

Die gestalterischen Varianten 5–7 ändern die Darstellung; der Hauptinhalt bleibt identisch. Keine allgemeine Aussage, dass jeder historische Bildschirm pixelgenau rekonstruiert wurde.

## Unvermeidbare Archivgrenzen

- Die Originalseiten stammen aus unterschiedlichen belegten Archivzeitpunkten zwischen Dezember 2025 und Februar 2026. Die aktuelle Originaldomain konnte nicht als vollständige Live-Vorlage abgerufen werden.
- Mehrere Originalporträts, ein Hintergrundbild und zusätzliche Plugin-Stylesheets fehlen im Archiv. Fehlende Bilder werden nicht durch neue oder fremde Bilder ersetzt. `christmann-heise-designs/04-Original/missing-assets.json` nennt die fehlenden Quellen. Deshalb ist der Nachbau trotz identischer Texte und originaler Hauptgestaltung visuell nicht vollständig.
- Die kleinen im Originalheader verlinkten Dateien sowie die Landespreisgrafik konnten gesichert werden und bleiben dort, wo das Original sie verwendet. Die kleinen Headerdateien werden nicht als vollständiges Kanzleilogo ausgegeben.
- Die Datenschutzquelle enthält lediglich `[avalex_de_datenschutz]`; ein vollständiger nachgeladener Rechtstext ist nicht archiviert. Es wurde kein neuer Text erfunden.
- Original-Kontaktdaten und rechtliche Angaben werden nicht eigenständig aktualisiert, auch bei widersprüchlichen Quellenangaben.

## Vorschaufunktionen

Das ursprüngliche WordPress-Kontaktformular bleibt sichtbar, übermittelt in keiner Vorschau jedoch Daten. Der Vorschaucode unterbindet die Übermittlung, bevor ein Netzaufruf erfolgt. Ein WordPress-Backend wird nicht vorgetäuscht. Die originale Kartenfläche bleibt ohne erfundene Karteninhalte; die optionale Maps-Initialisierung wird bei fehlender API technisch übersprungen.

Variante 4 erhält die öffentliche originale Notara-Widget-Einbindung. Es wurde keine Anmeldung durchgeführt und kein Formular an Notara gesendet. Analyse-/Werbeskripte und reCAPTCHA aus der historischen WordPress-Seite werden in der Vorschau nicht aktiviert. Der originale Cookiehinweis bleibt auf der separat geöffneten Originalvariante erhalten und wird nur im geschützten Vergleichsrahmen ausgelassen, wo Cookiezugriff technisch gesperrt ist. Diese Anpassungen betreffen den Vorschau-Betrieb, nicht die Originaltexte oder die unveränderten Archivbelege.

## Notara und Geheimnisprüfung

Die gesicherte Notara-Einbindung enthält eine öffentliche Notarkennung (`notaryId`), den Modus `popup` und Farben/Beschriftungen. Kein Passwort, kein Login-Token und kein geheimer API-Schlüssel wurde darin gefunden. Das öffentlich abrufbare Widget-Skript erwartet eine Notarkennung im Konstruktor, keine Passwortübergabe. Öffentliche Anbieterquelle: https://app.notara.de/js/notary-datasheet-widget.js .

Die erste Prüfung umfasste alle sechs damals vorhandenen Commits, 61 unterschiedliche Git-Dateiinhalte, drei eingebettete HTML-Dokumente und 110 Dateien im eingebetteten ZIP-Archiv; keine erkennbaren Geheimnisse gefunden. Die erneute Prüfung schließt auch die neuen Dateien ein. Das wiederholbare Werkzeug `scripts/check-public-secrets.py` gibt bei Treffern nur Dateiposition und Regelname aus, niemals den gefundenen Wert. Es prüft erkennbare Passwort-/Schlüsselzuweisungen, Provider-Token, private Schlüssel, JWT, Bearer-Zugangswerte und Passwörter in URLs.

Diese Musterprüfung ist kein vollständiges Sicherheitsgutachten und keine Prüfung des Notara-Backends. Öffentlich eingebettete Anbieterkennungen und reCAPTCHA-Site-Keys sind nicht mit geheimen Serverzugängen gleichzusetzen. Es werden keine Zugangswerte gegen fremde Dienste getestet.

## Durchgeführte Prüfungen

- Vier erfolgreiche lokale Hugo-Builds.
- 28 Originalseiten im Inhaltsvergleich identisch; vollständiges Impressum einbezogen.
- Positiver und negativer Test der Inhaltsprüfung bestanden.
- Edge-Browser: alle sieben Auswahloptionen und Mobilumschaltung, alle neuen Originalseiten erreichbar, keine JavaScript-Seitenfehler nach der Korrektur des Cookiehinweises im Vergleichsrahmen.
- Neue Startseiten bei 1440px und 390px geprüft; kein horizontaler Überlauf bei 390px.
- Vorschauformulare aller vier Hugo-Varianten auf ausbleibende Übermittlung geprüft.
- Historische Quellarchiv-Dateien bleiben unverändert erhalten. Ein eingebettetes früheres Downloadarchiv ist als früherer Quellstand bezeichnet; aktuelle Hugo-Quellen sind direkt im Repository.

Remote-Build und Pages-Veröffentlichung werden zusätzlich am tatsächlich gepushten Commit geprüft. Ein lokaler Build allein gilt nicht als Veröffentlichungsnachweis.
