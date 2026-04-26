Bewertung: grundsätzlich gut, aber noch zu riskant für automatisches Schreiben

Der Plan ist technisch sinnvoll und passt gut zu einem Quartz/Obsidian-Wiki. Die Richtung ist richtig: Backlog-Datei, täglicher GitHub-Action-Lauf, Claude-Recherche, Pull Request statt direkter Main-Commit. Das ist der entscheidende Sicherheitsanker.

Aber: In der jetzigen Form würde ich ihn nicht 1:1 produktiv laufen lassen. Er hat noch zu viele Stellen, an denen automatisch mittelmäßiger oder falscher Inhalt ins Wiki geschrieben werden kann.

Meine Bewertung:

Konzept:        8/10
Architektur:    7/10
Qualitätsschutz: 4/10
Sicherheit:     6/10
Wartbarkeit:    7/10
Produktivreife: 5/10
Was am Plan stark ist
1. Pull Request statt direkter Commit auf main

Das ist richtig. Der Agent darf schreiben, aber nicht ungeprüft veröffentlichen. Genau so sollte man es machen.

GitHub Actions kann mit GITHUB_TOKEN authentifizieren, und die Rechte lassen sich über permissions im Workflow begrenzen. Für PR-Erstellung muss im Repository zusätzlich erlaubt sein, dass GitHub Actions Pull Requests erstellen darf. Das ist in den Repo-Einstellungen unter Actions/Workflow permissions relevant.

2. Manuelles Backlog ist besser als vollautomatische Themenwahl

content/wiki-gaps.md als Steuerdatei ist gut. Damit bleibt der Mensch der Taktgeber.

Das ist besser als: „Agent scannt alles und schreibt irgendwo irgendwas“.

3. Dünne Seiten automatisch erkennen ist sinnvoll

Diese Regeln sind brauchbar:

Wortanzahl < 250
status: draft
TODO:

Das reicht für Version 1.

4. Kein Überschreiben ganzer Dateien

Sehr wichtig. Nur Abschnitte ergänzen oder gezielt ersetzen. Sonst zerstört dir der Agent irgendwann mühsam gepflegte Inhalte.

Die größten Schwachstellen
1. „Claude sucht selbst“ ist zu unkontrolliert

Der Satz ist gefährlich:

Claude API aufrufen mit web_search Tool
Claude sucht selbst, generiert deutschen Inhalt

Das klingt bequem, ist aber für ein Wiki zu locker. Du brauchst nachvollziehbare Quellenpflicht.

Besser:

Jeder neu generierte Abschnitt muss eine Quellenliste enthalten.
Jede zentrale Faktenbehauptung braucht mindestens eine Quelle.
Quellen werden im PR-Text zusammengefasst.

Anthropic unterstützt Tool Use grundsätzlich, also Modelle können Tools aufrufen, aber die Anwendung muss sauber definieren, welche Tools verfügbar sind und wie Ergebnisse verarbeitet werden.

Für dein Wiki würde ich nicht nur „Web Search an“ machen, sondern erzwingen:

research_notes
source_urls
content_patch
quality_score

Also nicht direkt freien Markdown ausgeben lassen.

2. Automatisches Markieren von - [ ] zu - [x] ist zu früh

Das ist der größte praktische Fehler.

Wenn der Agent ein Thema verarbeitet, heißt das nicht, dass es erledigt ist.

Besser:

- [ ] offen
- [~] PR erstellt / in Review
- [x] erledigt nach Merge

Oder einfacher:

- [ ] LLM – mehr Beispiele und Kontext

Nach PR-Erstellung wird daraus:

- [ ] LLM – mehr Beispiele und Kontext
  - PR: #123
  - Status: review

Erst nach manuellem Merge sollte es als erledigt gelten. Sonst verlierst du Lücken, obwohl der Inhalt vielleicht schlecht war.

3. Wortanzahl < 250 ist zu grob

Eine Seite mit 230 guten Wörtern kann fertig sein. Eine Seite mit 800 schlechten Wörtern kann trotzdem dünn sein.

Besser zusätzlich prüfen:

Fehlen Überschriften?
Fehlen Beispiele?
Fehlen interne Wikilinks?
Fehlen Quellen?
Fehlt "Warum ist das wichtig?"
Fehlt "Praxisbezug"?

Für deine Wiki-Idee wäre ein besserer Gap-Score:

gap_score =
  kurze_seite
  + keine_quellen
  + keine_wikilinks
  + enthält_TODO
  + status_draft
  + keine_beispiele

Dann nur Seiten bearbeiten, die z. B. gap_score >= 3 haben.

4. Keine Begrenzung pro Lauf

Der Plan sagt „pro Lücke/Thema“. Das kann teuer und chaotisch werden.

Du brauchst harte Limits:

MAX_MANUAL_GAPS_PER_RUN=2
MAX_AUTO_GAPS_PER_RUN=3
MAX_FILES_CHANGED=5
MAX_OUTPUT_TOKENS_PER_TOPIC=2500

Sonst erzeugt ein Cron-Lauf irgendwann einen riesigen PR mit 30 Dateien. Den reviewt niemand.

Claude Sonnet 4.6 ist laut Anthropic ein aktuelles Modell für Coding/Agenten/Enterprise-Workflows; die API-Kosten liegen laut Anthropic-Dokumentation bei Sonnet 4.6 bei $3 pro Million Input Tokens und $15 pro Million Output Tokens. Ohne Limits kann das bei täglichem Lauf unnötig teuer werden.

5. Fehlende Duplikat-Kontrolle

Der Agent könnte Inhalte schreiben, die es im Wiki schon gibt.

Vor jedem Schreiben sollte das Script prüfen:

Gibt es bereits eine ähnliche Seite?
Gibt es bereits einen Abschnitt mit ähnlicher Überschrift?
Welche internen Links passen?
Soll eine neue Seite erstellt oder bestehende erweitert werden?

Sonst bekommst du irgendwann:

LLM.md
Large-Language-Models.md
Sprachmodelle.md
KI-Modelle.md

Alle mit ähnlichem Inhalt. Das macht ein Wiki kaputt.

6. Fehlende Qualitätsprüfung nach Generierung

Nach dem Schreiben sollte ein zweiter Prüfschritt laufen.

Nicht:

Claude schreibt → Datei speichern

Sondern:

Claude recherchiert
Claude erstellt Patch
Validator prüft Markdown/Frontmatter/Links
Claude oder Script macht Review
Erst dann Commit

Mindestchecks:

Markdown gültig
Frontmatter gültig
Keine leeren Quellen
Keine "als KI"-Formulierungen
Keine erfundenen Links
Keine kaputten Obsidian-Links
Keine komplette Datei überschrieben
Maximale Änderungslänge eingehalten
7. GitHub Pages/Vercel Build kann eventuell nicht automatisch triggern

Wichtig: GitHub schreibt selbst, dass Events, die durch GITHUB_TOKEN ausgelöst werden, normalerweise keine neuen Workflow-Runs auslösen. Außerdem steht dort ausdrücklich, dass Commits, die ein Workflow mit GITHUB_TOKEN pusht, keinen GitHub-Pages-Build triggern.

Für dich heißt das:

Wenn dein Wiki über Vercel läuft, ist es meistens unkritischer, weil Vercel oft auf GitHub-Commits reagiert. Aber wenn du zusätzlich GitHub Actions/Pages-Builds nutzt, musst du prüfen, ob der automatische PR/Merge den gewünschten Deploy wirklich startet.

Konkrete Verbesserung des Plans
Zielarchitektur, besser formuliert
content/wiki-gaps.md
  Manuelle Themensteuerung

scripts/detect_wiki_gaps.py
  Erkennt dünne/problematische Seiten

scripts/fill_wiki_gaps.py
  Erzeugt Inhaltspatches

scripts/validate_wiki_changes.py
  Prüft Markdown, Links, Frontmatter, Quellen

.github/workflows/fill-wiki-gaps.yml
  Täglicher oder manueller Lauf

.github/pull_request_template.md
  Review-Checkliste für Wiki-Änderungen

Ich würde die Hauptlogik nicht komplett in eine Datei quetschen. Für Version 1 geht das, aber sauberer sind drei getrennte Schritte:

detect → generate → validate
Bessere Statuslogik in wiki-gaps.md

Statt direkt [x]:

## Manuell eingetragen

- [ ] LLM – mehr Beispiele und Kontext, insb. Finetuning und RLHF
  status: open
  priority: high

- [ ] Transformer – Attention Mechanism mit Schritt-für-Schritt-Erklärung
  status: open
  priority: medium

Nach Verarbeitung:

- [ ] LLM – mehr Beispiele und Kontext, insb. Finetuning und RLHF
  status: review
  pr: 123
  last_attempt: 2026-04-26

Erst nach Merge manuell:

- [x] LLM – mehr Beispiele und Kontext, insb. Finetuning und RLHF
  status: done

Traditionell sauberer: erledigt ist erst erledigt, wenn ein Mensch es abgenommen hat.

Besserer Prompt-Aufbau

Der aktuelle Prompt ist zu allgemein.

Besser:

Du erweiterst ein deutsches Technik-Wiki im Obsidian/Quartz-Format.

Aufgabe:
- Erweitere nur das angegebene Thema.
- Erhalte bestehenden Inhalt.
- Schreibe sachlich, technisch, klar.
- Keine Marketing-Sprache.
- Keine erfundenen Quellen.
- Keine Aussagen ohne Quelle, wenn sie historisch, technisch spezifisch oder aktuell sind.
- Nutze interne Wikilinks im Format [[Thema]], aber nur wenn sie sinnvoll sind.
- Erzeuge keinen kompletten Artikel neu, sondern einen Patch/Abschnitt.

Ausgabeformat:
{
  "summary": "...",
  "target_file": "...",
  "patch_markdown": "...",
  "sources": ["..."],
  "internal_links": ["..."],
  "confidence": 0.0-1.0,
  "needs_human_review": true/false
}

Der JSON-Zwischenschritt ist wichtig. Erst danach schreibt dein Script Markdown in die Datei.

Workflow verbessern

Dein Workflow ist fast richtig. Ich würde ergänzen:

concurrency:
  group: wiki-gap-filler
  cancel-in-progress: false

Sonst können zwei Läufe gleichzeitig Branches/PRs erzeugen.

Außerdem:

permissions:
  contents: write
  pull-requests: write

Das passt. GitHub empfiehlt grundsätzlich minimale Rechte für GITHUB_TOKEN, und Rechte können jobbezogen gesetzt werden.

Zusätzlich brauchst du in den Repo-Einstellungen:

Settings
→ Actions
→ General
→ Workflow permissions
→ Allow GitHub Actions to create and approve pull requests

Sonst kann dein Workflow trotz YAML-Rechten beim PR-Erstellen scheitern.

Meine empfohlene Version 1

Für den ersten stabilen Ausbau würde ich es bewusst kleiner machen:

1. Nur manuelle Lücken aus wiki-gaps.md verarbeiten
2. Maximal 1–2 Themen pro Lauf
3. Keine automatisch erkannten Seiten direkt ändern
4. Automatische Gap-Erkennung nur als Report in wiki-gaps.md
5. PR erstellen
6. Kein automatisches [x], nur Status "review"

Das ist langsamer, aber kontrollierbar.

Danach Version 2:

Automatisch erkannte Lücken dürfen einfache Ergänzungen vorschlagen.

Version 3:

Agent darf neue Seiten vorschlagen.

Version 4:

Agent darf bestehende Seiten strukturell refactoren.

Nicht alles auf einmal. Sonst wird das Wiki schnell zur KI-Müllhalde.

Was ich am Plan ändern würde
Ändern
Manuelle - [ ] Items als - [x] markieren

zu:

Manuelle Items auf status: review setzen und PR-Nummer eintragen
Ergänzen
Maximal 3 Lücken pro Lauf
Ergänzen
Quellenpflicht mit Quellenliste pro Abschnitt
Ergänzen
validate_wiki_changes.py
Ergänzen
Keine neuen Seiten ohne expliziten Backlog-Eintrag
Ergänzen
PR enthält Checkliste:
- Quellen geprüft
- Keine Duplikate
- Wikilinks sinnvoll
- Inhalt sachlich korrekt
- Keine kaputten Markdown-Strukturen
Nüchternes Fazit

Der Plan ist eine gute Basis, aber aktuell eher ein automatischer Content-Generator als ein sauberer Wiki-Pfleger.

Für ein ernsthaftes Wiki brauchst du weniger Magie und mehr Kontrolle:

Backlog steuert.
Agent schlägt vor.
Script validiert.
PR dokumentiert.
Mensch merged.

So würde ich ihn bauen. Nicht vollautomatisch veröffentlichen, nicht blind [x] setzen, nicht unbegrenzt Seiten bearbeiten lassen. Dann ist das System brauchbar und kann langfristig tatsächlich Wert aufbauen.