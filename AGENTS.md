# Projektvorgaben

## Arbeitsumgebung, nächste Schritte, Freigaben und Abschluss

### Bearbeitung ausschließlich über Work

- Dieses Repository und die Website werden ausschließlich in ChatGPT Work bearbeitet. Eine ausdrückliche Ausnahme kann nur der Nutzer erteilen.
- Wird ein Bearbeitungsauftrag in Codex geöffnet, auf diese Vorgabe hinweisen und einen konkreten Übergabetext für Work mit dem empfohlenen nächsten Schritt bereitstellen. Ohne ausdrückliche Ausnahme keine Dateien ändern und keine Commits, Pushes oder Veröffentlichungen ausführen.
- Diese Regel ist eine Arbeitsanweisung. Sie ersetzt keine technische Zugriffskontrolle.

### GitHub-main als verbindlicher Ausgangsstand

- Vor jeder fachlichen Bearbeitung und beim Wiederaufnehmen eines Auftrags den vorgesehenen Remote und Zielbranch prüfen, den aktuellen GitHub-Stand von `main` erfolgreich abrufen und die betroffenen Dateien sowie Projektvorgaben dieses Stands lesen.
- GitHub-`main` ist der verbindliche Ausgangsstand. Lokale Dateien, zwischengespeicherte Remote-Referenzen, alte Arbeitsbranches und frühere Chat-Aussagen dürfen nicht ungeprüft als aktueller Projektstand gelten.
- In einer lokalen Arbeitskopie vor dem Wechsel oder Abgleich nicht committete Änderungen und zusätzliche lokale Commits prüfen. Ein sauberes lokales `main` nur per Fast-forward auf den frisch abgerufenen Stand bringen; neue Arbeitsbranches von diesem Stand aus anlegen.
- Lokale Änderungen können technisch neuer sein, gelten aber bis zur geprüften Übernahme in GitHub-`main` als separate, noch nicht abgeschlossene Arbeit. Sie weder verlieren noch ungefragt verwerfen, überschreiben oder mit einem anderen Auftrag vermischen.
- Ist der aktuelle GitHub-Stand nicht abrufbar oder gibt es widersprüchliche lokale Änderungen, die davon abhängige Bearbeitung zurückstellen, den konkreten Unterschied benennen und den nächsten Lösungsschritt mit Empfehlung vorlegen. Keinen veralteten Stand als aktuell ausgeben.
- Vor dem Merge erneut auf Änderungen an GitHub-`main` prüfen und die Integration sowie erforderliche Prüfungen auf die aktuelle Basis bringen. Nach dem Merge den Gleichstand erneut durch frischen Abruf belegen.

### Geführte nächste Schritte und schrittweise Freigaben

- Bei Fragen die Frage konkret beantworten und anschließend den besten nächsten Schritt vorschlagen. Bei Änderungswünschen die bereits beauftragten Schritte ausführen und danach den nächsten erforderlichen Schritt vorschlagen.
- Nicht bei bloßer Zustimmung oder einer Aussage wie „Ja, stimmt“ oder „Ich habe nichts geändert“ stehen bleiben. Aus dem aktuellen Stand eine konkrete Handlung ableiten und erklären, was sie bewirkt.
- Den Nutzer durch die nächsten Schritte führen: sinnvolle Auswahlmöglichkeiten anbieten, eine davon klar empfehlen und die Empfehlung kurz begründen. Wenn verfügbar, native Auswahlmöglichkeiten verwenden; andernfalls nummerierte Optionen. Keine künstlichen Alternativen erfinden, wenn es nur einen sinnvollen nächsten Schritt gibt.
- Bei erforderlichen Entscheidungen oder Freigaben jeweils nur den nächsten konkreten Schritt vorlegen. Keine pauschalen Sammelfreigaben für noch unklare Folgeschritte verlangen.
- Nur sachlich notwendige Entscheidungen abfragen. Bereits erteilte Aufträge und Freigaben innerhalb ihres Umfangs ausführen, ohne erneut um Zustimmung zu bitten. Eine Frage allein ist keine Freigabe für eine externe Änderung.
- Unabhängige, bereits beauftragte Vorarbeiten und Prüfungen vor einer Freigabe vollständig erledigen. Der Nutzer soll ein konkretes, prüfbares Ergebnis freigeben können.
- Nach einer Entscheidung den freigegebenen Schritt ausführen, das Ergebnis prüfen und die nächste erforderliche Entscheidung mit Auswahl und Empfehlung vorlegen.
- Ausbleibende Antworten und vorausgewählte Optionen gelten nicht als Freigabe.
- GitHub-Reviews, Branch-Schutz und andere vorgeschriebene Freigaben dürfen nicht umgangen oder durch eine Chat-Freigabe ersetzt werden.

### Wann ein Auftrag abgeschlossen ist

- Änderungen gelten erst als abgeschlossen, wenn sie auf GitHub im Branch `main` enthalten sind. Ein lokaler Commit, ein gepushter Arbeitsbranch oder ein offener Pull Request genügt nicht.
- Den vorgeschriebenen Pull-Request- und Review-Weg einhalten.
- Nach der Nutzerentscheidung vom 28.10.2026 gilt für `main`: Pull Request und erfolgreicher `build` sind Pflicht; die Zahl der erforderlichen Review-Zustimmungen ist `0`. Eine zweite Person ist für die reguläre Übernahme nicht erforderlich. Die übrigen Schutzregeln gelten weiter.
- Nach dem Merge die Remote-Referenzen frisch abrufen und prüfen, dass lokales `main` und `origin/main` denselben Commit haben.
- Die zur Änderung passenden Prüfungen müssen erfolgreich sein.
- Nicht committete Änderungen gesondert prüfen und offen benennen. Fremde Änderungen weder überschreiben noch ungefragt mitnehmen.
- Bei einer beauftragten Veröffentlichung zusätzlich das Deployment und die erreichbare Website prüfen. Ein Merge allein belegt keine erfolgreiche Veröffentlichung.
- Im Abschlussbericht den Commit auf `main`, den Synchronisationsstatus und die relevanten Prüfergebnisse nennen.
- Sind erforderliche Reviews, der Merge, die Synchronisation oder eine beauftragte Veröffentlichung noch offen, den tatsächlichen Stand benennen, etwa „zur Freigabe vorbereitet“ oder „wartet auf Review“. Den Auftrag nicht als fertig melden.

## Verbindliche Nutzeranweisungen vom 26.10.2026

- Inhaltlich und bei den Seiten bei der Wahrheit bleiben: keine Erfindungen, keine neuen Ideen.
- Firmenname, Impressum und Haftungsangaben sind fix. Keine Interpretation, redaktionelle Neufassung, eigenständige Aktualisierung oder Ergänzung.
- Originaltexte und Originalseiten aus belegten Quellen übernehmen. Abweichende Quellenstände und fehlende Angaben dokumentieren, nicht selbst auflösen oder auffüllen.
- Die neue Gestaltung soll der alten Website so nahe wie möglich kommen. Tatsächlich archivierte Farben, Schriften und Gestaltung sind maßgeblich; Designvorschläge nicht als Original ausgeben.
- Aktuelle Entscheidung vom 27.10.2026: Variante 03 Originalnachbau wird die Grundlage der finalen Website; 01 Ruhig und 02 Editorial bleiben Entwürfe. Varianten 04 Arcana, 05 Agnes und 06 Blunix werden entfernt. Der frühere Kobaltblau-Vorschlag darf nicht erneut erzeugt werden.
- Dosis, Libre Baskerville kursiv für Zitate und die belegten Originalfarben einschließlich Violett `#7a3674` gelten unabhängig vom Theme in allen Varianten. Keine eigenen Theme-Schriften oder alternativen Markenfarben verwenden.
- Notara ist in allen Varianten Pflicht. Die belegte öffentliche Einbindung mit Kennung 1499 verwenden; niemals Passwörter oder Zugangstoken einbetten. Keine Testformulare absenden.
- Die beiden früheren Entwürfe sind weiterhin Gestaltungsvorschauen; ihre Texte sind nicht vollständig als Originalübernahme freigegeben. Ihr Aufbau bleibt erhalten, die ausdrücklich beauftragte Originalgestaltung und Notara werden übernommen.
- Arbeit erst als abgeschlossen melden, wenn die beauftragten Änderungen auf GitHub committed sind und lokales `main` nach frischem Abruf mit `origin/main` übereinstimmt. Nicht committete Änderungen gesondert prüfen.

## Quellen

- Zieltechnik ist Hugo. Variante 03 ist der Hugo-Originalnachbau mit sieben belegten Originalseiten; 01 und 02 sind separate Entwürfe.
- Themes dürfen ihre eigenen Beispieltexte, Demo-Firmennamen, Leistungsversprechen, Preise oder Kontaktdaten nicht in die Kanzleiseiten übernehmen.
- Vor Veröffentlichung `scripts/build-site.py`, `scripts/verify-site.py` und die Tests zur unveränderten Übernahme der Originaltexte ausführen. Keine Zugangsdaten im öffentlichen Repository speichern.

- `docs/ARCHIV-GESTALTUNG-2026-10-26.md`: belegte Gestaltung und Grenzen der Archivfunde.
- `docs/archive-original/`: archivierte Quelltexte, Stylesheets und Herkunftsnachweise. HTML absichtlich als `.html.txt` archiviert, damit alter aktiver Code nicht als Website ausgeführt wird.
- `docs/ORIGINALBILDER-2026-10-26.json`: wiederhergestellte Originalporträts mit Herkunfts-URL und Prüfsumme.
- `docs/REPOSITORY-SCHUTZ.md` und `.github/security/`: beauftragte Zugriffskontrolle und Schutz von `main`. Nach Aktivierung nur über den vorgeschriebenen Pull-Request- und Review-Weg liefern; Regeln nicht umgehen.
