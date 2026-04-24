---
tags: [javascript, typescript, web, frontend, nodejs]
status: aktiv
typ: thema
quelle_anzahl: 3
zuletzt_aktualisiert: 2026-04-23
---

# JavaScript / TypeScript

## Kurzbeschreibung
JavaScript ist die Sprache des Webs. TypeScript erweitert JavaScript um statische Typen. Node.js bringt JavaScript auf den Server. Relevant im KI-Kontext für Web-Frontends, APIs und Tool-Builds.

## Relevanz
Web-Frontends für KI-Tools, Next.js-Backends für ML-APIs, Browser-basierte Demos und Visualisierungen.

## Typische Fragestellungen
- JavaScript vs. TypeScript: Wann was?
- Wie baue ich eine Web-UI für ein LLM-Backend?
- Was ist Node.js und wann nutze ich es?
- React vs. vanilla JS – wann welches?
- Wie rufe ich eine REST-API aus dem Browser ab?

## JavaScript Grundlagen

### Variablen und Typen
```javascript
const name = "Alice";    // unveränderlich
let count = 0;           // veränderlich
var old = "veraltet";    // nicht mehr empfohlen
```

### Arrow Functions
```javascript
const add = (a, b) => a + b;
const greet = name => `Hallo ${name}`;
```

### Async/Await
```javascript
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
```

### Array-Methoden
```javascript
const doubled = [1,2,3].map(x => x * 2);
const evens = [1,2,3,4].filter(x => x % 2 === 0);
const sum = [1,2,3].reduce((acc, x) => acc + x, 0);
```

## TypeScript

### Typen
```typescript
interface User {
    id: number;
    name: string;
    email?: string;  // optional
}

function greet(user: User): string {
    return `Hallo ${user.name}`;
}
```

### Generics
```typescript
function identity<T>(arg: T): T {
    return arg;
}
```

## Ökosystem

| Tool/Framework | Zweck |
|---|---|
| React | UI-Komponenten, State Management |
| Next.js | React + Server-Side-Rendering, Fullstack |
| Vue.js | Alternative zu React |
| Node.js | JavaScript auf dem Server |
| Express.js | Minimales Node.js-Backend |
| npm/pnpm | Paketmanager |
| Webpack/Vite | Build-Tools |
| TypeScript | Typsicheres JavaScript |

## Praxis: API-Aufruf zu LLM-Backend

```javascript
async function improvePrompt(rawPrompt) {
    const response = await fetch("/api/improve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: rawPrompt })
    });
    const { improved } = await response.json();
    return improved;
}
```

## HTML-Templates
```html
<!DOCTYPE html>
<html>
<head>
    <title>KI-Tool</title>
</head>
<body>
    <div id="app"></div>
    <script>
        // Template-Logik
        const template = document.getElementById("template");
    </script>
</body>
</html>
```

## Verwandte Themen
- [[APIs und Web]]
- [[Python]]
- [[DevOps und Git]]

## Quellenbasis
- `Templates in HTML nutzen` (2024-06-23) – JavaScript HTML-Templates
- `AI-basierte UX-Analyse` (2025-09-27) – Next.js Frontend für KI-Tool
- `Domain und Webhosting` (2026-03-18)

## Siehe auch
- [[Datenbanken]]
- [[Algorithmen und Datenstrukturen]]
