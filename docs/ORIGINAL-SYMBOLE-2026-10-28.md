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
archivierten Website-CSS-Datei überein. Es werden keine neuen Symbole entworfen
oder andere Zeichensätze verwendet.

Ein binärer Vergleich mit der damals von der Website ausgelieferten Schriftdatei
ist nicht belegt: Der Wayback-Abruf war bei dieser Prüfung nicht erreichbar.
Belegt sind die archivierte Schriftreferenz, der identische Schriftname und
sämtliche 135 identischen Symbolzuordnungen des offiziellen Projekts.

Quelladressen und SHA-256-Prüfsummen stehen in
`ORIGINAL-SYMBOLE-2026-10-28.json`. Das Upstream-Stylesheet liegt unverändert in
`original-icons/upstream-styles.css`, die Upstream-Lizenz unverändert neben den
Schriftdateien als `fonts/LICENSE.txt`.

## Einbindung und Prüfung

- Die archivierte Website-CSS-Datei, die HTML-Texte und die Anordnung bleiben unverändert.
- Hugo bindet das lokale Original-Schriftverzeichnis als `static/fonts` ein.
  Damit funktionieren die bestehenden relativen CSS-Verweise sowohl auf der
  Hauptseite als auch unter der Vorschau `03-Original` und unter einem Projektpfad.
- `scripts/verify-site.py` prüft beide Ausgabeorte auf die referenzierten
  Schriftdateien und ihre belegten Prüfsummen. Ein fehlendes WOFF wird im
  Regressionstest absichtlich erzeugt und muss zurückgewiesen werden.
- `scripts/verify-original-icons.cjs` prüft mit Playwright die tatsächlich
  gerenderte Symbolschrift aller sechs betroffenen Symbole auf Desktop und
  Mobilgerät, jeweils auf Hauptseite und Vorschau. Externe Aufrufe und
  Formularübermittlungen sind dabei gesperrt. Ein zusätzlicher Browserlauf mit
  absichtlich blockierter Symbolschrift muss den ursprünglichen Fehler erkennen.
- Browseraufruf bei vorhandenem Playwright: `node scripts/verify-original-icons.cjs`.
  Eine Veröffentlichung kann zusätzlich mit `--base-url https://christmann-heise.de/`
  geprüft werden. Unter Windows kann `BROWSER_CHANNEL=msedge` verwendet werden.
  Screenshots und Laufberichte werden lokal unter `preview-review/linea-icons/`
  abgelegt und nicht als Website veröffentlicht.
