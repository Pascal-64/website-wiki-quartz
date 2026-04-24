---
tags: [llm, ki, transformer, gpt, claude]
status: aktiv
typ: thema
quelle_anzahl: 3
zuletzt_aktualisiert: 2026-04-23
---

# LLM – Large Language Models

## Kurzbeschreibung
Large Language Models sind KI-Modelle die auf riesigen Textmengen trainiert wurden und Sprache verstehen und generieren können. Basis: [[Transformer]]-Architektur. Bekannteste Vertreter: GPT-4, Claude, Gemini, Llama.

## Relevanz
LLMs sind der Kern moderner [[KI]]-Anwendungen. Sie sind Grundlage für [[AI Agents]], [[Prompt Engineering]], [[NLP]]-Aufgaben und Code-Generierung.

## Typische Fragestellungen
- Welches Modell für welche Aufgabe?
- Wie funktioniert Tokenisierung?
- Was ist ein Context Window?
- Lokal vs. Cloud-Modell: Wann was?
- Was ist RAG und wann sinnvoll?
- Wie reduziere ich Halluzinationen?

## Kernkonzepte

### Tokenisierung
Text wird in [[Token]]s zerlegt. Ein Token entspricht ca. 3–4 Zeichen. Modelle denken in Tokens, nicht Wörtern.

### Context Window
Maximale Anzahl Tokens die ein Modell gleichzeitig verarbeiten kann. GPT-4: 128k. Claude: 200k. Llama 3.2: 128k.

### Temperature & Sampling
- **Temperature**: Kreativität/Zufälligkeit. 0 = deterministisch. 1+ = kreativ.
- **Top-P**: Wahrscheinlichkeitsschwelle für Token-Auswahl.
- **Top-K**: Nur die Top-K wahrscheinlichsten Tokens werden gewählt.

### Embeddings
Vektordarstellungen von Text. [[Embedding]]s ermöglichen semantische Suche und RAG.

### Halluzination
LLMs erfinden manchmal plausibel klingende aber falsche Fakten. Gegenmaßnahmen: RAG, Grounding, Fact-Checking.

### RAG (Retrieval-Augmented Generation)
Externe Wissensdatenbank wird bei jeder Anfrage durchsucht und als Kontext mitgegeben. Reduziert Halluzinationen für domänenspezifisches Wissen.

### Fine-Tuning
Ein vortrainiertes Modell wird auf speziellen Daten weitertrainiert. Aufwändig, aber ermöglicht sehr spezifisches Verhalten.

### RLHF
Reinforcement Learning from Human Feedback. Methode um LLMs durch menschliches Feedback zu verbessern. Genutzt bei GPT, Claude etc.

## Lokale vs. Cloud-Modelle

| Aspekt | Lokal (Ollama, LM Studio) | Cloud (OpenAI, Anthropic) |
|---|---|---|
| Datenschutz | Vollständig lokal | Daten beim Anbieter |
| Kosten | Hardware-Einmalkosten | Pro-Token-Kosten |
| Qualität | Kleiner (7B–70B) | Größer (>100B) |
| Latenz | Abhängig von Hardware | Gut optimiert |
| Offline | Ja | Nein |

### Lokale Hosting-Tools
- **Ollama**: Einfachstes lokales LLM-Deployment. REST-API auf `localhost:11434`.
- **LM Studio**: GUI-Tool für lokale LLMs.
- **llama.cpp**: C++-Engine für effiziente LLM-Inferenz.

Beispiel Ollama API:
```python
import requests
response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2",
    "prompt": "Erkläre mir Gradient Descent",
    "stream": False
})
print(response.json()["response"])
```

## Wichtige Modelle (Stand 2026)

| Modell | Anbieter | Typ | Besonderheit |
|---|---|---|---|
| GPT-4o | OpenAI | Cloud | Multimodal, stark |
| Claude 3.5/4.x | Anthropic | Cloud | Langer Context, sicher |
| Gemini 2.x | Google | Cloud | Google-Integration |
| Llama 3.x (8B/70B) | Meta | Open-Source | Lokal nutzbar |
| Mistral 7B | Mistral AI | Open-Source | Effizient |
| Phi-3/4 | Microsoft | Open-Source | Small, schnell |

## Unterthemen
- [[Prompt Engineering]] – Wie man LLMs steuert
- [[AI Agents]] – LLMs als Entscheidungsinstanz
- [[Transformer]] (Glossar) – Architektur
- [[Embedding]] (Glossar) – Vektordarstellung

## Verwandte Themen
- [[KI]]
- [[Deep Learning]]
- [[NLP]]
- [[AI Agents]]
- [[Prompt Engineering]]

## Quellenbasis
- `GUI für Prompt-Optimierung` (2026-04-02) – Ollama-Nutzung, lokales Deployment, Prompt-Pipeline
- `Meistgenutzte AI-Agents USA` (2026-04-08) – LLM-Marktüberblick
- `Agent Nutzungsmöglichkeiten` (2025-07-22) – ChatGPT Agent-Funktionen

## Siehe auch
- [[Neural Networks]]
- [[Algorithmen und Datenstrukturen]]
