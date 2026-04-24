---
tags: [api, rest, http, web, fastapi, backend]
status: aktiv
typ: thema
quelle_anzahl: 3
zuletzt_aktualisiert: 2026-04-23
---

# APIs und Web

## Kurzbeschreibung
APIs (Application Programming Interfaces) sind die Schnittstellen zwischen Systemen. REST-APIs sind der Standard für Web-Backend-Kommunikation. Im KI-Kontext: LLM-APIs, ML-Model-Serving, Agent-Backends.

## Relevanz
Jede KI-Anwendung die nicht lokal und isoliert läuft, kommuniziert über APIs. LLM-Provider (OpenAI, Anthropic) bieten REST-APIs. Eigene ML-Modelle werden über APIs bereitgestellt.

## Typische Fragestellungen
- Was ist REST und wie funktioniert es?
- HTTP-Methoden: GET, POST, PUT, DELETE – wann was?
- Wie authentifiziere ich mich an einer API?
- Wie baue ich eine eigene API mit FastAPI?
- Was sind Status-Codes?

## REST-Grundlagen

### HTTP-Methoden

| Methode | Zweck | Beispiel |
|---|---|---|
| GET | Daten abrufen | `GET /users/123` |
| POST | Neue Ressource erstellen | `POST /analyze` |
| PUT | Ressource ersetzen | `PUT /users/123` |
| PATCH | Ressource teilweise aktualisieren | `PATCH /users/123` |
| DELETE | Ressource löschen | `DELETE /users/123` |

### HTTP Status-Codes

| Code | Bedeutung |
|---|---|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |

### REST-Prinzipien
- Zustandslos (Stateless)
- Client-Server-Trennung
- Einheitliche Schnittstelle
- Ressourcen über URLs adressiert

## FastAPI (Python)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AnalyzeRequest(BaseModel):
    image_url: str
    model: str = "gpt-4o"

@app.post("/analyze")
async def analyze_ui(req: AnalyzeRequest):
    if not req.image_url:
        raise HTTPException(status_code=400, detail="image_url required")
    # ... LLM-Aufruf
    return {"findings": [], "suggestions": []}

@app.get("/health")
def health():
    return {"status": "ok"}
```

Start: `uvicorn main:app --reload`
Docs: `http://localhost:8000/docs`

## Authentifizierung

| Methode | Beschreibung | Wann |
|---|---|---|
| API Key | Header: `Authorization: Bearer sk-...` | Einfache APIs |
| OAuth 2.0 | Token-basiert, delegiert | Nutzer-Auth |
| JWT | JSON Web Token, selbst-enthaltend | Stateless Auth |
| Basic Auth | Base64 encoded user:pass | Nur intern |

## LLM-API-Nutzung

### OpenAI API
```python
from openai import OpenAI
client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hallo"}]
)
print(response.choices[0].message.content)
```

### Anthropic API
```python
import anthropic
client = anthropic.Anthropic(api_key="sk-ant-...")
message = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hallo"}]
)
```

### Ollama (lokal)
```python
import requests
r = requests.post("http://localhost:11434/api/generate",
    json={"model": "llama3.2", "prompt": "Hallo", "stream": False})
print(r.json()["response"])
```

## GraphQL vs REST
- **REST**: Mehrere Endpoints, über-/unter-fetching möglich
- **GraphQL**: Ein Endpoint, Client bestimmt Datenstruktur

## Verwandte Themen
- [[Python]]
- [[JavaScript-TypeScript]]
- [[AI Agents]]
- [[LLM]]

## Quellenbasis
- `RESTful API Explained` (2024-06-24)
- `AI-basierte UX-Analyse` (2025-09-27) – FastAPI-Backend
- `GUI für Prompt-Optimierung` (2026-04-02) – Ollama API

## Siehe auch
- [[DevOps und Git]]
- [[Datenbanken]]
