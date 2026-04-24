---
tags: [reinforcement-learning, ml, ki, rl]
status: aktiv
typ: thema
zuletzt_aktualisiert: 2026-04-23
---

# Reinforcement Learning

## Kurzbeschreibung
Reinforcement Learning (RL) ist ein ML-Paradigma bei dem ein Agent durch Interaktion mit einer Umgebung lernt. Der Agent erhält Belohnungen für gewünschte Aktionen und Strafen für unerwünschte — ähnlich wie Dressur.

## Relevanz
RL ist die Grundlage für: Spielende KI (AlphaGo, AlphaStar), RLHF (Training von [[LLM]]s), robotische Steuerung, autonomes Fahren.

## Kernkonzepte

| Konzept | Beschreibung |
|---|---|
| Agent | Das lernende System |
| Environment | Die Umgebung in der der Agent agiert |
| State | Aktueller Zustand der Umgebung |
| Action | Mögliche Aktionen des Agents |
| Reward | Belohnungssignal nach einer Aktion |
| Policy | Strategie des Agents (State → Action) |
| Value Function | Erwarteter zukünftiger Reward |
| Q-Value | Wert von (State, Action)-Paaren |

## Algorithmen

| Algorithmus | Typ | Anwendung |
|---|---|---|
| Q-Learning | Model-free | Diskrete Aktionsräume |
| DQN | Deep RL | Atari-Spiele |
| Policy Gradient | Model-free | Kontinuierliche Aktionen |
| PPO | Policy Gradient | Standard-RL-Algorithmus |
| SAC | Actor-Critic | Robotik |
| AlphaGo/MuZero | Model-based | Spiele |

## RLHF (Reinforcement Learning from Human Feedback)
Wie LLMs wie GPT und Claude trainiert werden:
1. Supervised Fine-Tuning auf menschlich geschriebenen Antworten
2. Reward Model trainieren (Menschen bewerten Antworten)
3. PPO-Training des LLMs gegen das Reward Model

## Verwandte Themen
- [[Machine Learning]]
- [[Deep Learning]]
- [[LLM]]
- [[AI Agents]]

## Quellenbasis
- Allgemeines Wissen

## Siehe auch
- [[Neural Networks]]
- [[KI]]
