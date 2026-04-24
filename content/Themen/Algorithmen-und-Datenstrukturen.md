---
tags: [algorithmen, datenstrukturen, cs, python, komplexität]
status: aktiv
typ: thema
quelle_anzahl: 1
zuletzt_aktualisiert: 2026-04-23
---

# Algorithmen und Datenstrukturen

## Kurzbeschreibung
Grundlegende Informatikkonzepte: Algorithmen lösen Probleme systematisch, Datenstrukturen organisieren Daten effizient. Basis für alle Programmierung und KI-Systeme.

## Relevanz
Effiziente Algorithmen und Datenstrukturen sind die Grundlage für schnelle ML-Modelle, skalierbare APIs und performante Systeme.

## Typische Fragestellungen
- Welcher Sortieralgorithmus für welche Situation?
- Was ist Big-O-Notation?
- Wann nutze ich List vs. Dict vs. Set?
- Was ist ein Graph und wie traversiert man ihn?
- Hash-Tabellen – wie funktionieren sie?

## Big-O-Notation (Komplexität)

| Notation | Name | Beispiel |
|---|---|---|
| O(1) | Konstant | Dict-Lookup |
| O(log n) | Logarithmisch | Binary Search |
| O(n) | Linear | Linearer Scan |
| O(n log n) | Linearithmisch | Mergesort |
| O(n²) | Quadratisch | Bubble Sort |
| O(2ⁿ) | Exponentiell | Brute Force |

## Datenstrukturen

### Array / Liste
- Geordnet, indexiert, mutable
- Python: `list`, NumPy-Array
- Access: O(1), Search: O(n), Insert: O(n)

### Hash-Tabelle / Dictionary
- Key-Value-Paare, schneller Zugriff
- Python: `dict`, `set`
- Access: O(1) durchschnittlich

### Stack (LIFO)
- Last-In-First-Out
- Python: `list` mit `.append()` und `.pop()`

### Queue (FIFO)
- First-In-First-Out
- Python: `collections.deque`

### Linked List
- Knoten mit Zeiger auf nächsten Knoten
- Python: keine eingebaut, aber mit Klassen umsetzbar

### Baum (Tree)
- Hierarchisch, Wurzel → Äste → Blätter
- Binary Search Tree: Links kleiner, Rechts größer

### Graph
- Knoten (Nodes) + Kanten (Edges)
- Gerichtet oder ungerichtet
- Python: `networkx`, Adjazenzliste als Dict

## Sortieralgorithmen

| Algorithmus | Avg. | Worst | Stabil | In-Place |
|---|---|---|---|---|
| Bubble Sort | O(n²) | O(n²) | Ja | Ja |
| Selection Sort | O(n²) | O(n²) | Nein | Ja |
| Insertion Sort | O(n²) | O(n²) | Ja | Ja |
| Merge Sort | O(n log n) | O(n log n) | Ja | Nein |
| Quick Sort | O(n log n) | O(n²) | Nein | Ja |
| Heap Sort | O(n log n) | O(n log n) | Nein | Ja |
| Timsort | O(n log n) | O(n log n) | Ja | Nein |

Python nutzt Timsort für `sorted()` und `.sort()`.

```python
# Mergesort (Beispiel)
def mergesort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
```

## Such-Algorithmen

### Binary Search
O(log n). Nur auf sortierten Arrays.
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1
```

### Graph-Traversierung
- **BFS** (Breadth-First): Queue, kürzester Pfad
- **DFS** (Depth-First): Stack/Rekursion, erschöpfende Suche

## Verwandte Themen
- [[Python]]
- [[Machine Learning]]
- [[Datenbanken]]

## Quellenbasis
- `Efficient Sorting Algorithms` (2023-12-18)
- Allgemeines Wissen (CLRS, Stanford Algorithms)

## Siehe auch
- [[Data Analysis]]
- [[DevOps und Git]]
