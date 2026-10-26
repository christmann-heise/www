# Christmann & Heise · www-ch

Vollständige Übergabe der Website-Arbeit aus der Unterhaltung vom 24.–26. Oktober 2026. Stand: 26.10.2026.

**Hier beginnen:** [Arbeitsstand und Fortsetzung](docs/UEBERGABE-2026-10-26.md).

## Aktueller Hugo-Stand

Zieltechnik ist Hugo. [Vorschauauswahl](https://christmann-heise.github.io/www/) und [Vergleich](https://christmann-heise.github.io/www/christmann-heise-designs/Christmann-Heise-Designvergleich.html) enthalten sechs neu nummerierte Varianten. Der frühere Kobaltblau-Vorschlag ist auf Nutzerwunsch gelöscht:

1. **Ruhig**: bisheriger Aufbau mit Originalschriften, Originalfarben und Notara.
2. **Editorial**: bisheriger Aufbau mit Originalschriften, Originalfarben und Notara.
3. **Original / Archiv**: Hugo-Nachbau mit dem gesicherten Vortex-Design.
4. **Hugo Arcana**: angefragtes Theme mit Originalinhalten.
5. **Hugo Agnes**: angefragtes Theme mit Originalinhalten.
6. **Hugo Blunix**: angefragtes Theme mit Originalinhalten.

Alle sechs verwenden die belegten Originalschriften Dosis und Libre Baskerville kursiv, die Originalfarben und die öffentliche Notara-Einbindung. Die fünf Originalporträts wurden aus einer erhaltenen Website-Sicherung wiederhergestellt; beide Notarinnen-Porträts haben 668 × 1000 Pixel. Jede der vier Hugo-Varianten enthält genau die sieben gesicherten Originalseiten. Firmenname, Impressum, Haftungsangaben und übrige Haupttexte werden unverändert übernommen. Die Texte der Vorschauen 1–2 sind weiterhin Entwurfsstand. Die historischen Hinweise weiter unten beschreiben die damalige Übergabe, nicht den aktuellen Veröffentlichungsstand.

Mit Hugo 0.168.0, Dart Sass 1.106.1 und Python 3 auf dem Suchpfad:

```sh
python scripts/build-site.py
python scripts/verify-site.py
python -m unittest discover -s tests
python -m http.server 8000 --directory public
```

Die vier Hugo-Projekte liegen unter `hugo/`; feste Theme-Stände samt Lizenz liegen unter `hugo/themes/`. Ein GitHub-Workflow baut und prüft dieselbe Ausgabe und veröffentlicht ausschließlich `public/`.

Details und bekannte Archivlücken: [Hugo-Übergabe und Sicherheitsprüfung](docs/HUGO-VARIANTEN-2026-10-26.md).

## Ursprüngliche Übergabe: vorhandene Entwürfe

1. **Ruhig / Salbei** – ursprünglicher Entwurf unverändert.
2. **Editorial / Bordeaux** – Serifentypografie, Partnerinnen vor den Anliegen, Themenliste.
Der damals dritte Vorschlag **Klar / Kobaltblau** wurde inzwischen ausdrücklich gelöscht.

Vergleichsdatei: [Christmann-Heise-Designvergleich.html](christmann-heise-designs/Christmann-Heise-Designvergleich.html). Sie enthält alle drei durchklickbaren Varianten und ein eingebettetes Quellarchiv. Eine GitHub-Dateiansicht führt HTML nicht als Website aus; für die Vorschau die Datei lokal öffnen oder eine getrennte Vorschau bereitstellen.

## Projektstruktur

- `christmann-heise/`: erste Fassung, Build, Inhalte, Gestaltung, Quelleninventar und offene Prüfungen.
- `christmann-heise-designs/`: Designvergleich, drei eigenständige HTML-Vorschauen, Alternativ-Styles und Skripte.
- `christmann-heise-designs/projekte/`: drei vollständige Quellstände.
- `docs/UEBERGABE-2026-10-26.md`: Auftrag, übernommene Inhalte, Grenzen, Prüfungen und nächste Schritte.
- `docs/dateien-sha256.json`: Dateiverzeichnis mit Prüfsummen des übernommenen Materials.

Generierte `dist/`-Ordner wurden weggelassen; sie sind mit den enthaltenen Python-Skripten reproduzierbar. Keine Paketinstallation erforderlich.

## Lokal ausführen

```sh
python3 christmann-heise/scripts/build.py
python3 -m http.server 8000 --directory christmann-heise/dist
```

Dann `http://localhost:8000` öffnen. Für eine andere Variante deren `projekte/<Variante>/scripts/build.py` ausführen und den dort erzeugten `dist`-Ordner ausliefern.

Alle Alternativen und die Vergleichsdatei neu erstellen:

```sh
python3 christmann-heise-designs/create-variants.py
python3 christmann-heise-designs/build-comparison.py
```

**Entwurfsstand:** Originalfotos, Original-Logo und bestätigte Markenfarben fehlen. Rechtliche Angaben sind nicht veröffentlichungsfertig. Notara-Link fehlt. Keine öffentliche Bereitstellung und keine Domain-/DNS-Änderung durch diese Übergabe.
