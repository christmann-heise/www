# Projektvorgaben

## Verbindliche Nutzeranweisungen vom 26.10.2026

- Inhaltlich und bei den Seiten bei der Wahrheit bleiben: keine Erfindungen, keine neuen Ideen.
- Firmenname, Impressum und Haftungsangaben sind fix. Keine Interpretation, redaktionelle Neufassung, eigenständige Aktualisierung oder Ergänzung.
- Originaltexte und Originalseiten aus belegten Quellen übernehmen. Abweichende Quellenstände und fehlende Angaben dokumentieren, nicht selbst auflösen oder auffüllen.
- Die neue Gestaltung soll der alten Website so nahe wie möglich kommen. Tatsächlich archivierte Farben, Schriften und Gestaltung sind maßgeblich; Designvorschläge nicht als Original ausgeben.
- Es gibt sechs Vorschauen: 1 Ruhig, 2 Editorial, 3 Originalnachbau, 4 Hugo Arcana, 5 Hugo Agnes, 6 Hugo Blunix. Der frühere Kobaltblau-Vorschlag ist gelöscht und darf nicht erneut erzeugt werden.
- Dosis, Libre Baskerville kursiv für Zitate und die belegten Originalfarben einschließlich Violett `#7a3674` gelten unabhängig vom Theme in allen Varianten. Keine eigenen Theme-Schriften oder alternativen Markenfarben verwenden.
- Notara ist in allen Varianten Pflicht. Die belegte öffentliche Einbindung mit Kennung 1499 verwenden; niemals Passwörter oder Zugangstoken einbetten. Keine Testformulare absenden.
- Die beiden früheren Entwürfe sind weiterhin Gestaltungsvorschauen; ihre Texte sind nicht vollständig als Originalübernahme freigegeben. Ihr Aufbau bleibt erhalten, die ausdrücklich beauftragte Originalgestaltung und Notara werden übernommen.
- Arbeit erst als abgeschlossen melden, wenn die beauftragten Änderungen auf GitHub committed sind und lokales `main` nach frischem Abruf mit `origin/main` übereinstimmt. Nicht committete Änderungen gesondert prüfen.

## Quellen

- Zieltechnik ist Hugo. Varianten 3 bis 6 sind Originalnachbau, Hugo Arcana, Hugo Agnes und Hugo Blunix; alle vier verwenden die sieben belegten Originalseiten.
- Themes dürfen ihre eigenen Beispieltexte, Demo-Firmennamen, Leistungsversprechen, Preise oder Kontaktdaten nicht in die Kanzleiseiten übernehmen.
- Vor Veröffentlichung `scripts/build-site.py`, `scripts/verify-site.py` und die Tests zur unveränderten Übernahme der Originaltexte ausführen. Keine Zugangsdaten im öffentlichen Repository speichern.

- `docs/ARCHIV-GESTALTUNG-2026-10-26.md`: belegte Gestaltung und Grenzen der Archivfunde.
- `docs/archive-original/`: archivierte Quelltexte, Stylesheets und Herkunftsnachweise. HTML absichtlich als `.html.txt` archiviert, damit alter aktiver Code nicht als Website ausgeführt wird.
- `docs/ORIGINALBILDER-2026-10-26.json`: wiederhergestellte Originalporträts mit Herkunfts-URL und Prüfsumme.
- `docs/REPOSITORY-SCHUTZ.md` und `.github/security/`: beauftragte Zugriffskontrolle und Schutz von `main`. Nach Aktivierung nur über den vorgeschriebenen Pull-Request- und Review-Weg liefern; Regeln nicht umgehen.
