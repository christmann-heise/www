# Übergabe an www-ch

## Auftrag und Ziel

Der Nutzer möchte christmann-heise.de modernisieren und auf GitHub Pages übertragen. Notara-Formulare sollen über einen echten Kanzleilink eingebunden werden; eine direkte Einbettung wurde mangels bestätigter Anleitung nicht umgesetzt. Am 26.10.2026 wurde ausdrücklich die Übergabe von Inhalt und bisheriger Arbeit an das Projekt `www-ch` beauftragt. Das gefundene zugehörige private Website-Repository ist `christmann-heise/www`; es war zu Beginn leer.

Das ist eine Datei- und Arbeitsstandsübergabe. Der gesamte Chat wurde nicht in einen anderen ChatGPT-Projektchat verschoben. Eine solche Projektchat-Verwaltungsfunktion stand in dieser Sitzung nicht zur Verfügung.

## Nutzerwünsche und Entscheidungen

- Kanzlei: Christmann & Heise, Rechtsanwältinnen in Partnerschaft und Notarinnen, Darmstadt.
- Persönliche, seriöse und vertrauenswürdige Wirkung. Berufsbezeichnungen korrekt weiblich; keine erfundenen Qualifikationen.
- Bestehenden ersten Entwurf erhalten und zwei echte Designalternativen erstellen. Noch keine endgültige Designwahl.
- Der Nutzer wünscht konkrete Umsetzung, eine nutzbare Vorschau und selbstständige Bearbeitung statt wiederholter Downloadanweisungen.
- Bestehende Websiteidentität berücksichtigen. Farben der vorliegenden Entwürfe sind Vorschläge, keine nachgewiesene Übernahme der alten Markenfarben.

## Gelieferte Arbeit

14 Seiten je Variante: Startseite, Rechtsanwältinnen, Notarinnen, fünf notarielle Themenseiten, Mediation, Terminvorbereitung, Kontakt, Impressum, Datenschutz und 404. Zusätzlich 404.html als Kopie für statisches Hosting.

Die bekannten Hauptpfade wurden erhalten: `/`, `/rechtsanwaeltinnen/`, `/notarinnen/`, `/mediatorin/`, `/kontakt/`, `/impressum/`, `/datenschutz/`.

Statische Umsetzung mit HTML, lokalem CSS/JavaScript und Python-Build ohne externe Pakete. Keine Analysewerkzeuge, keine automatisch geladene externe Karte, kein Kontaktformular-Backend. Kontakt über Telefon/E-Mail und externe Route erst auf Klick. Mobiles Menü, Fokusmarkierung, Sprunglink und reduzierte Bewegung wurden im Code berücksichtigt.

### Die drei Designs

1. `01-Ruhig-Salbei.html`: erste Fassung unverändert, Serifenschrift, abstrakte Architekturillustration und Anliegenraster.
2. `02-Editorial-Bordeaux.html`: große zentrierte Serifentypografie, Partnerinnen früher im Seitenaufbau, Themen als Liste.
3. `03-Klar-Kobaltblau.html`: serifenlose Typografie, blauer Einstieg, direkter Anliegenzugang und Karten.

Der Designvergleich ist eine eigenständige HTML-Datei mit allen drei HTML-Seitenständen, Umschaltung Desktop/Mobil und einem eingebetteten ZIP des damaligen Quellstands. Der aktuelle Quellstand steht zusätzlich direkt im Repository. Der Originalentwurf hat SHA-256 `b90ad109ee794a5137bd17856cc8b64ac039420a319d740061ad95c047e1a4c8`; die übergebene Vergleichsdatei hat SHA-256 `b08148d6e446b0f3690242da38277426c06296132ff8226a83bfe5ff176f15da`.

## Was aus der bisherigen Website übernommen wurde

Die Textinhalte und Seitenstruktur konnten über den Recherchezugriff gelesen werden, teilweise aus indexierten Fassungen. Die vollständige visuelle Darstellung wurde nicht geprüft.

- Kanzleiname, Berufsbezeichnungen, Namen und Tätigkeitsschwerpunkte.
- Silke Christmann als Fachanwältin für Miet- und Wohnungseigentumsrecht.
- Hannah-Silvia Heise als Rechtsanwältin, Notarin und Mediatorin. Sie wurde nicht als Fachanwältin bezeichnet.
- Inhalte zur Mediation, gekürzt und paraphrasiert.
- Anschrift Haardtring 369, 64295 Darmstadt, E-Mail-Adresse und Parkplatzhinweis.
- Telefonnummer der Kontaktseite: 06151 3921 2000, noch zu bestätigen.

Neu sind Layout, Startseitentexte, Anliegenführung, Terminvorbereitung und abstrakte Architekturillustration. Die Illustration zeigt kein Kanzleigebäude. Initialenfelder ersetzen vorläufig fehlende Porträtdateien. Keine Stockfotos oder künstlich erzeugten Personen wurden als Kanzleipersonal verwendet.

## Fehlendes Originalmaterial

Direkte Abrufe von HTML/Bildern scheiterten in dieser Sitzung mit HTTP 403; der Recherchezugriff auf Bildadressen teilweise mit HTTP 401. Es ist damit keine vollständige Original-Sicherung erfolgt.

Bekannte Porträtadressen:

- Silke Christmann: `https://christmann-heise.de/wp-content/uploads/2018/08/RechtsanwaeltinnenSC-e1534960103594.jpg`
- Hannah-Silvia Heise: `https://christmann-heise.de/wp-content/uploads/2018/08/RechtsanwaeltinnenHH-e1534960135173.jpg`

Nachladeskript: `christmann-heise/scripts/fetch-originals.py`. In einer Umgebung mit Zugriff erneut ausführen; Logo und Farben anhand der tatsächlichen Dateien prüfen. Nicht behaupten, die Originalbilder seien bereits gesichert. Das Skript ist kein vollständiges WordPress-Backup.

## Vorschauproblem und Korrektur bisheriger Aussagen

Die Vergleichsdatei ist außerdem in ChatGPT gespeichert: `libfile_7d653231e7608191a5fdace60e3bf5c1`, bisher Version 0. Link: https://chatgpt.com/library?file_id=libfile_7d653231e7608191a5fdace60e3bf5c1&account_id=847d7eb7-8183-432c-852f-126f95119556

Der Nutzer zeigte im Desktop-Webbrowser die Meldung „Die Codeausführung ist für diesen Workspace deaktiviert“. In der Mobil-App funktionierte dieselbe Vorschau laut Nutzer. Die genaue Ursache wurde nicht ermittelt. Daraus darf weder eine allgemeine Dateisperre noch eine allgemeine Unmöglichkeit der Vorschau abgeleitet werden. Browser-/Workspace-Unterschiede sind mögliche, unbestätigte Erklärungen.

Es wurde kein externer Browser auf dem PC des Nutzers geöffnet. In dieser Sitzung fehlte die lokale Browsersteuerung; die im Plugin-Katalog gefundene zusätzliche Cloud-Browser-Integration war administrativ gesperrt. Das beweist nicht, dass jede Browserintegration oder jede andere Sitzung gesperrt ist.

Ein normaler, direkt nutzbarer Vorschau-Weblink ist der nächste sinnvolle Lieferschritt. Die GitHub-Dateiansicht und der ChatGPT-Dateilink sind keine bestätigte Ersatzlösung für diesen Wunsch.

## Prüfungen

- Builds aller drei Varianten erfolgreich.
- Je 14 eingebettete Seitenrouten vorhanden.
- 45 generierte HTML-Dateien einschließlich drei 404-Kopien auf lokale Linkziele und Sprungmarken geprüft: keine fehlenden Ziele.
- Je Seite genau eine H1.
- Syntax der Vorschau-/Vergleichsskripte geprüft.
- Erste Fassung per Bytevergleich unverändert erhalten.
- Produktionsbuild ohne Freigaben wird gesperrt.
- Keine visuelle Browserprüfung: Browser war nicht installiert, Browserdownload blockiert. Keine bestätigten Lighthouse-/Accessibility-Ergebnisse. Keine Notara-Übermittlung getestet.

## Vor Veröffentlichung zu klären

1. Design auswählen; Original-Logo, Fotos und tatsächliche Markenfarbe übernehmen.
2. Telefonnummer bestätigen: Kontaktseite nennt `06151 3921 2000`, bisheriges Impressum `06151/3921200`.
3. Vollständiges aktuelles Impressum und Datenschutzerklärung erstellen/freigeben. Bisheriges Impressum enthält alte TMG-/RStV-Verweise und widersprüchliche Adressangaben. Datenschutz lieferte nur den Shortcode `[avalex_de_datenschutz]`. Entwurfsseiten nicht ungeprüft veröffentlichen.
4. Individuellen Notara-Link bestätigen und in `site.json` unter `notara_url` hinterlegen. Ohne Link führen die entsprechenden Wege zum Kanzleikontakt. Keine URL eines anderen Notariats verwenden.
5. GitHub-Pages-Verfügbarkeit für das private Repository und Nutzungsbedingungen zur kommerziellen Verwendung prüfen. Die technische statische Eignung ist keine pauschale Bestätigung der Nutzungszulässigkeit. Alternativ denselben `dist`-Ordner bei passendem statischem Hosting bereitstellen.
6. Zuerst separate Vorschau-URL bereitstellen und prüfen. Danach vollständige Bestands-URL-/Medieninventur, fachliche Freigabe und Domainumstellung behandeln. Mail-DNS erhalten. In dieser Übergabe wurde nichts veröffentlicht.

## Fortsetzungsanweisung für das Projekt

Den Stand direkt übernehmen und an den vorhandenen Dateien weiterarbeiten. Keine erneute Neuerstellung der drei Designs erforderlich. Zuerst eine im externen Browser nutzbare Vorschau unter einer separaten URL ermöglichen und Desktop/Mobil visuell prüfen. Variante 1 als Referenz erhalten. Tatsächliche Ergebnisse und verbleibende Grenzen benennen. Bestehende Domain und E-Mail-Konfiguration bis zur abgestimmten Umstellung erhalten.
