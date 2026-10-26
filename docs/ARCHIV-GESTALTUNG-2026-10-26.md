# Originalgestaltung und unveränderte Inhalte

Recherche: 26.10.2026. Ziel: belegte Originalgestaltung sichern und die bestehende Website möglichst genau übernehmen. Keine neue inhaltliche Konzeption.

Aktualisierung: In einer erhaltenen früheren Website-Sicherung wurden inzwischen die fünf Originalporträts gefunden und unverändert übernommen. Belege: `ORIGINALBILDER-2026-10-26.json`. Es sind keine Screenshot-Ersatzbilder erforderlich. Die nachfolgend dokumentierten ersten fehlgeschlagenen Archivabrufe bleiben als Recherchehistorie erhalten. Aktueller Umsetzungsstand: `HUGO-VARIANTEN-2026-10-26.md`.

## Maßgebliche Nutzeranweisung

Keine erfundenen Inhalte, keine neuen Seiten oder Ideen. Firmenname, Impressum und Haftungsangaben bleiben unverändert. Quellenkonflikte werden dokumentiert und nicht eigenständig entschieden. Die bisherigen drei Varianten sind Gestaltungsvorschauen und keine freigegebene Originalübernahme.

## Gesicherte Quellen

Die Startseite wurde vollständig als HTML-Quelltext aus dem Internet Archive abgerufen:

- Original: https://christmann-heise.de/
- Archivstand: https://web.archive.org/web/20260113002325id_/https://christmann-heise.de/
- Sicherung: `archive-original/startseite-2026-01-13.html.txt`.

Sechs weitere Originalseiten wurden erfolgreich gesichert: Rechtsanwältinnen, Notarinnen, Mediatorin, Kontakt, Impressum und Datenschutz. `archive-original/pages-manifest.json` nennt jeweils die tatsächlich ausgelieferte Archivadresse, Datum, Status und SHA-256. Die Archivstände liegen zwischen Dezember 2025 und Februar 2026; sie bilden ausdrücklich keinen zeitgleichen Komplettsnapshot.

Die derzeitige Originaldomain lieferte beim direkten Abruf HTTP 401. Historische Quellen werden deshalb nicht als bestätigter aktueller Kanzleistand ausgegeben.

## VERIFIED: konkrete Gestaltung aus dem Originalquelltext

| Element | Originalwert | Beleg |
|---|---|---|
| Grundschrift, Überschriften, Navigation, Formulare, Schaltflächen | Dosis, normal, Gewicht 400 | Inline-CSS der Startseite |
| Zitate / `.font-serif` | Libre Baskerville, kursiv, Gewicht 400 | Inline-CSS der Startseite |
| Markenakzent / Überschriften | `#7a3674` | Marken-CSS und eigenes Überschriften-CSS |
| Marken-Schaltflächen bei Hover/Fokus | `#682e63` | `.btn.btn-brand:hover` und `:focus` |
| Links | `rgba(122, 54, 116, .6)` | Inline-CSS |
| Links bei Hover/Fokus | `#572652` | Inline-CSS |
| Grundfläche | `#fff` | Vortex-Template-CSS |
| Grundtext | `#777`, 14px, Zeilenhöhe 1.8 | Vortex-Template-CSS; rollenbezogene Abweichungen möglich |
| Themenbasis | WordPress-Theme Vortex 1.0.3 | archiviertes `style.css` |

Die Grundschrift aus dem allgemeinen Theme ist Open Sans; die konkreten Inline-Einstellungen der Kanzlei überschreiben sie mit Dosis. Der auskommentierte Open-Sans-Block im eigenen CSS ist keine aktive Schriftvorgabe. WordPress-Standardpaletten im Quelltext sind keine nachgewiesenen Kanzleifarben.

Gesicherte Stylesheets:

- `inline-site-styles.css`: relevante Original-Inline-Regeln aus dem Startseiten-Snapshot, ohne redaktionelle Neufassung.
- `theme-style.css`: https://web.archive.org/web/20250708200643id_/https://christmann-heise.de/wp-content/themes/vortex/style.css
- `template.min.css`: https://web.archive.org/web/20260220141533id_/https://christmann-heise.de/wp-content/themes/vortex/assets/css/template.min.css
- `extra-styles.css`: https://web.archive.org/web/20250708200550id_/https://christmann-heise.de/wp-content/themes/vortex/includes/additional-sources/static/css/extra-styles.css

## VERIFIED: Seiten und Bezeichnungen

Die archivierte Navigation nennt Startseite, Rechtsanwältinnen, Notarinnen, Mediatorin und Kontakt. Im Footer sind Impressum und Datenschutz verlinkt. Dies ist die belegte Navigationsstruktur, keine Behauptung über eine vollständige historische URL-Inventur.

Auf der Originalstartseite stehen die drei Zeilen:

- Christmann & Heise
- Rechtsanwältinnen in Partnerschaft
- Notarinnen

Das Impressum verwendet die Bezeichnung „Christmann und Heise – Rechtsanwältinnen in Partnerschaft“. Die Schreibweisen werden in ihrem jeweiligen Kontext erhalten und nicht durch eine selbst erfundene einheitliche Firmenbezeichnung ersetzt.

Im Impressum sind unter anderem die Berufshaftpflichtversicherung, der räumliche Versicherungsschutz und die Aussage zur Verbraucherschlichtung enthalten. Maßgeblich bleibt der gesicherte vollständige Originaltext; diese Recherche liefert keine neue Rechtsfassung.

## OPEN: fehlendes Material und Quellenkonflikte

- Die archivierten Dateien `additional-logo.png` und `blind.png` wurden abgerufen und visuell geprüft. Sie zeigen nur ein kleines „V“ bzw. eine winzige Markierung. Sie belegen kein verwendbares Kanzleilogo und werden nicht als solches übernommen.
- Die beiden im Original genannten Porträt-URLs lieferten beim ersten Archivabruf 404. Die Bilder sind damit noch nicht gesichert.
- Auf der Datenschutzseite steht im gesicherten HTML lediglich `[avalex_de_datenschutz]`. Der vollständige nachgeladene Text ist damit nicht belegt. Keine Datenschutzerklärung erfinden oder aus dem Shortcode ableiten.
- Kontaktseite und Impressum enthalten unterschiedlich geschriebene Telefonnummern; das Impressum nennt außerdem im Abschnitt zur redaktionellen Verantwortung eine andere Adresse. Originaltexte unverändert erhalten, Konflikte nicht eigenständig korrigieren.
- Im Startseiten-Quelltext ist eine Notara-Einbindung mit Kennung `1499` und Widget-Farbe `#7a3674` enthalten. Dies ist ein historischer Quellenfund, keine Bestätigung der heutigen Kennung oder Freigabe einer Übermittlung.
- Keine formale eigenständige Styleguide-Datei gefunden. Die oben genannten Gestaltungswerte sind direkt aus der tatsächlich eingesetzten Website abgeleitet.
- Die gesamte historische Darstellung ist noch nicht vollständig rekonstruiert. Archivdateien können aus verschiedenen Zeitpunkten stammen.

## Konsequenz für die Fortsetzung

Salbei, Bordeaux und Kobaltblau sind bisherige Entwurfsvorschläge. Für die originalnahe neue Fassung sind die belegten violetten Akzente und Dosis maßgeblich. Originalseiten und Originaltexte werden zuerst gegen die gesicherten Quellen abgeglichen. Keine zusätzlichen Themenseiten, Werbeaussagen oder neuen Leistungsbeschreibungen ohne ausdrücklichen Auftrag. Die drei vorhandenen Entwürfe bleiben als bisheriger Arbeitsstand erhalten.

## Vorschauprüfung

Die Pages-Startseite verlinkt den Vergleich und alle drei Einzelvorschauen. Alle vier Vorschauadressen lieferten HTTP 200. Im lokalen Edge-Browser wurden die drei Umschaltungen und die Mobilansicht mit 390px geprüft; keine JavaScript-Seitenfehler. Die mobile Übersichtsseite zeigte keinen horizontalen Überlauf. Diese Prüfung belegt die Vorschaufunktion, keine inhaltliche Freigabe und keine vollständige Barrierefreiheitsprüfung.
