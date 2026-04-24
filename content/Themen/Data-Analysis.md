---
tags: [data-analysis, data-science, pandas, python, visualisierung]
status: aktiv
typ: thema
zuletzt_aktualisiert: 2026-04-23
---

# Data Analysis

## Kurzbeschreibung
Data Analysis (Datenanalyse) umfasst alle Prozesse um aus Rohdaten Erkenntnisse zu gewinnen. Teilgebiet: Data Science, das neben Analyse auch Modellierung und Engineering umfasst.

## Relevanz
Grundlage für alle datengetriebenen Entscheidungen. Auch Voraussetzung für [[Machine Learning]]: ohne saubere Daten kein gutes Modell.

## Typische Fragestellungen
- Wie exploriere ich einen neuen Datensatz (EDA)?
- Wie bereinige ich fehlende/fehlerhafte Werte?
- Welche Visualisierung für welche Datenart?
- Wie erkenne ich Korrelationen?
- Wie exportiere ich Ergebnisse?

## Kerntools (Python)

| Bibliothek | Zweck |
|---|---|
| pandas | DataFrames, Datenmanipulation |
| numpy | Numerische Berechnungen, Arrays |
| matplotlib | Grundlegende Plots |
| seaborn | Statistische Visualisierungen |
| plotly | Interaktive Charts |
| scipy | Statistische Tests |
| jupyter | Interaktive Notebooks |

## Typischer EDA-Workflow

### 1. Daten laden
```python
import pandas as pd
df = pd.read_csv("data.csv")
df.head()
df.info()
df.describe()
```

### 2. Fehlende Werte
```python
df.isnull().sum()
df.fillna(0)          # oder
df.dropna()
```

### 3. Duplikate
```python
df.duplicated().sum()
df.drop_duplicates()
```

### 4. Verteilungen visualisieren
```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(df["alter"])
sns.boxplot(x="kategorie", y="wert", data=df)
sns.heatmap(df.corr(), annot=True)
```

### 5. Aggregation
```python
df.groupby("kategorie")["wert"].mean()
df.pivot_table(values="umsatz", index="monat", columns="region")
```

## Datentypen und Transformationen

| Transformation | Methode |
|---|---|
| Normalisierung (0–1) | MinMaxScaler |
| Standardisierung (z-score) | StandardScaler |
| Encoding kategorisch | LabelEncoder, OneHotEncoder |
| Dimensionsreduktion | PCA, t-SNE, UMAP |

## Statistik-Grundlagen

| Konzept | Beschreibung |
|---|---|
| Mean/Median/Mode | Lagemaße |
| Standardabweichung | Streuung |
| Korrelation | Pearson r, Spearman ρ |
| p-Wert | Signifikanztest-Ergebnis |
| Konfidenzintervall | Bereich für wahren Wert |

## Verwandte Themen
- [[Python]]
- [[Machine Learning]]
- [[Datenbanken]]
- [[NLP]]

## Quellenbasis
- `Efficient Sorting Algorithms` (2023-12-18) – CS-Grundlagen
- `Software Marktlücken und Chancen` (2025-01-13) – Python, Datenanalyse
- Allgemeines Wissen

## Siehe auch
- [[KI]]
- [[Deep Learning]]
