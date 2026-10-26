# Korrektur der Originaltypografie und der Porträts

Die frühere Gestaltungsprüfung kontrollierte überwiegend den Schriftnamen Dosis.
Das reichte nicht: Die Entwürfe und Themes bestimmten weiterhin Schriftgrößen,
Zeichenabstände, Großschreibung und einzelne Schriftstärken. Im Blunix-Layout war
zusätzlich die Theme-Klasse `font-nunito` am Seitentext gesetzt.

Die gemeinsame Gestaltung übernimmt nun auch die belegten typografischen Regeln
aus `archive-original/template.min.css`, `archive-original/extra-styles.css` und
`archive-original/inline-site-styles.css`. Dazu gehören die responsiven Titel mit
weit auseinanderstehenden Großbuchstaben, normale Überschriften, Navigation,
Fließtext, Profilbeschreibungen und Libre Baskerville kursiv für Zitate. Die
verschiedenen Theme-Aufbauten bleiben erhalten. Originaltexte werden nicht geändert.

In Vorschau 1 und 2 waren Bilder lediglich im anfänglichen HTML ersetzt worden.
Die Navigation überschrieb diesen Inhalt sofort mit HTML aus einem eingebetteten
JSON-Objekt, das noch Initialen als Platzhalter enthielt. Der Build verarbeitet
jetzt dieses JSON als Daten und ersetzt die Bilder im tatsächlich verwendeten
Seiteninhalt. Auf der Rechtsanwältinnen-Seite werden die dafür gesicherten
Originalbilder verwendet. Die Porträts bleiben auch beim Rücksprung zur Startseite
sichtbar. Die beiden älteren Vorschauen behalten ihren dokumentierten Entwurfsstatus.

## Prüfung

`scripts/verify-browser.cjs` vergleicht die tatsächlich berechnete Typografie jedes
Textelements der sieben archivierten Inhaltsseiten in Arcana, Agnes und Blunix
mit dem Originalnachbau. Geprüft werden Schriftfamilie, Größe, Stärke, Stil,
Zeichenabstand, Zeilenhöhe, Großschreibung und Textfarbe, jeweils bei 1440 und
390 Pixeln Breite. Die tatsächlich gerenderten Dosis- und Libre-Baskerville-Schriften
werden zusätzlich über die Browser-Schnittstelle kontrolliert. Navigation und
Bildanzeige nach Seitenwechseln in Vorschau 1 und 2 sind ebenfalls Bestandteil.

Lokaler Durchlauf mit Microsoft Edge: 58 erfolgreiche Seiten-/Navigationsprüfungen,
keine typografischen Abweichungen, keine JavaScript-Seitenfehler, kein horizontaler
Überlauf in den geprüften Vorschauen. Ergebnis:
`TYPOGRAFIE-PRUEFUNG-2026-10-26.json`. Die Prüfung sendet keine Formulare ab.

Die vorhandenen Inhaltsprüfungen vergleichen weiterhin alle 28 Hugo-Seiten mit
den archivierten Originaltexten. Ein zusätzlicher Regressionstest prüft die
Porträts in den Navigationsdaten beider älteren Vorschauen anhand der Prüfsummen
der gesicherten Originalbilder.

Die lokale Prüfung bestätigt die Korrektur vor der Veröffentlichung. Die
Übernahme nach `main` erfolgt gemäß aktivem Repository-Schutz über einen Pull
Request mit erfolgreichem Build und der vorgeschriebenen zustimmenden Prüfung.
