---
tags: [nlp, natural-language-processing, ml, ki, text]
status: aktiv
typ: thema
zuletzt_aktualisiert: 2026-04-23
---

# NLP – Natural Language Processing

## Kurzbeschreibung
Natural Language Processing ist das Teilgebiet der [[KI]] das sich mit der Verarbeitung und dem Verstehen natürlicher Sprache befasst. NLP ist die Grundlage für [[LLM]]s, Übersetzungen, Sentiment-Analyse und vieles mehr.

## Relevanz
NLP ist überall: Suchmaschinen, Chatbots, Übersetzungen, Autocorrect, Spam-Filter, Dokumentenanalyse, Code-Generierung.

## Typische Fragestellungen
- Wie funktioniert Tokenisierung?
- Was ist ein Word Embedding?
- Wie analysiere ich Sentiment?
- Named Entity Recognition – was ist das?
- Transformer vs. RNN für NLP?

## Kernaufgaben

| Aufgabe | Beschreibung | Beispiel |
|---|---|---|
| Tokenisierung | Text in Tokens zerlegen | "Hallo Welt" → ["Hallo", "Welt"] |
| POS-Tagging | Wortarten erkennen | "laufe" → Verb |
| Named Entity Recognition | Entitäten erkennen | "Berlin" → Ort, "Merkel" → Person |
| Sentiment Analysis | Stimmung erkennen | "super!" → positiv |
| Text Classification | Text kategorisieren | Spam / Nicht-Spam |
| Machine Translation | Übersetzen | DE → EN |
| Summarization | Zusammenfassen | Langer Text → Kurzzusammenfassung |
| Question Answering | Fragen beantworten | über Textdokument |

## Kernkonzepte

### [[Tokenisierung]]
Text wird in kleinste Einheiten (Tokens) zerlegt.
- Word-Level: "machine learning" → ["machine", "learning"]
- Subword (BPE): "unhappy" → ["un", "happy"] — Standard für LLMs
- Character-Level: Zeichen für Zeichen

### [[Embedding]]
Wörter oder Tokens werden als Vektoren im mehrdimensionalen Raum dargestellt. Ähnliche Bedeutungen → ähnliche Vektoren.
- Word2Vec, GloVe: Klassische Word Embeddings
- Sentence Transformers: Satz-Embeddings
- LLM-Embeddings: Kontextbezogen, state-of-the-art

### Attention Mechanism
Ermöglicht dem Modell auf relevante Teile des Inputs zu fokussieren. Basis des [[Transformer]]-Modells. Self-Attention: Wörter "schauen" aufeinander.

### Transformers in NLP
- **BERT**: Bidirektional, Sprachverständnis, kein Text-Generator
- **GPT**: Unidirektional (links→rechts), Text-Generator
- **T5/BART**: Encoder-Decoder, Übersetzung/Zusammenfassung

## NLP-Bibliotheken (Python)

| Bibliothek | Stärken |
|---|---|
| spaCy | Schnell, Production-ready, NER, POS |
| NLTK | Klassisch, für Lehre und Prototypen |
| HuggingFace Transformers | State-of-the-art Modelle, einfache API |
| Sentence-Transformers | Satz-Embeddings, semantische Suche |
| Gensim | Word2Vec, Topic Modeling |

## Beispiel: Sentiment mit HuggingFace
```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
result = classifier("Das Produkt ist fantastisch!")
# [{'label': 'POSITIVE', 'score': 0.9998}]
```

## Verwandte Themen
- [[LLM]]
- [[Deep Learning]]
- [[Machine Learning]]
- [[Embedding]] (Glossar)

## Quellenbasis
- `AI-basierte UX-Analyse` (2025-09-27) – NLP für UI-Texterkennung
- Allgemeines Wissen

## Siehe auch
- [[Computer Vision]]
- [[Prompt Engineering]]
