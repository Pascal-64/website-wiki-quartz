---
tags: [devops, git, docker, ci-cd, linux]
status: aktiv
typ: thema
zuletzt_aktualisiert: 2026-04-23
---

# DevOps und Git

## Kurzbeschreibung
DevOps verbindet Softwareentwicklung und IT-Betrieb. Git ist das Standard-Versionskontrollsystem. Docker containerisiert Anwendungen. CI/CD automatisiert Tests und Deployments.

## Relevanz
KI-Projekte müssen versioniert, deployt und skaliert werden. Docker ist Standard für ML-Model-Serving. Git ist unverzichtbar für jeden Entwickler.

## Typische Fragestellungen
- Git-Grundbefehle?
- Was ist ein Branch und wann nutze ich ihn?
- Wie containerisiere ich eine Python-App mit Docker?
- Was ist CI/CD?
- Wie deploye ich ein FastAPI-Backend?

## Git Grundlagen

```bash
git init                   # Repository initialisieren
git clone <url>            # Repository klonen
git status                 # Änderungen anzeigen
git add .                  # Alle Änderungen stagen
git commit -m "message"    # Commit erstellen
git push origin main       # Auf Remote pushen
git pull                   # Änderungen holen
git branch feature-x       # Branch erstellen
git checkout feature-x     # Branch wechseln
git merge feature-x        # Branch mergen
git log --oneline          # Commit-History
git diff                   # Änderungen anzeigen
```

### Branching-Strategien
- **main/master**: Produktions-Branch, immer stabil
- **develop**: Integrations-Branch
- **feature/xxx**: Für neue Features
- **hotfix/xxx**: Kritische Fixes direkt auf main

### Git Flow (vereinfacht)
```
feature → develop → main
hotfix → main → develop
```

## Docker

### Grundkonzepte
- **Image**: Unveränderliche Vorlage (wie ISO)
- **Container**: Laufende Instanz eines Images
- **Dockerfile**: Bauanleitung für ein Image
- **Docker Hub**: öffentliche Image-Registry

### Dockerfile für Python/FastAPI
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t my-api .
docker run -p 8000:8000 my-api
docker-compose up
```

### docker-compose.yml
```yaml
version: "3.9"
services:
  api:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
```

## CI/CD

### GitHub Actions (Beispiel)
```yaml
name: Test & Deploy
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest
```

## Linux-Grundbefehle
```bash
ls -la          # Dateien auflisten
pwd             # Aktueller Pfad
cd /path        # Verzeichnis wechseln
cat file.txt    # Datei ausgeben
grep "term" .   # Suchen
chmod +x script.sh  # Ausführbar machen
ps aux          # Prozesse
top             # System-Monitor
```

## Verwandte Themen
- [[Python]]
- [[APIs und Web]]
- [[JavaScript-TypeScript]]

## Quellenbasis
- `Volumen verkleinern für Linux` (2025-09-05) – Linux + Docker
- Allgemeines Wissen

## Siehe auch
- [[Datenbanken]]
- [[Algorithmen und Datenstrukturen]]
