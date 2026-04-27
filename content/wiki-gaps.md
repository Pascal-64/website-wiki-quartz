# Wiki-Lücken

Offene Lücken, die lokal durch den Wiki-Agenten gefüllt werden.
Workflow: `open` → `generated` → `applied` → `done` / `failed`
Nur der Mensch setzt Status auf `done`.

---

## Offene Lücken

### LLM – Fine-Tuning und RLHF vertiefen
status: open
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

Akzeptanzkriterien:
- Enthält Vergleichstabelle zu SFT, LoRA, QLoRA, RLHF und DPO
- Enthält echtes PEFT/LoRA-Codebeispiel (peft-Bibliothek)
- Erklärt QLoRA mit Speicherreduktion und Consumer-Hardware
- Erklärt DPO als Alternative zu RLHF ohne separates Reward Model
- Verwendet mindestens 2 echte Quellen

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

---

## Erledigt

(hier landen abgeschlossene Einträge)
