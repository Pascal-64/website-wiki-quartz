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
