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
