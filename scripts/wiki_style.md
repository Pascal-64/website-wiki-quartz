# Wiki Style-Referenz

## Regeln

**Heading-Ebene:**
Ziel-Heading `##` (Ebene 2) → neue Abschnitte beginnen mit `###` (Ebene 3)
Ziel-Heading `###` (Ebene 3) → neue Abschnitte beginnen mit `####` (Ebene 4)
Die erwartete Ebene steht explizit im Prompt. Halte dich strikt daran.

**Mathematik:**
Inline: `$w = w - \eta \cdot \nabla L$`
Block: `$$w_{\text{neu}} = w - \eta \cdot \frac{\partial L}{\partial w}$$`
KEIN `\(...\)` oder `\[...\]` — wird in Quartz nicht gerendert.

**Wikilinks:**
Format: `[[Seitenname]]` oder `[[Seitenname|Anzeigetext]]`
Nur auf existierende Seiten verweisen (Liste im Prompt). Leerzeichen und Bindestriche sind gleichwertig.

**Stil:**
Sachlich, technisch, klar. Keine Marketing-Sprache.
Kurze Absätze (2–4 Sätze). Listen und Tabellen nur wenn sie helfen.
Kein "Als KI", kein "Ich werde", keine Einleitungsfloskeln.

---

## Negativbeispiel (wird blockiert)

FALSCH — Floskel am Anfang, falsche Heading-Ebene (## statt ###), LaTeX `\(...\)`:

Gerne erkläre ich das Konzept ausführlich:

## Lernrate

Die Lernrate wird mit \( \eta \) bezeichnet...

---

## Gutes Beispiel

Ziel-Heading war `## Training` → neuer Abschnitt beginnt mit `###`:

### Lernrate und Konvergenz

Die Lernrate $\eta$ steuert die Schrittgröße beim [[Gradient Descent]]. Typische Startwerte liegen zwischen $0{,}001$ und $0{,}01$.

| Lernrate | Effekt |
|---|---|
| Zu groß | Überspringt Minimum, divergiert |
| Zu klein | Langsame Konvergenz |
| Optimal | Schnelle, stabile Konvergenz |

Adaptive Verfahren wie Adam oder RMSProp passen $\eta$ pro Parameter automatisch an und sind in der Praxis meist stabiler als ein fester Wert.
