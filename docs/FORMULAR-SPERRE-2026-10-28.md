# Globale Formular-Sperre aus der Veröffentlichung entfernen

## Nachgewiesene Ursache

Auf der veröffentlichten Hauptseite und allen sieben Originalseiten wurde
`assets/preview-runtime.js` geladen, auf Unterseiten mit relativem Pfad `../assets/`.
Das Skript registrierte einen dokumentweiten `submit`-Listener in der
Capture-Phase und rief für jedes Ereignis `preventDefault()` sowie
`stopImmediatePropagation()` auf. Damit erreichten Formularereignisse weder
Handler am Formular noch delegierte Handler am Dokument.

Eine Browserprobe auf der veröffentlichten Startseite bestätigte vor der
Reparatur: `dispatchAccepted=false`, `defaultPrevented=true`,
`handlerReached=false`. Die Probe verwendete ausschließlich ein künstliches
Ereignis an einem leeren, vorübergehend erzeugten Formularelement. Es wurden
keine Formulardaten, Notara-Anfragen oder Übermittlungen erzeugt.

## Reparatur

- `scripts/build-original.py` bindet die Sperre nicht mehr ein. Die öffentliche
  Notara-Einbindung bleibt unverändert erhalten.
- Die Sperrdatei wird entfernt. Die gespeicherten Original-Nachbauseiten und
  Hugo-Head-Daten enthalten ebenfalls keine Einbindung mehr.
- Archivierte Originalquellen, Kanzleitexte, Gestaltung und öffentliche
  Notara-Kennung `1499` bleiben unverändert, abgesehen von der anschließend
  ausdrücklich beauftragten Entfernung des alten Kontaktformulars aus der Ausgabe.
- `scripts/verify-site.py` verwirft eine erneute Auslieferung der Datei oder
  Einbindung auf einer der 14 Hauptseiten-/Original-Vorschauadressen. Der
  Notara-Loader muss auf allen diesen Seiten erhalten bleiben.

## Prüfung und Grenze des Nachweises

`scripts/verify-form-runtime.cjs` prüft mit Playwright die sieben Hauptseiten
und ihre sieben Original-Vorschauen. Künstliche Ereignisse müssen bis zum
Formular-Handler und zum delegierten Dokument-Handler gelangen und dürfen
nicht global abgebrochen werden. Eine Gegenprobe mit dem früheren Blocker muss
fehlschlagen. Der öffentliche Notara-Loader wird mit einer Test-Konstruktorfunktion
auf die unveränderte Kennung `1499` geprüft; der externe Anbieter wird dabei
nicht kontaktiert. Alle externen und alle nicht lesenden Anfragen sind gesperrt.

Die Prüfung ist keine vollständige Notara-Formularübermittlung. Das Verbot von
Testübermittlungen bleibt bestehen.

## Nutzerauftrag: altes WordPress-Kontaktformular entfernen

Im selben Auftrag hat der Nutzer ausdrücklich die Entfernung des alten
Kontaktformulars verlangt. Der Build entfernt deshalb auf Kontakt ausschließlich
den alten `wpcf7`-Formularblock einschließlich Feldern, Einwilligung und Absenden-
Schaltfläche. Die vorhandenen Kontaktdaten und Notara bleiben erhalten. Es wird
kein WordPress-Backend eingerichtet und kein Ersatztext erfunden.

Die archivierte Originaldatei bleibt bytegenau erhalten. Die Inhaltsprüfung
berücksichtigt ausschließlich diese genehmigte Entfernung auf Kontakt; alle
übrigen Originaltexte werden weiter verglichen. Eine Gegenprobe mit veränderter
Kontaktadresse muss weiterhin fehlschlagen. Eine weitere Gegenprobe verhindert,
dass das alte Formular wieder in die Ausgabe gelangt.

Bei vorhandenem Playwright: `node scripts/verify-form-runtime.cjs --directory public`
oder nach Veröffentlichung `node scripts/verify-form-runtime.cjs --base-url https://christmann-heise.de/`.
Unter Windows kann `BROWSER_CHANNEL=msedge` verwendet werden. Die lokalen
Prüfberichte liegen unter `preview-review/form-runtime/`.
