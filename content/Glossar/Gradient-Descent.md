---
title: Gradient Descent
tags: [glossar, ml, deep-learning, optimierung]
---

# Gradient Descent

## Definition
Gradient Descent ist der Standard-Optimierungsalgorithmus im [[Machine Learning]]. Er minimiert die Loss-Funktion durch iterative Anpassung der Modellparameter in Richtung des negativen Gradienten.

## Funktionsweise
1. Loss berechnen (Fehler zwischen Vorhersage und Ziel)
2. Gradienten berechnen (partielle Ableitungen, Backpropagation)
3. Parameter updaten: `w = w - learning_rate * gradient`
4. Wiederholen bis Konvergenz

## Varianten

| Variante | Batch-Größe | Eigenschaft |
|---|---|---|
| Batch GD | Alle Daten | Stabil, langsam |
| Stochastic GD (SGD) | 1 Sample | Schnell, rauschig |
| Mini-Batch GD | 32–256 | Kompromiss (Standard) |

## Optimizers (Erweiterungen)
- **Adam**: Adaptiv, mit Momentum → Standard für Deep Learning
- **RMSProp**: Adaptiv, gut für RNNs
- **AdaGrad**: Selten genutzte Elemente lernen mehr
- **SGD mit Momentum**: Klassisch, oft für Finetuning

## Lernrate (Learning Rate)
Kritischer Hyperparameter:
- Zu groß: Divergenz (Fehler steigt)
- Zu klein: Langsame Konvergenz
- Learning Rate Scheduler: Lernrate über Zeit anpassen

## Verwandte Begriffe
- [[Overfitting]] → zu viele Update-Schritte können dazu führen
- [[Backpropagation]] → berechnet Gradienten

## Verweise
- [[Machine Learning]]
- [[Deep Learning]]
- [[Neural Networks]]
