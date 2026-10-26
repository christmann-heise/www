# Christmann & Heise · www-ch

Vollständige Übergabe der Website-Arbeit aus der Unterhaltung vom 24.–26. Oktober 2026. Stand: 26.10.2026.

**Hier beginnen:** [Arbeitsstand und Fortsetzung](docs/UEBERGABE-2026-10-26.md).

## Vorhandene Entwürfe

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
