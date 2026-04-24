# Auftrag für Claude Code: Quartz 404 bei Explorer-/Ordnerlinks endgültig fixen

## Problem

Im Quartz-Wiki werden Ordnerlisten und Explorer-Einträge angezeigt, aber beim Hover/Klick erscheint weiterhin 404.

Beispiel aus Screenshot:

```text
Ordner: Glossar
Einträge sichtbar:
- Gradient-Descent
- API
- Agent
- Token
- Transformer
```

Beim Hover/Klick auf einzelne Einträge erscheint aber:

```text
404
Diese Seite ist entweder nicht öffentlich oder existiert nicht.
```

Das bedeutet: Quartz erkennt die Dateien für die Ordnerübersicht/Explorer-Struktur, aber die erzeugten Links zeigen auf Pfade, die im Build nicht existieren.

Aktuelle Production-URL:

```text
https://website-wiki-quartz.vercel.app/
```

Lokales Projekt:

```text
C:\Users\pasca\Documents\Claude\Projekte\website-wiki-quartz
```

---

## Ziel

Alle Einzelseiten müssen direkt funktionieren.

Beispiele, die funktionieren müssen:

```text
/Glossar/Agent/
/Glossar/API/
/Glossar/Token/
/Glossar/Transformer/
/Themen/AI-Agents/
/Themen/Machine-Learning/
/Themen/Prompt-Engineering/
```

Falls Quartz andere Slugs erzeugt, müssen Dateinamen, Frontmatter und Links so angepasst werden, dass diese Pfade konsistent und klickbar sind.

---

## Wichtig

Nicht nur CSS oder Design ändern.

Nicht nur Startseitenlinks ändern.

Der Fehler liegt sehr wahrscheinlich in einem dieser Punkte:

1. Dateinamen stimmen nicht mit Links überein
2. Slugs werden anders erzeugt als erwartet
3. Frontmatter enthält falsche `permalink`, `slug`, `aliases`, `draft` oder `publish`
4. Dateien liegen als `README.md`, aber Quartz erwartet `index.md`
5. Ordnerseiten und Einzeldateien erzeugen kollidierende Routen
6. Dateinamen enthalten Leerzeichen, Sonderzeichen oder Groß-/Kleinschreibung, die in Vercel anders aufgelöst werden
7. Links im Explorer zeigen auf kanonische Namen, aber die generierten Dateien heißen anders
8. Vercel ist case-sensitive, Windows lokal nicht

---

# Schritt 1: Repo prüfen

```bash
cd C:\Users\pasca\Documents\Claude\Projekte\website-wiki-quartz
git status
```

Keine vorhandenen Änderungen blind überschreiben.

---

# Schritt 2: Content-Dateien auflisten

Bitte ausführen:

```powershell
Get-ChildItem -Recurse content -File | Select-Object FullName
```

Zusätzlich:

```powershell
Get-ChildItem -Recurse content -File -Include *.md | ForEach-Object {
  Write-Host "-----"
  Write-Host $_.FullName
  Get-Content $_.FullName -TotalCount 20
}
```

Prüfe insbesondere:

```text
content/Glossar/
content/Themen/
content/Projekte/
content/LLM-Wiki/
content/Tools/
```

---

# Schritt 3: Build-Output prüfen

Build ausführen:

```bash
npx quartz build
```

Dann prüfen, welche HTML-Dateien wirklich erzeugt wurden:

```powershell
Get-ChildItem -Recurse public -File | Where-Object { $_.Name -match "index.html|Agent|API|Token|Transformer|AI|Machine|Prompt" } | Select-Object FullName
```

Zusätzlich die Ordnerstruktur prüfen:

```powershell
Get-ChildItem -Recurse public\Glossar -ErrorAction SilentlyContinue | Select-Object FullName
Get-ChildItem -Recurse public\Themen -ErrorAction SilentlyContinue | Select-Object FullName
```

Erwartung:

Für eine funktionierende URL wie

```text
/Glossar/Agent/
```

muss im Build normalerweise existieren:

```text
public/Glossar/Agent/index.html
```

oder eine äquivalente Quartz-Struktur, die diese Route bedient.

Wenn stattdessen z. B. nur dies existiert:

```text
public/Glossar/Agent.html
public/glossar/agent/index.html
public/Glossar/Agent%20/index.html
public/Glossar/Agent-/index.html
```

dann müssen Links oder Dateinamen angepasst werden.

---

# Schritt 4: Dateinamen und Routen standardisieren

Bitte saubere, Vercel-sichere Dateinamen verwenden.

## Standard

Für Einzeldateien:

```text
content/Glossar/Agent.md
content/Glossar/API.md
content/Glossar/Token.md
content/Glossar/Transformer.md
content/Glossar/Embedding.md
content/Glossar/Gradient-Descent.md
content/Glossar/Overfitting.md
```

Für Themen:

```text
content/Themen/AI-Agents.md
content/Themen/Algorithmen-und-Datenstrukturen.md
content/Themen/APIs-und-Web.md
content/Themen/Computer-Vision.md
content/Themen/Data-Analysis.md
content/Themen/Datenbanken.md
content/Themen/Deep-Learning.md
content/Themen/DevOps-und-Git.md
content/Themen/JavaScript-TypeScript.md
content/Themen/KI.md
content/Themen/LLM.md
content/Themen/Machine-Learning.md
content/Themen/Neural-Networks.md
content/Themen/NLP.md
content/Themen/Prompt-Engineering.md
content/Themen/Python.md
content/Themen/Reinforcement-Learning.md
```

Keine Leerzeichen in Dateinamen.

Keine Umlaute.

Keine doppelten Dateien mit ähnlichem Namen.

Nicht gleichzeitig:

```text
AI Agents.md
AI-Agents.md
AI_Agents.md
AI-Agents/index.md
```

Nur eine Variante behalten.

---

# Schritt 5: Frontmatter bereinigen

Jede Markdown-Datei soll minimales, sauberes Frontmatter haben.

Beispiel:

```md
---
title: Agent
tags:
  - glossar
  - ki
  - agents
---
```

Nicht verwenden, außer wirklich nötig:

```md
draft: true
publish: false
permalink:
slug:
aliases:
```

Bitte alle problematischen Felder entfernen oder korrigieren.

Besonders prüfen und entfernen:

```yaml
draft: true
publish: false
published: false
private: true
```

Diese können verursachen, dass Seiten nicht öffentlich gerendert werden.

---

# Schritt 6: README vs index.md prüfen

Ordnerseiten sollen stabil sein.

Für Ordner-Übersichtsseiten bevorzugt:

```text
content/Glossar/index.md
content/Themen/index.md
content/Projekte/index.md
content/LLM-Wiki/index.md
content/Tools/index.md
```

Nicht nur:

```text
README.md
```

Wenn aktuell `README.md` genutzt wird und Links/Routes Probleme machen, bitte auf `index.md` umstellen.

Beispiel:

```text
content/Glossar/index.md
```

Inhalt:

```md
---
title: Glossar
---

# Glossar

Kurze Erklärungen zentraler Begriffe.

- [[Glossar/Agent|Agent]]
- [[Glossar/API|API]]
- [[Glossar/Embedding|Embedding]]
- [[Glossar/Gradient-Descent|Gradient Descent]]
- [[Glossar/Overfitting|Overfitting]]
- [[Glossar/Token|Token]]
- [[Glossar/Transformer|Transformer]]
```

Für `content/Themen/index.md` entsprechend:

```md
---
title: Themen
---

# Themen

Thematische Einstiegspunkte.

- [[Themen/AI-Agents|AI Agents]]
- [[Themen/Machine-Learning|Machine Learning]]
- [[Themen/Prompt-Engineering|Prompt Engineering]]
```

---

# Schritt 7: Interne Links korrigieren

Alle internen Links müssen auf echte Dateien zeigen.

Bevorzugt:

```md
[[Glossar/Agent|Agent]]
[[Themen/AI-Agents|AI Agents]]
[[Themen/Machine-Learning|Machine Learning]]
```

Nicht:

```md
[[Agent]]
[[AI Agents]]
[[AI-Agents]]
[[Themen/AI Agents]]
```

Außer die Datei liegt exakt entsprechend.

Bitte mit Suche prüfen:

```powershell
Select-String -Path content\**\*.md -Pattern "\[\[" -AllMatches
```

Dann Links gegen vorhandene Dateien prüfen.

---

# Schritt 8: Case-Sensitivity fixen

Vercel/Linux ist case-sensitive.

Das funktioniert nicht zuverlässig, wenn Datei und Link anders geschrieben sind:

```text
Datei: content/Glossar/agent.md
Link:  [[Glossar/Agent]]
```

oder:

```text
Datei: content/themen/AI-Agents.md
Link:  [[Themen/AI-Agents]]
```

Bitte konsistent machen:

```text
Ordner: Glossar
Link:   Glossar

Ordner: Themen
Link:   Themen

Datei: Agent.md
Link:   Agent
```

Wenn Git unter Windows Umbenennungen nur in Groß-/Kleinschreibung nicht erkennt, dann über Zwischennamen arbeiten:

```bash
git mv content/glossar content/glossar_tmp
git mv content/glossar_tmp content/Glossar
```

oder bei Dateien:

```bash
git mv content/Glossar/agent.md content/Glossar/agent_tmp.md
git mv content/Glossar/agent_tmp.md content/Glossar/Agent.md
```

---

# Schritt 9: Lokale URLs testen

Nach Korrektur:

```bash
npx quartz build --serve
```

Dann im Browser prüfen:

```text
http://localhost:8080/
http://localhost:8080/Glossar/
http://localhost:8080/Glossar/Agent/
http://localhost:8080/Glossar/API/
http://localhost:8080/Themen/
http://localhost:8080/Themen/AI-Agents/
```

Wenn ohne Slash funktioniert, auch gut. Wichtig: Kein 404.

---

# Schritt 10: Vercel-spezifischen 404 prüfen

Wenn lokal alles funktioniert, aber Vercel weiterhin 404 zeigt:

1. Sicherstellen, dass Änderungen gepusht wurden:

```bash
git status
git log --oneline -5
git push
```

2. Vercel Deploy-Log prüfen.

3. Prüfen, ob Vercel den richtigen Branch nutzt:

```text
main
```

4. In Vercel ggf. Redeploy ohne Cache ausführen:

```text
Vercel Project
→ Deployments
→ Redeploy
→ Use existing Build Cache deaktivieren
```

---

# Schritt 11: Optional: URL-Redirects für alte Pfade

Falls bereits alte Links existieren, können Redirects ergänzt werden.

Nur wenn nötig.

In Vercel z. B. über `vercel.json`:

```json
{
  "redirects": [
    {
      "source": "/Themen/AI Agents",
      "destination": "/Themen/AI-Agents",
      "permanent": true
    }
  ]
}
```

Aber bevorzugt ist: Content-Dateien und Links korrekt machen.

---

# Schritt 12: Build und Commit

Wenn alles funktioniert:

```bash
npx quartz build
git status
git add .
git commit -m "Fix Quartz routes and content slugs"
git push
```

---

## Akzeptanzkriterien

Erledigt ist die Aufgabe erst, wenn diese URLs lokal und nach Vercel-Deploy funktionieren:

```text
/
 /Glossar/
 /Glossar/Agent/
 /Glossar/API/
 /Glossar/Token/
 /Glossar/Transformer/
 /Themen/
 /Themen/AI-Agents/
 /Themen/Machine-Learning/
 /Themen/Prompt-Engineering/
```

Zusätzlich:

- keine Hover-Vorschau zeigt 404 für existierende Explorer-Einträge
- Explorer-Links funktionieren
- Ordnerseiten funktionieren
- Startseitenlinks funktionieren
- `npx quartz build` läuft erfolgreich
- keine privaten Dateien wurden veröffentlicht

---

## Abschlussmeldung

Bitte nach Abschluss ausgeben:

```text
Erledigt:
- Content-Dateinamen geprüft und standardisiert
- Frontmatter bereinigt
- README/index-Struktur geprüft
- interne Links korrigiert
- lokale Routes getestet
- Build erfolgreich
- Änderungen gepusht

Geprüfte URLs:
- /
- /Glossar/
- /Glossar/Agent/
- /Glossar/API/
- /Themen/
- /Themen/AI-Agents/
```

Falls weiterhin 404 auftritt:

```text
Nicht erledigt:
- Betroffene URL:
- Erwartete Datei:
- Tatsächlich erzeugter Build-Pfad:
- Vermutete Ursache:
- Nächster Fix:
```
