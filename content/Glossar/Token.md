---
title: Token
tags: [glossar, llm, nlp]
---

# Token

## Definition
Die kleinste Verarbeitungseinheit eines [[LLM]]s. Text wird vor der Verarbeitung in Tokens zerlegt (Tokenisierung). Ein Token entspricht je nach Sprache ca. 3–4 Zeichen oder einem halben Wort.

## Kontext
LLMs "sehen" keinen Text direkt, sondern Sequenzen von Token-IDs. Das Modell-Limit (Context Window) wird in Tokens gemessen, nicht in Zeichen oder Wörtern.

Beispiel (GPT-Tokenizer):
- "machine learning" → 2 Tokens
- "Maschinelles Lernen" → 4 Tokens
- Deutsch/Chinesisch braucht oft mehr Tokens als Englisch

## Verwandte Begriffe
- [[Tokenisierung]] → Prozess des Zerlegens
- [[Embedding]] → Token wird zu Vektor
- [[Transformer]] → verarbeitet Token-Sequenzen

## Verweise
- [[LLM]]
- [[NLP]]
