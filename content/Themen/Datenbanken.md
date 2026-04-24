---
tags: [datenbanken, sql, nosql, datenbank]
status: aktiv
typ: thema
zuletzt_aktualisiert: 2026-04-23
---

# Datenbanken

## Kurzbeschreibung
Datenbanken speichern und verwalten strukturierte oder unstrukturierte Daten persistent. Im KI-Kontext: Trainingsdaten, Embedding-Stores, Session-Speicher, Logging.

## Relevanz
Jede KI-Anwendung die Daten persistiert braucht eine Datenbank. RAG-Systeme nutzen Vector Databases. ML-Pipelines speichern Features und Ergebnisse.

## Typische Fragestellungen
- SQL vs. NoSQL – wann was?
- Was ist eine Vector Database?
- Wie designe ich ein Datenbankschema?
- Was sind Indizes und warum sind sie wichtig?
- Wie verbinde ich Python mit einer Datenbank?

## Datenbanktypen

| Typ | Beispiele | Anwendung |
|---|---|---|
| Relational (SQL) | PostgreSQL, MySQL, SQLite | Strukturierte Daten, Transaktionen |
| Document | MongoDB | Flexibles Schema, JSON-Dokumente |
| Key-Value | Redis | Cache, Session, schnelle Lookups |
| Column-Family | Cassandra | Zeitreihen, Big Data |
| Graph | Neo4j | Verknüpfte Daten, Knowledge Graphs |
| Vector | Pinecone, Weaviate, pgvector | Embedding-Suche, RAG |

## SQL-Grundlagen

```sql
-- Tabelle erstellen
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Daten einfügen
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- Daten abfragen
SELECT id, name FROM users WHERE email LIKE '%@example.com' ORDER BY name;

-- JOIN
SELECT u.name, o.amount 
FROM users u 
JOIN orders o ON u.id = o.user_id
WHERE o.amount > 100;
```

## Vector Databases (für KI/RAG)

Vector Databases speichern [[Embedding]]s und ermöglichen semantische Ähnlichkeitssuche.

```python
# Beispiel mit pgvector + Python
import psycopg2
conn = psycopg2.connect(...)
# Embeddings speichern
cur.execute("INSERT INTO docs (content, embedding) VALUES (%s, %s)", 
            (text, embedding_vector))
# Ähnlichkeitssuche
cur.execute("SELECT content FROM docs ORDER BY embedding <-> %s LIMIT 5", 
            (query_embedding,))
```

Populäre Vector-DBs:
- **Pinecone**: Cloud, managed
- **Weaviate**: Open Source, GraphQL-API
- **Chroma**: Lokal, für Entwicklung
- **pgvector**: PostgreSQL-Extension

## Python-Datenbankzugriff

| Bibliothek | DB | Typ |
|---|---|---|
| psycopg2 | PostgreSQL | Low-Level |
| sqlite3 | SQLite | Standard, eingebaut |
| SQLAlchemy | Alle | ORM + Raw SQL |
| pymongo | MongoDB | Document |
| redis-py | Redis | Key-Value |

```python
import sqlite3
conn = sqlite3.connect("data.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO items (name) VALUES (?)", ("test",))
conn.commit()
```

## ORM (Object-Relational Mapping)

```python
# SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
```

## Verwandte Themen
- [[Python]]
- [[APIs und Web]]
- [[Data Analysis]]
- [[LLM]] (für RAG / Vector Stores)

## Quellenbasis
- `Schnellste DB-Übersetzung Methoden` (2026-04-15)
- Allgemeines Wissen

## Siehe auch
- [[DevOps und Git]]
- [[Algorithmen und Datenstrukturen]]
