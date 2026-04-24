---
title: Overfitting
tags: [glossar, ml, training]
---

# Overfitting

## Definition
Overfitting (Überanpassung) tritt auf wenn ein ML-Modell die Trainingsdaten "auswendig lernt" statt allgemeine Muster zu erkennen. Ergebnis: sehr gute Performance auf Trainingsdaten, schlechte auf neuen Daten.

## Kontext
Das Gegenteil ist Underfitting: Modell zu simpel, kann selbst Trainingsdaten nicht gut vorhersagen.

## Gegenmaßnahmen
- **Mehr Trainingsdaten**: Einfachste und wirksamste Lösung
- **Regularisierung**: L1/L2 Penalties auf Gewichte
- **Dropout**: Zufällig Neuronen deaktivieren
- **Cross-Validation**: Robustere Evaluierung
- **Early Stopping**: Training stoppen wenn Validation-Loss steigt
- **Daten-Augmentation**: Künstliche Datenerweiterung

## Erkennen
Train-Loss sinkt, Validation-Loss steigt → Overfitting.

## Verwandte Begriffe
- [[Gradient Descent]] → Optimierung die zum Overfitting führen kann
- [[Regularisierung]] → Gegenmaßnahme

## Verweise
- [[Machine Learning]]
- [[Deep Learning]]
