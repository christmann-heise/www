# Umsetzungsstand und Übergabe

## Bereits umgesetzt

14 statische Seiten einschließlich 404, gemeinsame Gestaltung und Navigation, mobil nutzbarer Kontakt, Anliegenstruktur, persönliche Profile, Terminvorbereitung, konfigurierbarer Notara-Einstieg und lokaler Build ohne zusätzliche Pakete. Bestehende Hauptpfade wurden berücksichtigt. Die Angaben zu Tätigkeiten wurden aus den bestehenden Kanzleiseiten paraphrasiert; neue fachliche Zusicherungen oder Qualifikationen wurden nicht ergänzt.

## Vor Produktionsfreigabe offen

1. Original-Logo, Bilddateien und Markenfarbe nachladen und visuell prüfen. Bekannte URLs stehen in `sources/inventar.json`. Das Original-Logo wird nach Prüfung als `assets/logo.svg` abgelegt und dann automatisch im Kopf-/Fußbereich eingebunden. Logo-Proportionen und Kontrast im dunklen Fußbereich kontrollieren. Ein SVG vor Verwendung auf aktive Inhalte prüfen. Nach dem Nachladen der Porträts übernimmt der Build sie automatisch.
2. Kanzleitelefon bestätigen: Kontaktseite nennt **06151 3921 2000**, Impressum nennt **06151/3921200**. Der Entwurf verwendet die Kontaktseite. Keine Öffnungszeiten erfunden.
3. Impressum vollständig aktualisieren. Die Quelle enthält unter anderem alte Verweise auf TMG und RStV, eine vom Kanzleisitz abweichende redaktionelle Anschrift und Versicherungs-/Aufsichtsangaben, deren Aktualität unbestätigt ist. Originaltext nicht ungeprüft übernehmen. Die Entwurfsseite muss durch eine vollständige freigegebene Fassung ersetzt werden.
4. Datenschutzerklärung beschaffen und auf die tatsächliche Architektur anpassen. Der abrufbare bestehende Inhalt zeigte nur den WordPress-Shortcode `[avalex_de_datenschutz]`; eine vollständige Erklärung konnte daraus nicht übernommen werden. GitHub dokumentiert IP-Protokollierung. Notara als verlinkter Dienst bzw. eingebetteter Dienst gesondert abbilden, je nach endgültiger Umsetzung.
5. Individuelle Notara-URL der Kanzlei bestätigen und in `site.json` unter `notara_url` eintragen. Formularübermittlung, Zustellung, Mobilansicht und Abschlussseite mit Testdaten prüfen. Einbettung ist nicht umgesetzt, da unterstützter Einbettungscode und Freigabe durch Notara fehlen. Linkintegration benötigt keine Formularverarbeitung auf GitHub Pages.
6. Ziel-Repository und Hosting festlegen. Unter dem privaten GitHub-Zugang war kein eindeutig Christmann & Heise zugeordnetes Repository erkennbar. Bestehende notariat8-Projekte wurden nicht verändert. GitHub-Pages-Nutzungsbedingungen zur kommerziellen Nutzung vor Festlegung berücksichtigen. Falls Pages ungeeignet ist, funktioniert derselbe `dist`-Ordner auch bei anderem statischen Hosting.
7. Bestandsinventar vervollständigen: alle vorhandenen URLs, Medien und Downloads erfassen. Auswertungen aus Search Console/Sitemap berücksichtigen, soweit vorhanden. Diesen Entwurf nicht als vollständigen URL-Crawl ansehen. Pfade nach Möglichkeit erhalten. GitHub Pages bietet keine frei konfigurierbaren serverseitigen 301-Regeln; erforderliche HTTP-Weiterleitungen am vorgeschalteten Hosting/CDN lösen.
8. Nach fachlicher und technischer Prüfung die Wahrheitswerte in `site.json` setzen, Produktionsbuild erzeugen und erst dann Domain umstellen. E-Mail-MX-, SPF-, DKIM- und DMARC-Einträge erhalten. Danach Apex/www, HTTPS, Links und E-Mail separat kontrollieren.

## Gestaltungsstand

Vorläufige redaktionelle Gestaltung mit großzügiger Typografie, klaren Wegen nach Anliegen, persönlichen Profilen und ruhiger Farbigkeit. Bestehende Bildsprache und genaue Farbwerte sind noch nicht bewertet. Es ist ein prüfbarer erster Entwurf, keine originalgetreue Übertragung aller Inhalte und Medien.

## Quellen

- https://christmann-heise.de/
- https://christmann-heise.de/rechtsanwaeltinnen/
- https://christmann-heise.de/notarinnen/
- https://christmann-heise.de/mediatorin/
- https://christmann-heise.de/kontakt/
- https://christmann-heise.de/impressum/
- https://christmann-heise.de/datenschutz/
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features

Die Quellen wurden am 24.10.2026 über den Recherchezugriff ausgewertet, teilweise aus zuletzt indexierten Fassungen. Der unmittelbare Liveabruf von Originaldateien war blockiert. Daten daher vor Produktivbetrieb bestätigen.
