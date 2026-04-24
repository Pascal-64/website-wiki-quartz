---
title: Transformer
tags: [glossar, deep-learning, llm, architektur]
---

# Transformer

## Definition
Transformer ist eine neuronale Netz-Architektur aus dem Paper "Attention Is All You Need" (2017, Google). Basis für alle modernen [[LLM]]s (GPT, BERT, Claude, Gemini) und viele [[Computer Vision]]-Modelle.

## Kernkomponenten

### Self-Attention
Jedes Token "schaut" auf alle anderen Tokens und gewichtet ihre Relevanz. Ermöglicht Langzeitabhängigkeiten ohne Rekurrenz.

### Multi-Head Attention
Mehrere parallele Attention-Mechanismen → verschiedene Aspekte des Kontexts gleichzeitig.

### Feed-Forward Network
Nach Attention: simples vollverbundenes Netz pro Token.

### Positional Encoding
Da keine Rekurrenz: Position der Tokens wird als Vektor kodiert.

## Encoder vs. Decoder

| Typ | Beispiele | Aufgabe |
|---|---|---|
| Encoder | BERT | Verstehen, Klassifikation |
| Decoder | GPT | Text generieren |
| Encoder-Decoder | T5, BART | Übersetzen, Zusammenfassen |

## Verwandte Begriffe
- [[Token]] → Input des Transformers
- [[Embedding]] → Darstellung der Tokens
- [[Attention Mechanism]] → Kern des Transformers

## Verweise
- [[LLM]]
- [[Deep Learning]]
- [[Neural Networks]]
