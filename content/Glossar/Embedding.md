---
tags: [glossar, llm, nlp, ml]
typ: glossar
---

# Embedding

## Definition
Ein Embedding ist eine dichte Vektordarstellung von Daten (Text, Bilder, etc.) im mehrdimensionalen Raum. Semantisch ähnliche Elemente liegen im Vektorraum näher beieinander.

## Kontext
Embeddings sind das Bindeglied zwischen rohen Daten und neuronalen Netzen. Sie ermöglichen:
- Semantische Suche (ähnlichsten Vektor finden)
- RAG (relevante Texte für LLMs abrufen)
- Clustering (ähnliche Dokumente gruppieren)
- Transfer Learning (vortrainierte Repräsentationen)

Beispiel:
- "König" - "Mann" + "Frau" ≈ "Königin" (Word2Vec)

## Typen
- **Word Embeddings**: Word2Vec, GloVe – je Wort ein Vektor
- **Sentence Embeddings**: Satz-Transformers – ganzer Satz als Vektor
- **Contextual Embeddings**: BERT, GPT – Kontext-abhängig

## Verwandte Begriffe
- [[Token]] → wird zu Embedding
- [[Transformer]] → erzeugt Embeddings
- [[LLM]] → nutzt Embeddings intern

## Verweise
- [[NLP]]
- [[Datenbanken]] (Vector DB)
- [[AI Agents]] (RAG)
