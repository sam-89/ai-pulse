# 🗺️ Learning Path: From Zero to AI Agent Engineer

> **Time investment:** 12–16 weeks part-time (10h/week)  
> **Target role:** AI/Agentic Platform Engineer  
> **Last updated:** 2026-04-14

---

## Overview

This path takes you from foundational Python to building production-grade autonomous agent systems. It mirrors the hiring bar at top AI-native companies in 2026.

```
[Foundations] → [LLM Fundamentals] → [Prompt Engineering] → [Agents] → [Swarms] → [Production]
```

---

## Stage 1 — Foundations (weeks 1–2)

**Goal:** Be comfortable with the tools of the trade.

| Topic | Resource | Time |
|---|---|---|
| Python 3.11+ | Official tutorial | 10h |
| Async Python (`asyncio`) | Real Python guide | 4h |
| Git & GitHub flow | GitHub Skills | 3h |
| APIs & HTTP | FastAPI docs | 4h |
| Docker basics | Play with Docker | 3h |

**Milestone:** Build a FastAPI endpoint that calls an LLM API and returns a JSON response.

---

## Stage 2 — LLM Fundamentals (weeks 3–4)

**Goal:** Understand what LLMs actually are and how they work.

| Topic | Resource | Time |
|---|---|---|
| Transformer architecture (intuition) | 3Blue1Brown series | 3h |
| Tokenization & embeddings | Andrej Karpathy's lectures | 5h |
| Context windows & attention | Anthropic interpretability posts | 2h |
| Model families comparison | AI-Pulse LLM Registry (this repo!) | 1h |

**Milestone:** Fine-tune a small open model on a custom dataset using Hugging Face.

---

## Stage 3 — Prompt Engineering (weeks 5–6)

**Goal:** Reliably extract structured output from any LLM.

| Topic | Resource | Time |
|---|---|---|
| Basic prompting techniques | Anthropic's prompt engineering guide | 3h |
| Chain-of-thought & few-shot | Research papers (linked below) | 2h |
| Structured output / JSON mode | OpenAI + Anthropic docs | 2h |
| System prompt design | AI-Pulse System Prompt Library | 2h |
| Evaluation & evals | Brainlid's LLM Evals guide | 3h |

**Milestone:** Build a prompt that reliably extracts structured data from 50 unstructured news articles.

---

## Stage 4 — Building Agents (weeks 7–9)

**Goal:** Build your first autonomous agent that can use tools.

| Topic | Resource | Time |
|---|---|---|
| ReAct pattern | Original paper + examples | 3h |
| Tool use / function calling | Anthropic tool use docs | 4h |
| MCP protocol | MCP official docs + this repo's registry | 3h |
| Memory systems (short/long-term) | LangChain memory docs | 3h |
| LangGraph fundamentals | LangGraph academy | 5h |

**Milestone:** Build an agent that can search the web, read a file, and summarize findings into a report — autonomously.

---

## Stage 5 — Multi-Agent Systems (weeks 10–12)

**Goal:** Orchestrate multiple specialized agents working together.

| Topic | Resource | Time |
|---|---|---|
| Multi-agent patterns | AutoGen documentation | 5h |
| Supervisor + subagent pattern | LangGraph multi-agent examples | 4h |
| Agent communication protocols | Research: AgentVerse, MetaGPT | 3h |
| Conflict resolution & consensus | Papers: CAMEL, Debate | 2h |
| Swarm intelligence basics | OpenAI Swarm (experimental) | 3h |

**Milestone:** Build a research swarm: one planner agent, three researcher agents, one writer agent — produces a full report on any topic.

---

## Stage 6 — Production & Scaling (weeks 13–16)

**Goal:** Ship agents that are observable, safe, and cost-efficient.

| Topic | Resource | Time |
|---|---|---|
| Observability & tracing | LangSmith / Langfuse | 4h |
| Cost management | Token budgeting patterns | 2h |
| Human-in-the-loop | Interrupt patterns in LangGraph | 3h |
| Safety & guardrails | Guardrails AI, Nemo Guardrails | 3h |
| Deployment patterns | Modal, Fly.io, AWS Bedrock | 4h |
| Agentic platform engineering | Anthropic's agent design patterns | 3h |

**Milestone:** Deploy your research swarm to production with full tracing, cost monitoring, and a human-approval step for final output.

---

## Key Papers to Read

- **ReAct** (2022) — Synergizing Reasoning and Acting in Language Models
- **Toolformer** (2023) — Language Models Can Teach Themselves to Use Tools
- **AgentVerse** (2023) — Facilitating Multi-Agent Collaboration
- **CAMEL** (2023) — Communicative Agents for Mind Exploration
- **Scaling Instructable Agents** (DeepMind, 2024)

---

## Community & Jobs

| Resource | Link |
|---|---|
| r/LocalLLaMA | Reddit |
| Hugging Face Discord | Discord |
| LangChain Discord | Discord |
| AI Engineer Summit talks | YouTube |
| Latent Space podcast | Podcast |

---

*Part of the [AI-Pulse](../README.md) repository. Contributions welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md)*
