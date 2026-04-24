---
tags: [prompt-engineering, llm, ki, prompting]
status: aktiv
typ: thema
quelle_anzahl: 2
zuletzt_aktualisiert: 2026-04-23
---

# Prompt Engineering

## Kurzbeschreibung
Prompt Engineering ist die Kunst und Wissenschaft, Eingaben für [[LLM]]s so zu formulieren, dass sie die gewünschten Ausgaben produzieren. Korrekte Prompts steigern Qualität, Konsistenz und Nützlichkeit drastisch.

## Relevanz
Ohne gute Prompts liefern selbst die besten Modelle schlechte Ergebnisse. Prompt Engineering ist die direkteste Form der LLM-Steuerung — ohne Fine-Tuning oder Code.

## Typische Fragestellungen
- Wie schreibe ich einen guten System Prompt?
- Wann nutze ich Few-Shot vs. Zero-Shot?
- Was ist Chain-of-Thought und wann hilft es?
- Wie verhindere ich, dass das Modell abschweift?
- Wie kann ich schlechte Prompts automatisch verbessern?

## Grundlegende Techniken

### Zero-Shot Prompting
Keine Beispiele, direkte Anweisung.
```
Erkläre mir Gradient Descent in einfachen Worten.
```

### Few-Shot Prompting
2–5 Beispiele mitgeben, Modell erkennt das Muster.
```
Eingabe: "Hund" → Ausgabe: "animal"
Eingabe: "Auto" → Ausgabe: "vehicle"
Eingabe: "Banane" → Ausgabe: ?
```

### Chain-of-Thought (CoT)
Modell soll Schritt für Schritt denken. Drastisch bessere Ergebnisse bei komplexen Aufgaben.
```
Denke Schritt für Schritt: Wenn Zug A um 9:00 Uhr abfährt...
```

### Tree-of-Thought (ToT)
Modell erkundet mehrere Denkpfade parallel. Für sehr schwierige Probleme.

### System Prompt
Grundlegende Anweisungen die das Modell-Verhalten definieren. Wird vor jedem User-Turn gesetzt.
```
Du bist ein hilfreicher Code-Assistent. Antworte präzise, 
ohne unnötige Erklärungen.
```

### Role Prompting
Modell in eine Rolle versetzen.
```
Du bist ein erfahrener Data Scientist. Erkläre mir...
```

### Instruction Following
Klare, strukturierte Anweisungen statt vage Fragen.
- Schlecht: "Schreib was über Python"
- Besser: "Erkläre in 3 Bullet Points die wichtigsten Python-Datenstrukturen für Data Science"

## Fortgeschrittene Konzepte

### Prompt-Pipeline / Multi-Step
Schwacher Rohprompt wird durch mehrere Stufen verbessert:
1. **Analyse**: Was ist das eigentliche Ziel?
2. **Verbesserung**: Prompt klarer formulieren
3. **Generierung**: Finale Ausgabe

Praxisbeispiel (Ollama lokal):
```python
def pipeline(raw_prompt, model="llama3.2"):
    analysis = llm(f"Analysiere: {raw_prompt}")
    improved = llm(f"Verbessere basierend auf Analyse '{analysis}': {raw_prompt}")
    return llm(f"Führe aus: {improved}")
```

### Output Format Control
LLM zur strukturierten Ausgabe zwingen:
```
Antworte nur als JSON mit Feldern: {"title": "...", "summary": "...", "tags": [...]}
```

### Prompt Injection
Angriff: Böswillige Eingabe überschreibt System Prompt. Wichtig bei produktiven Agents zu beachten.

### Temperature Tuning
- Für faktenbasierte Antworten: Temperature 0.0–0.3
- Für kreative Texte: Temperature 0.7–1.0

## Typische Fehler

| Fehler | Problem | Lösung |
|---|---|---|
| Zu vage | Modell rät | Konkrete Anforderungen |
| Zu lang | Modell verliert Fokus | Fokussieren, Priorisieren |
| Fehlende Beispiele | Modell versteht Format nicht | Few-Shot hinzufügen |
| Kein Output-Format | Unstrukturierte Ausgabe | JSON/Markdown vorgeben |
| Kein Role-Context | Generische Antworten | System Prompt setzen |

## Verwandte Themen
- [[LLM]]
- [[AI Agents]]
- [[Python]]

## Quellenbasis
- `GUI für Prompt-Optimierung` (2026-04-02) – Prompt-Pipeline mit Ollama, mehrstufige Verbesserung
- Allgemeines Wissen (Anthropic, OpenAI Prompt Engineering Guides)

## Siehe auch
- [[KI]]
- [[NLP]]
