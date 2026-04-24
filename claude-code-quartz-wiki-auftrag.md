# Auftrag für Claude Code: Portfolio-Wiki mit Quartz im bestehenden Repo vorbereiten

## Ausgangslage

Es gibt bereits:

1. Eine bestehende Portfolio-Seite, aktuell erreichbar unter:

```text
https://website-eight-lilac-81.vercel.app/
```

2. Ein bereits vorhandenes GitHub-Repo bzw. lokales Projekt für das Wiki:

```text
C:\Users\pasca\Documents\Claude\Projekte\website-wiki-quartz
```

Dieses Repo/Projekt soll für ein eigenständiges Quartz-Wiki verwendet werden.

---

## Ziel

Bereite im bestehenden Ordner

```text
C:\Users\pasca\Documents\Claude\Projekte\website-wiki-quartz
```

ein eigenständiges Quartz-Wiki-Projekt vor.

Das Wiki soll später als zusätzlicher Bereich zur Portfolio-Seite genutzt werden.

Ziel-Varianten:

```text
https://website-eight-lilac-81.vercel.app/wiki
```

oder sauberer als separates Vercel-Projekt/Subdomain:

```text
https://wiki.pascalpeters.info
```

Da die Portfolio-Seite bereits separat auf Vercel läuft, soll dieses Wiki-Projekt **nicht direkt in die bestehende Portfolio-App gemischt werden**.

Empfohlene Architektur:

```text
Portfolio-Projekt:
https://website-eight-lilac-81.vercel.app/

Wiki-Projekt:
separates Repo/Projekt website-wiki-quartz
später eigener Vercel-Deploy
```

Falls später `/wiki` auf der Portfolio-Seite genutzt werden soll, reicht dort eine Weiterleitung auf das Wiki-Projekt.

---

## Wichtig

Der Ordner und das Repo existieren bereits.

Deshalb:

- nichts blind überschreiben
- zuerst vorhandene Dateien prüfen
- bestehendes Git-Repo respektieren
- vorhandenen Remote nicht ersetzen
- keine bestehende Historie löschen
- kein neues verschachteltes Unterprojekt erzeugen
- `package.json` soll direkt im Projektordner liegen

Zielordner:

```text
C:\Users\pasca\Documents\Claude\Projekte\website-wiki-quartz
```

Nicht erzeugen:

```text
C:\Users\pasca\Documents\Claude\Projekte\website-wiki-quartz\website-wiki-quartz
```

---

## Gewünschte Projektstruktur

Am Ende soll die Struktur ungefähr so aussehen:

```text
website-wiki-quartz/
├─ content/
│  ├─ index.md
│  ├─ Projekte/
│  │  └─ README.md
│  ├─ LLM-Wiki/
│  │  └─ README.md
│  ├─ Tools/
│  │  └─ README.md
│  └─ Assets/
├─ docs/
│  ├─ vercel.md
│  └─ portfolio-redirect.md
├─ quartz/
├─ quartz.config.ts
├─ quartz.layout.ts
├─ package.json
├─ package-lock.json
├─ tsconfig.json
├─ .gitignore
└─ README.md
```

Wenn Quartz je nach Version leicht andere Dateien erzeugt, ist das okay. Wichtig ist: lauffähiger Quartz-Build, Content-Ordner, Graph, README und Vercel-Hinweise.

---

## Schritt 1: Bestehenden Zustand prüfen

Im Zielordner arbeiten:

```bash
cd C:\Users\pasca\Documents\Claude\Projekte\website-wiki-quartz
```

Prüfen:

```bash
dir
git status
git remote -v
```

Wenn bereits Dateien vorhanden sind:

- kurz analysieren
- keine Dateien löschen, außer eindeutig temporär/fehlerhaft
- falls Konflikte bestehen, vorher dokumentieren

Falls kein Git-Repo erkannt wird, aber der Ordner angeblich ein Repo sein soll, nicht blind neu initialisieren. Erst melden.

---

## Schritt 2: Quartz installieren oder initialisieren

Prüfe, ob bereits ein Quartz-Projekt vorhanden ist:

```text
quartz.config.ts
quartz.layout.ts
package.json
quartz/
```

### Fall A: Quartz ist bereits vorhanden

Dann nicht neu initialisieren.

Stattdessen:

```bash
npm install
```

und Konfiguration/Content gemäß diesem Auftrag anpassen.

### Fall B: Quartz ist noch nicht vorhanden

Initialisiere Quartz im bestehenden Ordner.

Falls `npm create quartz@latest` nicht direkt in den aktuellen Ordner schreiben kann, dann temporär erzeugen:

```bash
cd C:\Users\pasca\Documents\Claude\Projekte
npm create quartz@latest website-wiki-quartz-temp
```

Danach die nötigen Quartz-Dateien aus `website-wiki-quartz-temp` in den bestehenden Zielordner kopieren.

Wichtig:

- vorhandene Dateien im Zielordner nicht blind überschreiben
- bei Konflikten vorher prüfen
- temporären Ordner danach entfernen, wenn alles sauber kopiert wurde

Falls Node.js oder npm fehlen, abbrechen und klar melden, was installiert werden muss.

---

## Schritt 3: Content-Struktur vorbereiten

Erstelle, falls nicht vorhanden:

```text
content
content/Projekte
content/LLM-Wiki
content/Tools
content/Assets
```

Erstelle oder aktualisiere:

```text
content/index.md
```

Inhalt:

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

## Zweck

Dieses Wiki dient als strukturierter öffentlicher Wissensbereich neben meiner Portfolio-Seite.

Die bestehende Portfolio-Seite läuft aktuell hier:

https://website-eight-lilac-81.vercel.app/

Das Wiki soll bewusst getrennt davon aufgebaut werden, damit Portfolio und Wiki unabhängig deploybar bleiben.

Später können ausgewählte Obsidian-Notizen hier ergänzt werden, ohne den kompletten privaten Vault zu veröffentlichen.
```

Erstelle oder aktualisiere:

```text
content/Projekte/README.md
```

Inhalt:

```md
---
title: Projekte
---

# Projekte

Sammlung öffentlicher Projekt-Notizen.

## Beispiele

- Portfolio Website
- Ollama GUI
- Quartz Wiki
- Automatisierungen
```

Erstelle oder aktualisiere:

```text
content/LLM-Wiki/README.md
```

Inhalt:

```md
---
title: LLM-Wiki
---

# LLM-Wiki

Notizen zu LLMs, Prompting, lokalen Modellen, Agenten, Workflows und Wissensmanagement.

## Mögliche Themen

- Prompting
- Claude Code
- Codex
- OpenClaw
- Ollama
- Obsidian Knowledge Base
```

Erstelle oder aktualisiere:

```text
content/Tools/README.md
```

Inhalt:

```md
---
title: Tools
---

# Tools

Sammlung technischer Tools, Setups und Arbeitsabläufe.

## Mögliche Themen

- Git
- Vercel
- Node.js
- Quartz
- Obsidian
```

---

## Schritt 4: Graph und Backlinks aktivieren

Öffne:

```text
quartz.layout.ts
```

Prüfe, ob `Component.Graph()` vorhanden ist.

Falls nicht vorhanden, füge den Graph in die rechte Sidebar ein.

Ziel:

```ts
Component.Graph()
Component.Backlinks()
```

sollen im Layout vorhanden sein.

Falls die Quartz-Version anders aufgebaut ist, versionsgerecht anpassen. Nicht stumpf Code einfügen, wenn dadurch TypeScript bricht.

Erwartung:

- Graph-Ansicht sichtbar
- Backlinks sichtbar
- Navigation bleibt funktional
- TypeScript bleibt gültig

---

## Schritt 5: Quartz-Konfiguration anpassen

Öffne:

```text
quartz.config.ts
```

Setze oder prüfe sinngemäß:

```ts
pageTitle: "Pascal Peters Wiki"
```

Für die aktuelle Vercel-Testdomain kann vorerst verwendet werden:

```ts
baseUrl: "website-eight-lilac-81.vercel.app"
```

Wichtig:

- `baseUrl` ohne `https://`
- keine harte `/wiki`-Base setzen
- wenn später `wiki.pascalpeters.info` genutzt wird, dann ändern auf:

```ts
baseUrl: "wiki.pascalpeters.info"
```

Falls Quartz in der verwendeten Version keine `baseUrl` verlangt oder anders strukturiert ist, versionsgerecht lösen.

---

## Schritt 6: README für das bestehende Repo erstellen/aktualisieren

Erstelle oder aktualisiere:

```text
README.md
```

Inhalt:

````md
# Website Wiki Quartz

Eigenständiges Quartz-Wiki als zusätzlicher Wissensbereich zur Portfolio-Seite.

## Ausgangslage

Die bestehende Portfolio-Seite läuft aktuell hier:

```text
https://website-eight-lilac-81.vercel.app/
```

Dieses Repo enthält das separate Wiki-Projekt:

```text
website-wiki-quartz
```

## Ziel

Dieses Projekt rendert ausgewählte Markdown-/Obsidian-Notizen als statische Website.

Geplanter Einsatz:

- Portfolio: bestehende Vercel-Seite
- Wiki: separates Quartz-Projekt
- Deployment: Vercel
- mögliche spätere Domain: `wiki.pascalpeters.info`

## Warum separat?

Portfolio und Wiki sollen unabhängig bleiben.

Vorteile:

- Portfolio-Build wird nicht durch Quartz beeinflusst
- Wiki kann unabhängig deployt werden
- Obsidian-/Markdown-Struktur bleibt sauber getrennt
- später einfache Verlinkung über `/wiki` möglich

## Lokale Entwicklung

```bash
npm install
npx quartz build --serve
```

Danach öffnen:

```text
http://localhost:8080
```

## Build

```bash
npx quartz build
```

Der statische Output liegt anschließend in:

```text
public/
```

## Vercel Einstellungen

Für das Wiki-Projekt:

```text
Framework Preset: Other
Install Command: npm install
Build Command: npx quartz build
Output Directory: public
Root Directory: ./
```

## Content

Öffentliche Inhalte liegen in:

```text
content/
```

Nicht den kompletten privaten Obsidian Vault hier ablegen.

Nur Inhalte veröffentlichen, die bewusst öffentlich sichtbar sein dürfen.

## Portfolio-Verlinkung

Empfohlener Weg:

```text
Portfolio-Seite /wiki
→ Redirect auf das Wiki-Projekt
```

Beispielziel:

```text
https://wiki.pascalpeters.info
```

oder während der Testphase die jeweilige Vercel-Preview/Production-URL des Wiki-Projekts.
````

---

## Schritt 7: .gitignore prüfen

Erstelle oder ergänze `.gitignore`:

```gitignore
node_modules/
public/
.quartz-cache/
.DS_Store
Thumbs.db
.env
.env.local
```

Wichtig:

- `content/` darf nicht ignoriert werden
- `package-lock.json` soll versioniert werden
- keine privaten Vault-Ordner versehentlich committen

---

## Schritt 8: Vercel-Dokumentation erstellen

Erstelle:

```text
docs/vercel.md
```

Inhalt:

```md
# Vercel Deployment

## Bestehende Portfolio-Seite

Aktuelle Portfolio-Seite:

```text
https://website-eight-lilac-81.vercel.app/
```

## Wiki-Projekt

Dieses Projekt ist ein separates Quartz-Wiki.

Empfohlene Vercel-Einstellungen:

```text
Framework Preset: Other
Install Command: npm install
Build Command: npx quartz build
Output Directory: public
Root Directory: ./
```

## Domain

Während der Entwicklung nutzt Vercel eine automatisch generierte Projekt-URL.

Später empfohlen:

```text
wiki.pascalpeters.info
```

Dann in `quartz.config.ts` setzen:

```ts
baseUrl: "wiki.pascalpeters.info"
```

## Verbindung zur Portfolio-Seite

Empfohlen:

```text
https://website-eight-lilac-81.vercel.app/wiki
```

leitet weiter auf die Wiki-Domain oder Wiki-Vercel-URL.

Portfolio und Wiki bleiben dadurch sauber getrennt.
```

---

## Schritt 9: Redirect-Dokumentation für Portfolio erstellen

Erstelle:

```text
docs/portfolio-redirect.md
```

Inhalt:

````md
# Portfolio Redirect zu Wiki

Die Portfolio-Seite läuft aktuell hier:

```text
https://website-eight-lilac-81.vercel.app/
```

Das Wiki soll separat deployt werden.

## Variante Next.js App Router

Falls die Portfolio-Seite Next.js mit App Router nutzt, kann eine Route angelegt werden:

```tsx
// app/wiki/page.tsx
import { redirect } from "next/navigation";

export default function WikiPage() {
  redirect("https://wiki.pascalpeters.info");
}
```

Während der Testphase kann statt `wiki.pascalpeters.info` die Vercel-URL des Wiki-Projekts verwendet werden.

## Variante einfacher Link

Alternativ reicht in der Navigation ein normaler Link:

```tsx
<a href="https://wiki.pascalpeters.info">Wiki</a>
```

oder vorläufig:

```tsx
<a href="https://DEINE-WIKI-VERCEL-URL.vercel.app">Wiki</a>
```

## Wichtig

Nicht in diesem Wiki-Projekt direkt die Portfolio-Dateien verändern.

Dieses Dokument ist nur eine Vorlage für das separate Portfolio-Projekt.
````

---

## Schritt 10: Lokalen Build testen

Führe im Zielordner aus:

```bash
npm install
npx quartz build
```

Wenn erfolgreich, teste lokal:

```bash
npx quartz build --serve
```

Erwartetes Ergebnis:

```text
http://localhost:8080
```

Die Seite soll zeigen:

- Startseite
- Links zu Projekte, LLM-Wiki und Tools
- Graph-Ansicht
- Backlinks, sofern vom Layout vorgesehen

---

## Schritt 11: Git prüfen und Commit vorbereiten

Da das Repo bereits existiert:

```bash
git status
git remote -v
```

Nicht den Remote ändern.

Dann:

```bash
git add .
git commit -m "Prepare Quartz wiki project"
```

Falls noch kein Remote vorhanden ist, nur melden:

```text
Kein Git Remote vorhanden. Bitte GitHub-Repo verbinden.
```

Falls ein Remote vorhanden ist:

```bash
git push
```

Nur pushen, wenn der aktuelle Branch klar ist und keine unerwarteten Änderungen vorhanden sind.

---

## Schritt 12: Sicherheitsprüfung vor Commit/Push

Vor dem finalen Commit prüfen:

- keine `.env`
- keine API-Keys
- keine privaten Chat-Exporte
- keine Firmendaten
- keine internen Arbeitsnotizen
- keine sensiblen Obsidian-Dateien
- keine kompletten privaten Vault-Ordner
- keine versehentlich kopierten `node_modules`
- kein `public/` Build-Output, falls ignoriert

Nur Beispielinhalte in `content/` verwenden.

---

## Akzeptanzkriterien

Die Aufgabe gilt als erledigt, wenn:

1. Das bestehende Repo im Ordner `website-wiki-quartz` weiterverwendet wurde.
2. Es wurde kein verschachtelter Projektordner erzeugt.
3. Ein lauffähiges Quartz-Projekt liegt direkt im Zielordner.
4. `npm install` funktioniert.
5. `npx quartz build` erfolgreich läuft.
6. `npx quartz build --serve` lokal eine Website startet.
7. `content/index.md` existiert.
8. Beispielbereiche `Projekte`, `LLM-Wiki`, `Tools` existieren.
9. Graph und Backlinks sind aktiviert oder nachvollziehbar dokumentiert.
10. README enthält lokale Startbefehle, Vercel-Build-Einstellungen und Hinweis auf die bestehende Portfolio-Seite.
11. `docs/vercel.md` existiert.
12. `docs/portfolio-redirect.md` existiert.
13. `.gitignore` ist sinnvoll gesetzt.
14. Es wurden keine privaten Vault-Inhalte veröffentlicht.

---

## Ausgabe nach Abschluss

Am Ende bitte kurz ausgeben:

```text
Erledigt:
- Bestehendes Repo geprüft
- Quartz-Projekt vorbereitet
- Content-Struktur erstellt
- Graph/Backlinks geprüft
- Build getestet
- README und Vercel-Hinweise erstellt
- Portfolio-Redirect dokumentiert

Nächste Schritte:
1. Wiki-Projekt in Vercel importieren oder bestehendes Vercel-Projekt verbinden
2. Vercel Build Settings setzen
3. Wiki-Vercel-URL testen
4. Optional Domain wiki.pascalpeters.info setzen
5. In der Portfolio-Seite /wiki als Redirect oder Link ergänzen
```

Falls etwas nicht funktioniert, bitte direkt:

- Fehler nennen
- betroffene Datei nennen
- genauen Befehl nennen
- konkrete Lösung vorschlagen
