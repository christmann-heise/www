# Christmann & Heise · www-ch

Vollständige Übergabe der Website-Arbeit aus der Unterhaltung vom 24.–26. Oktober 2026. Stand: 26.10.2026.

**Hier beginnen:** [Arbeitsstand und Fortsetzung](docs/UEBERGABE-2026-10-26.md).

## Aktueller Hugo-Stand

Zieltechnik ist Hugo. [Vorschauauswahl](https://christmann-heise.github.io/www/) und [Vergleich](https://christmann-heise.github.io/www/christmann-heise-designs/Christmann-Heise-Designvergleich.html) enthalten sieben Varianten. Die drei ursprünglichen HTML-Entwürfe bleiben erhalten. Neu sind:

4. **Original / Archiv**: Hugo-Nachbau mit dem gesicherten Vortex-Design.
5. **Hugo Arcana**: angefragtes Theme mit Originalinhalten.
6. **Hugo Agnes**: angefragtes Theme mit Originalinhalten.
7. **Hugo Blunix**: angefragtes Theme mit Originalinhalten.

Jede der vier neuen Hugo-Varianten enthält die sieben gesicherten Originalseiten. Firmenname, Impressum, Haftungsangaben und übrige Haupttexte werden unverändert übernommen. Es gibt keine neuen Leistungsseiten oder erfundenen Aussagen. Die historischen Hinweise weiter unten beschreiben die damalige Übergabe, nicht den aktuellen Veröffentlichungsstand.

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
3. **Klar / Kobaltblau** – serifenlose Typografie, direkter Anliegenzugang, Karten.

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
