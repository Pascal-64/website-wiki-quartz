---
tags: [agents, ki, llm, automation, langchain]
status: aktiv
typ: thema
quelle_anzahl: 4
zuletzt_aktualisiert: 2026-04-23
---

# AI Agents

## Kurzbeschreibung
AI Agents sind autonome KI-Systeme die Aufgaben selbstständig planen, ausführen und dabei Werkzeuge (Tools) nutzen. Basis ist meist ein [[LLM]] als Denkinstanz. Der Agent bekommt ein Ziel und entscheidet selbst über die nächsten Schritte.

## Relevanz
Agents sind der Übergang von Chatbots zu echten KI-Arbeitern. Sie können Code ausführen, Webseiten durchsuchen, APIs aufrufen, Dateien bearbeiten – alles ohne manuellen Eingriff.

## Typische Fragestellungen
- Was ist der Unterschied zwischen Chatbot und Agent?
- Welche Agent-Frameworks gibt es?
- Wie baut man einen eigenen Agenten?
- Wann lohnt sich ein Multi-Agent-System?
- Wo werden Agents in der Praxis eingesetzt?

## Kernkonzepte

### ReAct-Pattern (Reason + Act)
Standard-Architektur für Agents:
1. **Reason**: Agent überlegt: "Was ist der nächste Schritt?"
2. **Act**: Agent führt eine Aktion aus (Tool-Call)
3. **Observe**: Agent liest das Ergebnis
4. Zurück zu 1 bis Ziel erreicht

### Tools / Function Calling
Agents bekommen Werkzeuge: Web-Suche, Code-Ausführung, Dateioperationen, API-Calls. LLM entscheidet wann welches Tool genutzt wird.

### Memory (Gedächtnis)
- **Short-Term**: Aktueller Kontext-Verlauf
- **Long-Term**: Externe Datenbank (Vector Store), wird bei Bedarf abgerufen
- **Episodic**: Erinnerung an frühere Interaktionen

### Orchestration
Bei Multi-Agent-Systemen: Ein Orchestrator-Agent verteilt Aufgaben an spezialisierte Sub-Agents.

### Plan-and-Execute
Agent erstellt zuerst einen Plan, dann führt er jeden Schritt aus. Gut für komplexe mehrstufige Aufgaben.

## Agent-Frameworks

| Framework | Sprache | Besonderheit |
|---|---|---|
| LangChain | Python | Umfassend, viele Integrationen |
| LangGraph | Python | Graph-basierte Agent-Workflows |
| CrewAI | Python | Multi-Agent-Koordination |
| AutoGen | Python | Microsoft, Multi-Agent |
| smolagents | Python | Hugging Face, leichtgewichtig |
| OpenAI Assistants API | API | Function Calling, Thread-Memory |
| Anthropic Claude API | API | Tool Use, direkt integrierbar |

## Praxis: Lokaler Agent mit Ollama

```python
import requests

def call_llm(prompt: str, model="llama3.2") -> str:
    r = requests.post("http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False})
    return r.json()["response"]

# Einfache Prompt-Pipeline als Proto-Agent
def improve_prompt(raw_prompt: str) -> str:
    analysis = call_llm(f"Analysiere diesen Prompt: {raw_prompt}")
    improved = call_llm(f"Verbessere diesen Prompt basierend auf: {analysis}\nOriginal: {raw_prompt}")
    return improved
```

## Einsatzbereiche (USA, 2026)

Laut US-Marktdaten (PwC, McKinsey):
1. **Kundenservice / Contact Center** (57% Unternehmen)
2. **Sales & Marketing** (54%)
3. **IT / Helpdesk / Cybersecurity** (53%)
4. **Wissensmanagement / Research**
5. **Software Engineering / Coding**

Deutschland hinkt nach: Stärker in Kundenkontakt und Marketing, schwächer in IT-Prozessen.

### Wichtige Agent-Plattformen
- **ChatGPT Agent** (OpenAI): Pro/Plus/Team. Kombiniert Research + Operator. 40–400 Tasks/Monat.
- **Claude** (Anthropic): Tool Use, Code-Ausführung, Dateiverarbeitung.
- **Copilot** (Microsoft): In Office-Integration, IT-Workflows.
- **Gemini** (Google): Google-Workspace-Integration.

## Unterthemen
- [[Prompt Engineering]] – Wie man Agents steuert
- [[LLM]] – Die Denkinstanz des Agents
- [[APIs und Web]] – Tools des Agents

## Verwandte Themen
- [[LLM]]
- [[Prompt Engineering]]
- [[Python]]
- [[APIs und Web]]

## Quellenbasis
- `Agent Nutzungsmöglichkeiten` (2025-07-22)
- `Meistgenutzte AI-Agents USA` (2026-04-08)
- `GUI für Prompt-Optimierung` (2026-04-02) – lokaler Agent mit Ollama
- `Chat Export für Obsidian` (2026-04-13)

## Siehe auch
- [[KI]]
- [[Machine Learning]]
