# Schreibzugriff und Schutz von main

Beauftragter Umfang: Öffentliches Repository `christmann-heise/www` behalten; Schreibzugriff nur über berechtigte Konten und ausdrücklich verbundene Integrationen. Keine neuen Anmeldedaten oder zusätzlichen Konten einrichten.

Die Prüfung am 26.10.2026 ergab zwei direkt berechtigte Administratoren, keine zugeordneten Teams und keine Deploy Keys. Die beiden Organisationsinhaber sind dieselben berechtigten Personen. Die allgemeine Organisationsberechtigung ist bereits `read`; sie wird nicht organisationsweit verändert.

Die bestehende `chatgpt-codex-connector`-App bleibt als ausdrücklich verbundene Integration erhalten. Sie hat keine Ausnahme für die Schutzregeln von `main`. Der Hugo-Veröffentlichungsworkflow hat für Repository-Inhalte nur Leserechte; die zusätzlichen Job-Rechte `pages: write` und `id-token: write` dienen der Veröffentlichung.

## Verbindliche Schutzkonfiguration

Die überprüfbare Konfiguration liegt unter `.github/security/`:

- `main-ruleset.json`: aktives Branch-Regelwerk für `refs/heads/main`, keine Bypass-Akteure, Löschen und Force-Push gesperrt.
- Änderungen an `main` müssen einen Pull Request mit einer Zustimmung durch eine andere berechtigte Person durchlaufen. Neue Commits verwerfen alte Zustimmungen; Review-Diskussionen müssen aufgelöst sein.
- Der GitHub-Actions-Prüflauf `build` muss erfolgreich sein; die PR-Basis muss aktuell sein. Die Prüfintegration ist die tatsächlich verwendete GitHub-Actions-App (`15368`).
- `workflow-permissions.json`: standardmäßig nur Leserechte für Workflows; automatisches Genehmigen von Pull Requests durch Workflows deaktiviert.

Die Regeln werden nach dem geprüften Website-Commit auf GitHub aktiviert und anschließend über die API zurückgelesen. Dateien im Repository allein aktivieren diese GitHub-Einstellungen nicht.

Öffentliches Lesen, Forks und das Einreichen von Pull Requests verleihen Außenstehenden kein Recht, Änderungen in dieses Repository zu übernehmen. Organisationsinhaber können weiterhin die Repository-Verwaltung ausüben; Branch-Regeln ersetzen keinen Kontoschutz.
