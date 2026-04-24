---
tags: [neural-networks, deep-learning, ml, ki]
status: aktiv
typ: thema
zuletzt_aktualisiert: 2026-04-23
---

# Neural Networks

## Kurzbeschreibung
Neuronale Netze sind das Grundbaustein-Konzept des [[Deep Learning]]. Sie bestehen aus verbundenen Neuronen die in Schichten angeordnet sind und mathematisch Funktionen approximieren.

## Relevanz
Neuronale Netze sind das Fundament aller modernen KI-Systeme: [[LLM]]s, [[Computer Vision]], [[NLP]], Sprachsynthese, Übersetzung.

## Aufbau eines Neurons

```
Eingaben (x1, x2, ...) 
  → Gewichtete Summe (w1*x1 + w2*x2 + bias) 
  → Aktivierungsfunktion 
  → Ausgabe
```

### Komponenten
- **Weights (Gewichte)**: Wie stark ist die Verbindung zwischen zwei Neuronen?
- **Bias**: Verschiebt die Aktivierungsfunktion. Wie der y-Achsenabschnitt.
- **Aktivierungsfunktion**: Fügt Nicht-Linearität hinzu (ReLU, Sigmoid, etc.)

## Arten von Netzen

### Feedforward Neural Network (FNN)
Einfachste Form. Daten fließen nur vorwärts: Input → Hidden → Output. Keine Schleifen.

### Convolutional Neural Network (CNN)
Speziell für räumliche Daten (Bilder). Nutzt Faltungsoperationen statt vollständig verbundener Schichten. → [[Computer Vision]]

### Recurrent Neural Network (RNN)
Für sequentielle Daten. Hat interne Zustände (Memory). Probleme: Vanishing Gradients. Weitgehend von Transformers abgelöst.

### Transformer
Moderne Architektur für Sequenzdaten. Nutzt Self-Attention statt Rekurrenz. Basis für alle modernen [[LLM]]s.

## Training

Ziel: Gewichte so anpassen, dass der Loss (Fehler) minimiert wird.

1. Initialisierung: Gewichte zufällig
2. Forward Pass: Vorhersage berechnen
3. Loss berechnen (z. B. Cross-Entropy, MSE)
4. Backpropagation: Gradienten berechnen
5. [[Gradient Descent]]: Gewichte aktualisieren

## Vanishing Gradient Problem
Bei tiefen Netzen werden Gradienten im Rückwärts-Pass sehr klein → frühe Schichten lernen kaum noch. Lösung: ReLU, ResNet (Skip-Connections), Batch Normalization.

## Verwandte Themen
- [[Deep Learning]]
- [[Machine Learning]]
- [[LLM]]
- [[Transformer]] (Glossar)

## Quellenbasis
- Allgemeines Wissen, Standardliteratur

## Siehe auch
- [[NLP]]
- [[Computer Vision]]
