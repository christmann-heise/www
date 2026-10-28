# Wiederherstellung der Original-Symbolschrift

Die fünf Informationssymbole auf `/rechtsanwaeltinnen/` erschienen als Ziffer `0`.
Die archivierte CSS-Datei ordnet `icon-basic-info` diesem Zeichen in der
Symbolschrift `linea-basic-10` zu. Die CSS-Datei war vorhanden, ihre relativen
Schriftdateien unter `../fonts/` fehlten jedoch. Derselbe Fehler betraf das
Symbol `icon-basic-message-multiple` auf `/mediatorin/`.

## Herkunft und Abgrenzung

Die vier unveränderten Schriftdateien stammen aus dem offiziellen
[Linea-Iconset](https://github.com/linea-io/Linea-Iconset/tree/8ecf784f58326ae288ec0db364cd5b2ed55109c4/_basic/_ICONFONT/fonts),
festgehalten auf Commit `8ecf784f58326ae288ec0db364cd5b2ed55109c4`.
Alle 135 Symbolzuordnungen im zugehörigen Upstream-Stylesheet stimmen mit der
archivierten Website-CSS-Datei überein. Diese Wiederherstellung verwendete den
belegten Originalzeichensatz; die nachfolgend dokumentierte Nutzerentscheidung
ändert anschließend ausschließlich die fünf Rechtsgebietssymbole.

### Nachprüfung: Informationssymbol oder Paragraphenzeichen?

Die zunächst offene Frage nach der tatsächlich ausgelieferten Originalschrift
konnte in einer weiteren Recherche geklärt werden. Über die Availability-API
des Internet Archive wurden zwei konkrete Schriftaufnahmen gefunden und direkt
abgerufen:

- [Original-WOFF vom 24.02.2019](https://web.archive.org/web/20190224074414id_/https://christmann-heise.de/wp-content/themes/vortex/assets/fonts/linea-basic-10.woff).
- [Original-WOFF vom 20.02.2026](https://web.archive.org/web/20260220141528id_/https://christmann-heise.de/wp-content/themes/vortex/assets/fonts/linea-basic-10.woff).

Beide Antworten enthalten eine gültige WOFF-Datei mit 12.260 Bytes. Beide Dateien
sind bytegenau identisch mit der wiederhergestellten WOFF-Datei; die gemeinsame
SHA-256-Prüfsumme lautet
`3f660cf145f6ee7ae270ea3f8e737b2353c7978c1b0de1b5d97684ddd0673db9`.
Damit ist das Informationssymbol „i im Kreis“ durch die damals ausgelieferten
Schriftdateien belegt. Ein Paragraphenzeichen ist für diese gesicherten Stände
nicht belegt. Die spätere Änderung zu `§` beruht deshalb auf einem ausdrücklichen
Nutzerauftrag und wird nicht als Originalrekonstruktion ausgegeben.

Die unveränderten Archivantworten liegen separat unter `archive-original/`.
Der direkte Fontvergleich ersetzt keinen historischen Screenshot einer ganzen
Seite; die Schrift- und Seitenaufnahmen stammen aus unterschiedlichen Zeitpunkten.

Zusätzlich wurde die [Seitenaufnahme vom 20.08.2019](https://web.archive.org/web/20190820122214id_/https://christmann-heise.de/rechtsanwaeltinnen/)
gesichert. Dieser ältere Stand verwendet sechs Mal `icon-basic-info`, enthält
sechs Rechtsgebiete einschließlich Familienrecht und hat eine andere Anordnung
als der bisher maßgebliche Seitenstand vom Dezember 2025. Diese historischen
Inhaltsunterschiede werden ausschließlich dokumentiert und nicht in die heutige
Website übernommen. Eine erhaltene lokale Website-Kopie bestätigt dagegen die
fünf Informationssymbole und die Anordnung des Dezember-2025-Stands; sie enthält
keine Schriftdateien und keinen historischen Screenshot dieses Abschnitts.

Quelladressen und SHA-256-Prüfsummen stehen in
`ORIGINAL-SYMBOLE-2026-10-28.json`. Das Upstream-Stylesheet liegt unverändert in
`original-icons/upstream-styles.css`, die Upstream-Lizenz unverändert neben den
Schriftdateien als `fonts/LICENSE.txt`.

## Ausdrückliche Nutzerentscheidung: § statt i

Am 28.10.2026 beauftragte der Nutzer nach der Quellenklärung: „mach ein update
und ersetze das i durch §“. Die fünf Informationssymbole auf
`/rechtsanwaeltinnen/` werden deshalb durch das Paragraphenzeichen in Dosis
ersetzt. Das ist eine bewusste Abweichung vom belegten Original. Texte, Farben
und die Anordnung der Rechtsgebiete bleiben unverändert; das Sprechblasensymbol
auf `/mediatorin/` bleibt erhalten.

Die Änderung liegt separat in `shared/requested-legal-symbols.css`. Der Build
bindet diese Datei ausschließlich auf Rechtsanwältinnen ein. Die archivierten
HTML-, CSS- und Schriftdateien werden nicht verändert. Die Entscheidung ist
auch in `AGENTS.md` festgehalten, damit spätere Originalabgleiche sie erhalten.

## Einbindung und Prüfung

- Die archivierte Website-CSS-Datei, die HTML-Texte und die Anordnung bleiben unverändert.
- Hugo bindet das lokale Original-Schriftverzeichnis als `static/fonts` ein.
  Damit funktionieren die bestehenden relativen CSS-Verweise sowohl auf der
  Hauptseite als auch unter der Vorschau `03-Original` und unter einem Projektpfad.
- `scripts/verify-site.py` prüft beide Ausgabeorte auf die referenzierten
  Schriftdateien und ihre belegten Prüfsummen. Ein fehlendes WOFF wird im
  Regressionstest absichtlich erzeugt und muss zurückgewiesen werden.
- `scripts/verify-original-icons.cjs` prüft mit Playwright die fünf Paragraphenzeichen
  in Dosis und das unveränderte Originalsymbol auf Mediatorin auf Desktop und
  Mobilgerät, jeweils auf Hauptseite und Vorschau. Externe Aufrufe und
  Formularübermittlungen sind dabei gesperrt. Ein zusätzlicher Browserlauf mit
  absichtlich blockierter Symbolschrift muss den ursprünglichen Fehler erkennen;
  eine weitere Gegenprobe ohne die gewünschte CSS-Abweichung muss die Rückkehr
  zum Informationssymbol erkennen.
- Browseraufruf bei vorhandenem Playwright: `node scripts/verify-original-icons.cjs`.
  Eine Veröffentlichung kann zusätzlich mit `--base-url https://christmann-heise.de/`
  geprüft werden; `--directory` wählt einen separaten lokalen Build-Ordner.
  Unter Windows kann `BROWSER_CHANNEL=msedge` verwendet werden.
  Screenshots und Laufberichte werden lokal unter `preview-review/linea-icons/`
  abgelegt und nicht als Website veröffentlicht.
