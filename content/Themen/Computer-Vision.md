---
tags: [computer-vision, ki, deep-learning, bilder, ocr]
status: aktiv
typ: thema
zuletzt_aktualisiert: 2026-04-23
---

# Computer Vision

## Kurzbeschreibung
Computer Vision ist das KI-Teilgebiet das Maschinen das "Sehen" ermöglicht. Bilder und Videos werden analysiert, klassifiziert und interpretiert. Grundlage: [[Deep Learning]], insbesondere CNNs und [[Transformer]]-Architekturen.

## Relevanz
OCR, Objekterkennung, medizinische Bildanalyse, autonomes Fahren, Qualitätssicherung, UI-Analyse — Computer Vision ist in vielen Branchen präsent.

## Typische Fragestellungen
- Wie erkenne ich Objekte auf einem Bild?
- Was ist OCR und welche Tools gibt es?
- Wie analysiere ich Screenshots mit KI?
- Wie trainiere ich einen Bildklassifikator?
- Multimodal: Wie gibt man einem LLM Bilder?

## Kernaufgaben

| Aufgabe | Beschreibung |
|---|---|
| Image Classification | Bild einer Klasse zuordnen (Katze/Hund) |
| Object Detection | Objekte lokalisieren + klassifizieren (Bounding Boxes) |
| Semantic Segmentation | Jeden Pixel klassifizieren |
| Instance Segmentation | Objekte + Pixel-genau (Mask RCNN) |
| OCR | Text aus Bildern extrahieren |
| Pose Estimation | Körperpositionen erkennen |
| Image Generation | Bilder aus Text generieren (DALL-E, SD) |

## Kernkonzepte

### CNN (Convolutional Neural Network)
Speziell für Bilder. Faltungsoperationen erkennen lokale Muster (Kanten, Texturen). Tiefere Schichten erkennen komplexere Muster.

### Transfer Learning
Vortrainiertes Netz (ImageNet) auf eigene Daten anpassen. Spart enorm viel Trainingszeit.

### Bounding Boxes
Rechteck das ein Objekt umschließt: `[x, y, width, height]`.

### Data Augmentation
Trainingsdaten künstlich erweitern: Spiegeln, Drehen, Zoomen, Rauschen → bessere Generalisierung.

## OCR (Optical Character Recognition)

Extraktion von Text aus Bildern:
- **Tesseract**: Open-Source, gut für klare Dokumente
- **PaddleOCR**: Besser für UI-Elemente und komplexe Layouts
- **Google Vision API**: Cloud, sehr präzise
- **Azure Computer Vision**: Cloud, Dokumentenanalyse

```python
import pytesseract
from PIL import Image

img = Image.open("screenshot.png")
text = pytesseract.image_to_string(img, lang="deu")
```

## Multimodal LLMs für Vision

Moderne LLMs können direkt Bilder verarbeiten:
- **GPT-4o**: Bild + Text gleichzeitig
- **Claude 3.5/4**: Vision-Fähigkeiten
- **Gemini**: Multimodal

Anwendungsfall: Screenshot eines UI hochladen → LLM analysiert Layout, gibt UX-Feedback, schlägt Verbesserungen vor. (Praxisbeispiel aus `AI-basierte UX-Analyse`)

## Wichtige Bibliotheken

| Bibliothek | Zweck |
|---|---|
| OpenCV (cv2) | Bildverarbeitung, Video |
| Pillow (PIL) | Bild laden/manipulieren |
| torchvision | Computer Vision für PyTorch |
| ultralytics | YOLO Objekt-Detektion |
| pytesseract | OCR |

## Verwandte Themen
- [[Deep Learning]]
- [[NLP]]
- [[Machine Learning]]
- [[Python]]

## Quellenbasis
- `AI-basierte UX-Analyse` (2025-09-27) – Vision-LLM für UI-Analyse, OCR-Pipeline
- `Software Marktlücken und Chancen` (2025-01-13)
- Allgemeines Wissen

## Siehe auch
- [[Neural Networks]]
- [[LLM]]
