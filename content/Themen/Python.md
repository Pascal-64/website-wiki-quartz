---
tags: [python, programmierung, ki, data-science]
status: aktiv
typ: thema
quelle_anzahl: 5
zuletzt_aktualisiert: 2026-04-23
---

# Python

## Kurzbeschreibung
Python ist die wichtigste Programmiersprache für KI, Data Science und Automatisierung. Klare Syntax, riesiges Ökosystem, Standardsprache im ML/KI-Bereich.

## Relevanz
Nahezu alle KI-Bibliotheken (PyTorch, TensorFlow, scikit-learn, LangChain) sind Python-first. Wer KI entwickelt, nutzt Python.

## Typische Fragestellungen
- Wie strukturiere ich ein Python-Projekt?
- Welche Bibliotheken für welche Aufgaben?
- Wie erstelle ich eine virtuelle Umgebung?
- Wie baue ich eine einfache API mit FastAPI?
- Wie baue ich eine GUI mit Streamlit?

## Kernkonzepte

### Virtuelle Umgebungen
```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Datenstrukturen
- **List**: `[1, 2, 3]` – geordnet, mutable
- **Tuple**: `(1, 2, 3)` – unveränderlich
- **Dict**: `{"key": "value"}` – Key-Value
- **Set**: `{1, 2, 3}` – eindeutig, ungeordnet

### Comprehensions
```python
squares = [x**2 for x in range(10)]
even = [x for x in range(20) if x % 2 == 0]
mapping = {k: v for k, v in pairs}
```

### Decorators
```python
@staticmethod
@property
@dataclass
```

### Type Hints
```python
def greet(name: str) -> str:
    return f"Hello {name}"
```

## Wichtige Bibliotheken

### KI / ML
| Bibliothek | Zweck |
|---|---|
| numpy | Arrays, Mathe |
| pandas | DataFrames |
| scikit-learn | Klassisches ML |
| PyTorch | Deep Learning |
| TensorFlow/Keras | Deep Learning |
| transformers | HuggingFace, LLMs |
| langchain | LLM-Frameworks |

### Web / API
| Bibliothek | Zweck |
|---|---|
| FastAPI | Schnelle REST-APIs |
| Flask | Einfaches Web-Framework |
| requests | HTTP-Requests |
| httpx | Async HTTP |
| pydantic | Datenvalidierung |

### GUI
| Bibliothek | Zweck |
|---|---|
| Streamlit | Schnelle KI-Dashboards |
| tkinter | Desktop-GUI, Standard |
| PyQt5/PySide6 | Professionelle Desktop-GUI |
| Gradio | ML-Model-Demos |

### Utilities
| Bibliothek | Zweck |
|---|---|
| pathlib | Dateipfade |
| json | JSON-Parsing |
| re | Regular Expressions |
| datetime | Datum/Zeit |
| asyncio | Async-Programmierung |
| subprocess | Shell-Befehle ausführen |

## Praxis: Streamlit-GUI für LLM

Aus einem realen Projekt (lokale Ollama-Pipeline):
```python
import streamlit as st
import requests

st.title("Prompt-Optimierer")
raw = st.text_area("Dein Rohprompt:")

if st.button("Verbessern"):
    r = requests.post("http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": raw, "stream": False})
    st.write(r.json()["response"])
```

Start: `streamlit run app.py` oder `python -m streamlit run app.py`

## Praxis: FastAPI Backend

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AnalyzeRequest(BaseModel):
    image_url: str
    focus: str = "ux"

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    return {"result": "Analyse wird durchgeführt"}
```

Start: `uvicorn main:app --reload`

## Projektstruktur (empfohlen)
```
my_project/
├── .venv/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```

## Verwandte Themen
- [[Machine Learning]]
- [[Data Analysis]]
- [[APIs und Web]]
- [[AI Agents]]

## Quellenbasis
- `GUI für Prompt-Optimierung` (2026-04-02) – Streamlit, Ollama-API
- `AI-basierte UX-Analyse` (2025-09-27) – FastAPI, OCR-Pipeline
- `Kundenliste und Filter GUI` (2023-06-27) – Tkinter-GUI
- `Kundenliste nach Kriterien filtern` (2023-06-28)
- `Deutsche IBAN generieren` (2023-07-19)

## Siehe auch
- [[JavaScript-TypeScript]]
- [[DevOps und Git]]
