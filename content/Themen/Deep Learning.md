---
tags: [deep-learning, ml, neural-networks, ki]
status: aktiv
typ: thema
zuletzt_aktualisiert: 2026-04-23
---

# Deep Learning

## Kurzbeschreibung
Deep Learning ist ein Teilgebiet des [[Machine Learning]], das auf tiefen (mehrschichtigen) [[Neural Networks]] basiert. Es ist die Technologie hinter modernen [[LLM]]s, [[Computer Vision]] und [[NLP]].

## Relevanz
Deep Learning hat die KI-Forschung revolutioniert. Ohne tiefe Netze wären GPT, BERT, Stable Diffusion und Co. nicht möglich.

## Typische Fragestellungen
- Was ist der Unterschied zwischen ML und Deep Learning?
- Was sind Layer, Neuronen, Weights und Biases?
- Was sind Aktivierungsfunktionen und warum sind sie nötig?
- Was ist Backpropagation?
- Welche Netzarchitektur für welche Aufgabe?

## Kernkonzepte

### Schichten (Layers)
- **Input Layer**: Empfängt rohe Eingabe (Pixel, Tokens, Zahlen)
- **Hidden Layers**: Lernen interne Repräsentationen
- **Output Layer**: Finale Ausgabe (Klasse, Zahl, nächstes Token)

Tief = viele Hidden Layers. Mehr Schichten → kann komplexere Muster lernen.

### Aktivierungsfunktionen
Nicht-Linearität die nach jedem Neuron angewendet wird.
- **ReLU** (Rectified Linear Unit): `max(0, x)` – Standard für Hidden Layers
- **Sigmoid**: Ausgabe 0–1 – für binäre Klassifikation
- **Softmax**: Wahrscheinlichkeitsverteilung – für Multi-Klassen
- **GELU**: Variante von ReLU, genutzt in Transformers

### Backpropagation
Algorithmus zum Anpassen der Gewichte. Fehler wird rückwärts durch das Netz propagiert. Basis: [[Gradient Descent]].

### Dropout
Regularisierungstechnik: Zufällige Neuronen werden während Training deaktiviert. Verhindert [[Overfitting]].

### Batch Normalization
Normiert Aktivierungen innerhalb eines Batches. Stabilisiert Training, ermöglicht höhere Learning Rates.

## Netzarchitekturen

| Architektur | Abk. | Anwendung |
|---|---|---|
| Convolutional Neural Network | CNN | Bilder ([[Computer Vision]]) |
| Recurrent Neural Network | RNN | Sequenzen (veraltet) |
| Long Short-Term Memory | LSTM | Sequenzen, Text (veraltet) |
| Transformer | – | Text, Sprache, Bilder ([[LLM]]) |
| Generative Adversarial Network | GAN | Bildgenerierung |
| Diffusion Model | – | Bildgenerierung (Stable Diffusion) |
| Autoencoder | AE | Kompression, Denoising |
| Variational Autoencoder | VAE | Generativ |

## Training-Prozess
1. Forward Pass: Eingabe durch Netz, Ausgabe berechnen
2. Loss berechnen (Fehler zwischen Ausgabe und Ziel)
3. Backward Pass: [[Gradient Descent]] + Backpropagation
4. Gewichte aktualisieren (Optimizer: Adam, SGD, RMSProp)
5. Wiederholen für alle Batches → ein Epoch

## Frameworks

| Framework | Sprache | Besonderheit |
|---|---|---|
| PyTorch | Python | Flexible, Forschungsstandard |
| TensorFlow | Python | Production-ready, von Google |
| Keras | Python | High-Level API über TF |
| JAX | Python | GPU/TPU, funktional |

## Verwandte Themen
- [[Machine Learning]]
- [[Neural Networks]]
- [[LLM]]
- [[NLP]]
- [[Computer Vision]]

## Quellenbasis
- Allgemeines Wissen, Standard-DL-Literatur

## Siehe auch
- [[Reinforcement Learning]]
- [[AI Agents]]
