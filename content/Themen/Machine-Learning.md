---
tags: [ml, machine-learning, ki, training]
status: aktiv
typ: thema
zuletzt_aktualisiert: 2026-04-23
---

# Machine Learning

## Kurzbeschreibung
Machine Learning (ML) ist ein Teilgebiet der [[KI]]. Systeme lernen aus Daten Muster und Regeln — ohne explizit programmiert zu werden. ML ist die Grundlage für [[Deep Learning]], [[NLP]], [[Computer Vision]] und viele weitere Bereiche.

## Relevanz
ML ist der methodische Kern moderner KI. Wer KI-Systeme entwickeln oder verstehen will, muss ML-Grundlagen kennen.

## Typische Fragestellungen
- Was ist der Unterschied zwischen Supervised und Unsupervised Learning?
- Wie trainiert man ein Modell?
- Was ist Overfitting und wie verhindert man es?
- Welche Metriken zur Modellbewertung?
- Wann nutze ich welchen Algorithmus?

## Lernparadigmen

### Supervised Learning (Überwachtes Lernen)
Modell lernt aus Eingabe-Ausgabe-Paaren (Labels).
- Beispiele: Bildklassifikation, Spam-Erkennung, Preisvorhersage
- Algorithmen: Linear Regression, Decision Trees, Random Forest, SVM, Neural Networks

### Unsupervised Learning (Unüberwachtes Lernen)
Modell findet selbst Strukturen in ungelabelten Daten.
- Beispiele: Clustering, Dimensionsreduktion, Anomalieerkennung
- Algorithmen: K-Means, DBSCAN, PCA, Autoencoder

### Reinforcement Learning
Agent lernt durch Interaktion mit einer Umgebung und Belohnungssignalen. → [[Reinforcement Learning]]

### Semi-Supervised Learning
Kombination aus wenigen gelabelten und vielen ungelabelten Daten.

### Self-Supervised Learning
Modell erzeugt eigene Labels aus den Daten (z. B. Masking bei BERT).

## Kernkonzepte

### Training, Validation, Test Split
- **Training**: Modell lernt auf diesen Daten
- **Validation**: Hyperparameter-Tuning, Überprüfung während Training
- **Test**: Finale Bewertung auf ungesehenen Daten

### [[Overfitting]] und Underfitting
- **Overfitting**: Modell lernt Trainingsdaten auswendig, generalisiert schlecht
- **Underfitting**: Modell zu simpel, kann Muster nicht lernen
- Gegenmaßnahmen: Regularisierung (L1/L2), Dropout, mehr Daten, Cross-Validation

### [[Gradient Descent]]
Optimierungsalgorithmus. Modell-Parameter werden iterativ in Richtung des geringsten Fehlers angepasst.

### Hyperparameter
Parameter die vor dem Training gesetzt werden: Learning Rate, Batch Size, Anzahl Schichten, etc.

### Cross-Validation
k-Fold: Daten in k Teile aufteilen, k-mal trainieren und validieren. Robustere Bewertung.

## Wichtige Metriken

| Aufgabe | Metriken |
|---|---|
| Klassifikation | Accuracy, Precision, Recall, F1-Score, ROC-AUC |
| Regression | MAE, MSE, RMSE, R² |
| Clustering | Silhouette Score, Davies-Bouldin |

## ML-Bibliotheken (Python)

| Bibliothek | Zweck |
|---|---|
| scikit-learn | Klassische ML-Algorithmen, Preprocessing |
| XGBoost/LightGBM | Gradient Boosting |
| PyTorch | Deep Learning |
| TensorFlow/Keras | Deep Learning |
| Pandas/NumPy | Datenverarbeitung |

## Typischer ML-Workflow
1. Daten sammeln und bereinigen ([[Data Analysis]])
2. Feature Engineering
3. Modell auswählen
4. Training
5. Evaluierung (Metriken, Confusion Matrix)
6. Hyperparameter-Tuning
7. Finale Evaluation auf Testdaten
8. Deployment

## Verwandte Themen
- [[Deep Learning]]
- [[Neural Networks]]
- [[Data Analysis]]
- [[Python]]
- [[KI]]

## Quellenbasis
- Allgemeines Wissen, Standardliteratur ML
- `Software Marktlücken und Chancen` (2025-01-13)

## Siehe auch
- [[Reinforcement Learning]]
- [[NLP]]
- [[Computer Vision]]
