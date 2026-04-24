# Auftrag für Claude Code: Quartz-Wiki Design, Texte und 404-Seiten fixen

## Ausgangslage

Das Quartz-Wiki ist deployed unter:

```text
https://website-wiki-quartz.vercel.app/
```

Die Startseite funktioniert grundsätzlich.

Aktueller Screenshot-Zustand:

- Startseite wird angezeigt
- linke Navigation/Explorer ist sichtbar
- Graphansicht ist sichtbar
- Graph ist beim Anklicken/Öffnen gut nutzbar
- die kleine Graph-Vorschau in der rechten Sidebar ist zu klein und schlecht lesbar
- einzelne Seiten wie z. B. `/Themen/AI-Agents` liefern aktuell 404
- einige Texte sind noch zukunftsorientiert formuliert, z. B. „Das Wiki soll...“
- die Texte sollen im Präsens formuliert sein, z. B. „Das Wiki ist...“

---

## Ziel

Bitte das bestehende Quartz-Projekt im Repo fixen und verbessern.

Projektordner lokal:

```text
C:\Users\pasca\Documents\Claude\Projekte\website-wiki-quartz
```

Repo:

```text
Pascal-64/website-wiki-quartz
```

Production-URL:

```text
https://website-wiki-quartz.vercel.app/
```

---

## Wichtig

Nicht neu initialisieren.

Nicht das Projekt neu aufsetzen.

Nur gezielt fixen:

1. Texte überarbeiten
2. Graph-Vorschau verbessern
3. 404 bei Einzelseiten beheben
4. Build lokal testen
5. Änderungen committen

Vor Änderungen zuerst prüfen:

```bash
cd C:\Users\pasca\Documents\Claude\Projekte\website-wiki-quartz
git status
npm install
```

Falls lokale Änderungen vorhanden sind, diese nicht blind überschreiben.

---

# Aufgabe 1: Texte ins Präsens umschreiben

## Problem

Auf der Startseite steht aktuell sinngemäß:

```text
Das Wiki soll bewusst getrennt davon aufgebaut werden, damit Portfolio und Wiki unabhängig deploybar bleiben.
Später können ausgewählte Obsidian-Notizen hier ergänzt werden...
```

Das ist zu sehr Projekt-/Planungstext.

## Ziel

Alle öffentlichen Seiten im Ordner `content/` sollen nicht wie ein Bauplan klingen, sondern wie eine fertige Website.

Formulierungen wie:

```text
soll
sollte
später
geplant
wird später
kann später
dient später
```

sollen ersetzt werden durch Präsens-Formulierungen.

## Beispiel für `content/index.md`

Bitte `content/index.md` inhaltlich ungefähr so anpassen:

```md
---
title: Wiki
---

# Wiki

Öffentlicher Wissensbereich zu Projekten, Tools, LLM-Workflows und technischen Notizen.

## Bereiche

- [[Projekte/README|Projekte]]
- [[LLM-Wiki/README|LLM-Wiki]]
- [[Tools/README|Tools]]
- [[Themen/AI-Agents|AI-Agents]]
- [[Glossar/Agent|Glossar]]

## Zweck

Dieses Wiki ist ein strukturierter öffentlicher Wissensbereich neben meiner Portfolio-Seite.

Die bestehende Portfolio-Seite läuft hier:

https://website-eight-lilac-81.vercel.app/

Portfolio und Wiki bleiben bewusst getrennt. Dadurch sind beide Projekte unabhängig deploybar, wartbar und erweiterbar.

Ausgewählte Obsidian-Notizen werden hier als öffentliche Markdown-Seiten dargestellt. Private Vault-Inhalte bleiben außerhalb dieses Repos.
```

## Weitere Seiten

Bitte auch diese Bereiche prüfen und bei Bedarf anpassen:

```text
content/Projekte/
content/LLM-Wiki/
content/Tools/
content/Themen/
content/Glossar/
```

Alle Texte sollen wie fertige Inhalte wirken, nicht wie To-do- oder Projektplan-Texte.

---

# Aufgabe 2: Graph-Vorschau größer und besser nutzbar machen

## Problem

Die Graphansicht in der rechten Sidebar ist zu klein.

Beim Anklicken ist der Graph gut, aber die Vorschau rechts wirkt fast nutzlos.

## Ziel

Die Graph-Vorschau in der rechten Sidebar soll größer und besser lesbar sein.

## Erwartung

Bitte die Quartz-Komponenten/CSS prüfen:

Mögliche Dateien:

```text
quartz.layout.ts
quartz/components/Graph.tsx
quartz/components/styles/graph.scss
quartz/styles/custom.scss
quartz/styles/base.scss
```

Je nach Quartz-Version kann die Struktur abweichen.

## Gewünschte Anpassung

Die kleine Graph-Karte rechts soll größer werden.

Orientierungswerte:

```scss
.graph {
  min-height: 320px;
}

.graph > .graph-outer,
.graph-container,
#graph-container {
  min-height: 320px;
}
```

Falls Quartz eine konkrete Graph-Komponente mit Optionen hat, bevorzugt über Optionen lösen.

Beispiel, falls unterstützt:

```ts
Component.Graph({
  localGraph: {
    depth: 2,
  },
  globalGraph: {
    depth: -1,
  },
})
```

Nur verwenden, wenn die aktuelle Quartz-Version diese API wirklich unterstützt.

## Design-Ziel

- rechte Graph-Vorschau mindestens ca. 300–350 px hoch
- nicht nur ein winziger Punkt-Cluster
- weiterhin responsive
- keine Überlagerung mit Inhaltsverzeichnis
- beim Klick darf die große Graphansicht weiterhin funktionieren

## Minimaler CSS-Fix

Falls keine bessere Komponentenkonfiguration möglich ist, bitte in einer passenden SCSS/CSS-Datei ergänzen:

```scss
.graph {
  min-height: 340px;
}

.graph svg {
  min-height: 320px;
}

.graph-container {
  min-height: 320px;
}
```

Aber bitte vorher die tatsächlichen Klassennamen im generierten/Quellcode prüfen. Nicht blind falsche Klassen einbauen.

---

# Aufgabe 3: 404 bei einzelnen Seiten beheben

## Problem

Diese URL liefert 404:

```text
https://website-wiki-quartz.vercel.app/Themen/AI-Agents
```

Auf der Startseite und im Explorer existiert aber ein Eintrag „AI Agents“.

Das bedeutet wahrscheinlich:

- Datei-Name und URL-Slug stimmen nicht überein
- Link verwendet falsche Schreibweise
- Quartz erzeugt andere Slugs
- Sonderzeichen/Umlaute/Leerzeichen werden anders behandelt
- Vercel/Quartz erwartet trailing slash oder kleingeschriebene Pfade
- Datei liegt evtl. als `AI Agents.md`, aber Link zeigt auf `AI-Agents`
- oder Build enthält die Datei nicht korrekt

## Ziel

Alle Explorer-Seiten und internen Links müssen funktionieren.

## Vorgehen

Bitte lokal prüfen:

```bash
npx quartz build
```

Dann Output prüfen:

```text
public/
```

Insbesondere suchen nach:

```text
public/Themen/
public/themen/
public/Themen/AI-Agents/
public/Themen/AI Agents/
public/Themen/AI-Agents.html
```

Unter Windows z. B.:

```powershell
Get-ChildItem -Recurse public | Select-String "AI"
```

oder:

```powershell
Get-ChildItem -Recurse public | Where-Object { $_.Name -match "AI|Agent" }
```

## Erwartete Lösung

Die Markdown-Datei und der Link sollen eindeutig zusammenpassen.

Empfohlener sauberer Standard:

```text
content/Themen/AI-Agents.md
```

mit Frontmatter:

```md
---
title: AI Agents
---

# AI Agents
```

Und Links so setzen:

```md
[[Themen/AI-Agents|AI Agents]]
```

Nicht mischen:

```text
AI Agents.md
AI-Agents.md
AI_Agents.md
AI-Agents/index.md
```

Bitte für alle Themen-Dateien prüfen und vereinheitlichen.

## Betroffene Bereiche

Prüfe insbesondere:

```text
content/Themen/
content/Glossar/
content/Projekte/
content/LLM-Wiki/
content/Tools/
```

Jeder Eintrag im Explorer soll anklickbar sein.

Jede interne Wiki-Verlinkung soll auf eine existierende Seite zeigen.

## Typische Fixes

Falls Dateien mit Leerzeichen existieren:

```text
AI Agents.md
Machine Learning.md
Prompt Engineering.md
```

dann entweder:

### Variante A: Links an echte Dateinamen anpassen

```md
[[Themen/AI Agents|AI Agents]]
```

oder besser:

### Variante B: Dateien sauber slugfähig umbenennen

```text
AI-Agents.md
Machine-Learning.md
Prompt-Engineering.md
```

und Links entsprechend anpassen:

```md
[[Themen/AI-Agents|AI Agents]]
[[Themen/Machine-Learning|Machine Learning]]
[[Themen/Prompt-Engineering|Prompt Engineering]]
```

Bitte Variante B bevorzugen, weil die URLs sauberer sind.

---

# Aufgabe 4: Explorer und Startseitenlinks prüfen

## Ziel

Die Navigation links und die Links auf der Startseite sollen konsistent sein.

Bitte prüfen:

- Startseitenlinks funktionieren
- Explorer-Links funktionieren
- Themen-Seiten funktionieren
- Glossar-Seiten funktionieren
- README-Seiten funktionieren
- keine 404-Links im Build

Falls möglich, nach dem Build die erzeugten Seiten prüfen.

Beispiele, die funktionieren sollen:

```text
/
 /Projekte/
 /LLM-Wiki/
 /Tools/
 /Themen/AI-Agents/
 /Glossar/Agent/
```

Wenn Quartz automatisch andere Slugs erzeugt, dann die Links und Hinweise entsprechend an die reale Struktur anpassen.

---

# Aufgabe 5: Build- und Deploy-Test

Nach den Änderungen ausführen:

```bash
npm install
npx quartz build
```

Falls möglich lokal testen:

```bash
npx quartz build --serve
```

Lokal prüfen:

```text
http://localhost:8080/
http://localhost:8080/Themen/AI-Agents
```

Falls Quartz trailing slash benötigt, auch prüfen:

```text
http://localhost:8080/Themen/AI-Agents/
```

---

# Aufgabe 6: README aktualisieren

README bitte ergänzen um einen kurzen Abschnitt:

```md
## Aktuelle Production-URL

```text
https://website-wiki-quartz.vercel.app/
```

## Portfolio-Seite

```text
https://website-eight-lilac-81.vercel.app/
```

## Hinweise zu URLs

Markdown-Dateien in `content/` werden als Seiten gerendert. Dateinamen und interne Links sollen konsistent sein.

Bevorzugter Standard:

```text
content/Themen/AI-Agents.md
```

Link:

```md
[[Themen/AI-Agents|AI Agents]]
```
```

Achtung: Markdown-Codeblöcke im README korrekt escapen.

---

# Aufgabe 7: Git Commit

Wenn alles lokal funktioniert:

```bash
git status
git add .
git commit -m "Fix wiki content, graph preview and page routes"
git push
```

Vor Push prüfen:

- keine `node_modules`
- kein versehentliches `.env`
- kein unnötiger Build-Output, falls `public/` ignoriert ist
- keine privaten Vault-Inhalte

---

# Akzeptanzkriterien

Erledigt ist die Aufgabe erst, wenn:

1. Texte auf öffentlichen Seiten im Präsens formuliert sind.
2. Startseite nicht mehr wie Projektplanung klingt.
3. Graph-Vorschau rechts größer und besser lesbar ist.
4. Die große Graphansicht beim Anklicken weiterhin funktioniert.
5. `/Themen/AI-Agents` oder die korrekt erzeugte entsprechende URL funktioniert.
6. Explorer-Links führen nicht mehr auf 404.
7. Startseitenlinks führen nicht mehr auf 404.
8. `npx quartz build` läuft erfolgreich.
9. README enthält aktuelle Production-URL und Portfolio-URL.
10. Änderungen sind committed und gepushed.

---

# Abschlussmeldung

Bitte nach Abschluss klar ausgeben:

```text
Erledigt:
- Texte ins Präsens umgeschrieben
- Graph-Vorschau vergrößert
- Seitenrouten/Slugs geprüft und korrigiert
- Build erfolgreich getestet
- README aktualisiert
- Änderungen committed/gepusht

Geprüfte URLs:
- /
- /Projekte/
- /LLM-Wiki/
- /Tools/
- /Themen/AI-Agents/
- /Glossar/Agent/
```

Falls etwas nicht funktioniert, nicht beschönigen.

Dann ausgeben:

```text
Nicht erledigt:
- Problem:
- Datei:
- Befehl:
- Fehler:
- Nächster konkreter Fix:
```
