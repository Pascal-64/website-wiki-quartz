# Wiki-Lücken

Offene Lücken, die lokal durch den Wiki-Agenten gefüllt werden.
Workflow: `open` → `generated` → `applied` → `done` / `failed`
Nur der Mensch setzt Status auf `done`.

---

## Offene Lücken

### LLM – Fine-Tuning und RLHF vertiefen
status: applied
priority: high
target: content/Themen/LLM.md
mode: append_under_heading
heading: "### RLHF"

Aufgabe:
Ergänze den Abschnitt mit konkreten Beispielen und Erklärungen zu SFT (Supervised Fine-Tuning),
LoRA, QLoRA, DPO (Direct Preference Optimization) und RLHF im Vergleich.
Erkläre den Unterschied zwischen den Methoden und wann welche sinnvoll ist.
QLoRA ermöglicht Fine-Tuning auf Consumer-GPUs durch 4-Bit-Quantisierung (ca. 90% weniger VRAM).
DPO ist eine Alternative zu RLHF: kein separates Reward Model nötig, direkte Optimierung auf Präferenzpaaren.
Füge ein echtes Codebeispiel mit der peft-Bibliothek (LoraConfig) hinzu.

Suchbegriffe:
- QLoRA memory reduction consumer GPU 4-bit quantization
- LoRA PEFT LoraConfig fine-tuning example
- DPO direct preference optimization reward model
- RLHF reinforcement learning human feedback PPO

Bevorzugte Quellen:
- huggingface.co
- pytorch.org
- arxiv.org
- github.com

Akzeptanzkriterien:
- type: table
  required: true
  contains: [SFT, LoRA, QLoRA, RLHF, DPO]

- type: code
  required: true
  language: python
  contains: [peft, LoraConfig]

- type: contains_all
  required: true
  terms: [QLoRA, Speicher, Consumer]

- type: contains_all
  required: true
  terms: [DPO, Reward Model]

- type: sources
  required: true
  min: 2

---

### Neural Networks – Backpropagation im Training erklären
status: open
priority: medium
target: content/Themen/Neural-Networks.md
mode: append_under_heading
heading: "## Training"

Aufgabe:
Ergänze den Training-Abschnitt um eine verständliche Erklärung von Backpropagation.
Erkläre die Kettenregel, den Gradienten-Flow durch Schichten und wie Gewichte aktualisiert werden.
Füge ein einfaches Beispiel mit 2 Schichten hinzu.

Suchbegriffe:
- backpropagation chain rule gradient descent explanation
- neural network weight update gradient flow layers
- backpropagation example step by step

Bevorzugte Quellen:
- deeplearningbook.org
- pytorch.org
- cs231n.github.io

Akzeptanzkriterien:
- type: contains_all
  required: true
  terms: [Kettenregel, Gradient, Gewicht]

- type: contains_all
  required: true
  terms: [Backpropagation, Schicht]

- type: sources
  required: true
  min: 1

---

### Machine Learning – Bias-Variance Tradeoff
status: open
priority: medium
target: content/Themen/Machine-Learning.md
mode: append_under_heading
heading: "## Kernkonzepte"

Aufgabe:
Erkläre den Bias-Variance Tradeoff mit einer kurzen Formel und einem praktischen Beispiel.
Zeige wann Underfitting und Overfitting auftritt und wie man gegensteuert.

Suchbegriffe:
- bias variance tradeoff machine learning underfitting overfitting
- bias variance decomposition MSE formula
- how to reduce overfitting regularization

Bevorzugte Quellen:
- scikit-learn.org
- deeplearningbook.org
- en.wikipedia.org

Akzeptanzkriterien:
- type: contains_all
  required: true
  terms: [Bias, Varianz, Tradeoff]

- type: contains_all
  required: true
  terms: [Underfitting, Overfitting]

- type: sources
  required: true
  min: 1

---

## Erledigt

(hier landen abgeschlossene Einträge)
