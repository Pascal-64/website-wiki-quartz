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
