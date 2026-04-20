<div align="center">

# ⚡ AI-Pulse

### The structured, high-density AI resource repository for 2026

[![GitHub Stars](https://img.shields.io/github/stars/sam-89/ai-pulse?style=flat-square&color=gold)](https://github.com/sam-89/ai-pulse/stargazers)
[![Last Updated](https://img.shields.io/badge/updated-2026-04-19-blue?style=flat-square)](https://github.com/sam-89/ai-pulse/commits/main)
[![Entries](https://img.shields.io/badge/entries-43-green?style=flat-square)](https://github.com/sam-89/ai-pulse/tree/main/registry)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

*Not just a list — a living, structured database of the AI ecosystem.*
*Auto-updated every 2 days by AI agents. Every entry is scored, curated, and validated before it lands here.*

[🗺️ Learning Paths](#learning-paths) · [🧠 LLMs](#llms) · [🤖 Agent Frameworks](#agent-frameworks) · [🔌 MCP Servers](#mcp-servers) · [📄 Papers](#papers) · [🤝 Contribute](CONTRIBUTING.md)

🧠 LLMs: `5` · 🤖 Frameworks: `4` · 🔌 MCP: `4` · 🛠️ Tools: `5`

</div>

---

## What makes this different?

Most "Awesome AI" lists are link dumps. AI-Pulse is a **structured registry**:

- 📋 **JSON schema** — every entry has consistent fields (pricing, maturity, curator note)
- 🤖 **Agent-updated every 2 days** — autonomous pipeline fetches, scores, and promotes new tools automatically
- 🗺️ **Role-based learning paths** — not just links, but curated journeys
- 💬 **Curator notes** — an LLM insight on *why* each entry matters, seeded by community suggestions
- ✅ **Scored, not scraped** — every entry passes a 0–10 LLM quality gate before reaching the registry

---

<!-- NEWS:START -->
## 📰 Today in AI · *2026-04-20*

| # | Story | Source |
|---|-------|--------|
| 1 | [DeepER-Med: Advancing Deep Evidence-Based Research in Medicine Through Agentic AI](https://arxiv.org/abs/2604.15456) | arxiv-cs-ai |
| 2 | [Experience Compression Spectrum: Unifying Memory, Skills, and Rules in LLM Agents](https://arxiv.org/abs/2604.15877) | arxiv-cs-ai |
| 3 | [Bilevel Optimization of Agent Skills via Monte Carlo Tree Search](https://arxiv.org/abs/2604.15709) | arxiv-cs-ai |
| 4 | [Bureaucratic Silences: What the Canadian AI Register Reveals, Omits, and Obscures](https://arxiv.org/abs/2604.15514) | arxiv-cs-ai |
| 5 | [SocialGrid: A Benchmark for Planning and Social Reasoning in Embodied Multi-Agent Systems](https://arxiv.org/abs/2604.16022) | arxiv-cs-ai |

*[Full summaries & why-it-matters →](daily/NEWS.md)* · *[Archive](daily/)*

<!-- NEWS:END -->

---

## Learning Paths

| Path | Target Role | Duration |
|------|------------|----------|
| [Zero to AI Agent Engineer](learning-paths/zero-to-agent-engineer.md) | AI/Agentic Platform Engineer | 12–16 weeks |
| [LLM Researcher Track](learning-paths/llm-researcher.md) *(coming soon)* | ML Researcher | 20–24 weeks |
| [AI Product Manager Track](learning-paths/ai-pm.md) *(coming soon)* | AI Product Manager | 6–8 weeks |

---

## 🆕 Recently Added

- **[AutoGen 0.4](https://microsoft.github.io/autogen/)** `agent-framework` — Microsoft Research's asynchronous, event-driven multi-agent framework. Supports distributed agent ne…
- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** `agent-framework` — Anthropic's open standard for connecting AI models to external data sources and tools. Becoming the …
- **[LangGraph](https://www.langchain.com/langgraph)** `agent-framework` — Graph-based orchestration framework from LangChain. Build stateful, multi-actor agent applications w…
- **[PydanticAI](https://ai.pydantic.dev/)** `agent-framework` — Agent framework built on Pydantic for type-safe, structured LLM interactions. Integrates natively wi…
- **[DeepLearning.AI Short Courses](https://www.deeplearning.ai/short-courses/)** `course` — Free short courses from Andrew Ng's DeepLearning.AI covering LLM APIs, RAG, agents, fine-tuning, and…

---

## 🧠 Large Language Models

*5 entries*

#### [DeepSeek R2](https://deepseek.com) · [GitHub](https://github.com/deepseek-ai)

DeepSeek's open reasoning model. Chain-of-thought specialist with strong math, science, and code benchmarks at significantly lower cost.

🟢 `open-source` · ✅ `stable` · ⭐ 82,000  
`deepseek` `reasoning` `math` `open-source` `cost-efficient`

> 💡 Unprecedented cost/performance ratio for reasoning tasks. Critical for cost-sensitive agentic pipelines.

#### [Llama 4 Scout](https://llama.meta.com/) · [GitHub](https://github.com/meta-llama/llama-models)

Meta's efficient open-weight model with 10M token context. Ideal for local deployment, RAG systems, and cost-sensitive production workloads.

🟢 `open-source` · 🚀 `production` · ⭐ 48,000  
`meta` `open-source` `local` `long-context` `rag`

> 💡 The go-to open model for 2026 — 10M context is a game changer for RAG.

#### [Claude Sonnet 4](https://www.anthropic.com/claude)

Anthropic's balanced model in the Claude 4 family. Excels at agentic tasks, coding, and analysis. Strong instruction-following with extended context window.

💰 `paid` · 🚀 `production`  
`anthropic` `coding` `agentic` `reasoning` `api`

> 💡 Best-in-class for agentic pipelines in 2026; computer-use ready.

#### [Claude Opus 4](https://www.anthropic.com/claude)

Anthropic's most capable model. Top-tier reasoning, research synthesis, and complex multi-step agentic workflows.

💰 `paid` · 🚀 `production`  
`anthropic` `frontier` `reasoning` `research` `api`

> 💡 Use when task complexity justifies cost. Unmatched on long-horizon reasoning.

#### [Gemini 2.5 Pro](https://deepmind.google/technologies/gemini/)

Google DeepMind's top multimodal model. Excels at video understanding, code generation, and scientific reasoning with native tool use.

💰 `paid` · 🚀 `production`  
`google` `multimodal` `video` `coding` `science`

> 💡 Best for video + code tasks. Competes directly with Claude Opus on benchmarks.

---

## 🤖 Agent Frameworks & Orchestration

*4 entries*

#### [AutoGen 0.4](https://microsoft.github.io/autogen/) · [GitHub](https://github.com/microsoft/autogen)

Microsoft Research's asynchronous, event-driven multi-agent framework. Supports distributed agent networks with a pluggable model client interface.

🟢 `open-source` · ✅ `stable` · ⭐ 45,000  
`microsoft` `multi-agent` `async` `event-driven` `python`

> 💡 The async event-driven architecture in 0.4 is a major leap. Best for complex multi-agent systems.

#### [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) · [GitHub](https://github.com/anthropics/anthropic-mcp)

Anthropic's open standard for connecting AI models to external data sources and tools. Becoming the universal interface layer for agentic systems in 2026.

🟢 `open-source` · 🚀 `production` · ⭐ 18,000  
`anthropic` `mcp` `protocol` `tools` `standard` `interoperability`

> 💡 The USB-C of AI tooling. Framework-agnostic and rapidly becoming an industry standard.

#### [LangGraph](https://www.langchain.com/langgraph) · [GitHub](https://github.com/langchain-ai/langgraph)

Graph-based orchestration framework from LangChain. Build stateful, multi-actor agent applications with fine-grained control over cycles, branching, and persistence.

🟢 `open-source` · 🚀 `production` · ⭐ 12,000  
`langgraph` `orchestration` `stateful` `python` `multi-agent`

> 💡 Production-grade stateful agent orchestration. The graph model solves the 'agent loop' problem cleanly.

#### [PydanticAI](https://ai.pydantic.dev/) · [GitHub](https://github.com/pydantic/pydantic-ai)

Agent framework built on Pydantic for type-safe, structured LLM interactions. Integrates natively with FastAPI for production deployment.

🟢 `open-source` · 🔶 `beta` · ⭐ 8,500  
`pydantic` `type-safe` `fastapi` `structured-output` `python`

> 💡 If you're already on FastAPI, this is the natural choice. Type safety catches bugs before production.

---

## 🔍 Vector Databases & Embedding Stores

*5 entries*

#### [Qdrant](https://qdrant.tech) · [GitHub](https://github.com/qdrant/qdrant)

High-performance vector search engine written in Rust. Supports filtering, named vectors, and sparse vectors. Available as cloud or self-hosted with a gRPC/REST API.

🟢 `open-source` · 🚀 `production` · ⭐ 21,000  
`rust` `open-source` `self-hosted` `filtering` `grpc`

> 💡 Best self-hosted option in 2026 — Rust performance with excellent filtering support.

#### [Chroma](https://www.trychroma.com) · [GitHub](https://github.com/chroma-core/chroma)

Open-source AI-native embedding database designed for LLM applications. Runs embedded or as a server; ideal for prototyping RAG systems locally with zero infrastructure.

🟢 `open-source` · 🔶 `beta` · ⭐ 16,000  
`open-source` `embeddings` `rag` `local` `python`

> 💡 Fastest path from zero to working RAG prototype — no infra required.

#### [pgvector](https://github.com/pgvector/pgvector) · [GitHub](https://github.com/pgvector/pgvector)

Open-source PostgreSQL extension that adds vector similarity search. Store embeddings alongside relational data and query with standard SQL and ACID guarantees.

🟢 `open-source` · ✅ `stable` · ⭐ 13,000  
`postgresql` `sql` `open-source` `embeddings` `extension`

> 💡 If your data is already in Postgres, pgvector removes the need for a separate vector store.

#### [Weaviate](https://weaviate.io) · [GitHub](https://github.com/weaviate/weaviate)

Open-source vector database with built-in vectorization modules for text, images, and code. GraphQL API, multi-tenancy, and hybrid BM25+vector search out of the box.

🟢 `open-source` · 🚀 `production` · ⭐ 11,000  
`open-source` `multimodal` `graphql` `hybrid-search` `multi-tenancy`

> 💡 Unique built-in vectorizer modules make it ideal for multimodal RAG pipelines.

#### [Pinecone](https://www.pinecone.io)

Fully managed cloud vector database with single-digit millisecond query latency at billion-vector scale. First-class support for hybrid dense+sparse search.

🟡 `freemium` · 🚀 `production`  
`managed` `cloud` `hybrid-search` `scalable` `production`

> 💡 Go-to managed option when you need billion-scale search without ops overhead.

---

## 🔌 MCP Servers

*4 entries*

#### [MCP Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) · [GitHub](https://github.com/modelcontextprotocol/servers)

Official Anthropic MCP server for local filesystem access. Enables read/write file operations, directory traversal, and file search from within any MCP-compatible agent.

🟢 `open-source` · 🚀 `production` · ⭐ 14,000  
`mcp` `filesystem` `official` `local` `read-write`

> 💡 Start here. The reference implementation — essential for any local agentic workflow.

#### [MCP GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/github) · [GitHub](https://github.com/modelcontextprotocol/servers)

GitHub MCP server exposing repos, issues, PRs, code search, and commit history as agent-accessible tools. Powers code-review and devops automation agents.

🟢 `open-source` · 🚀 `production` · ⭐ 14,000  
`mcp` `github` `devtools` `code-review` `ci-cd`

> 💡 Essential for any dev-focused agent pipeline. PR review automation alone is worth the setup.

#### [MCP PostgreSQL](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) · [GitHub](https://github.com/modelcontextprotocol/servers)

Read-only PostgreSQL MCP server. Gives agents schema inspection and SQL query capabilities against your Postgres databases with safe sandboxing.

🟢 `open-source` · ✅ `stable` · ⭐ 14,000  
`mcp` `postgresql` `database` `sql` `read-only`

> 💡 The read-only constraint is the right call for production. Pair with a write-capable agent layer.

#### [MCP Brave Search](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search) · [GitHub](https://github.com/modelcontextprotocol/servers)

Brave Search API wrapped as an MCP server. Provides web and local search capabilities to agents without Google's privacy concerns. Includes news and image search.

🟡 `freemium` · ✅ `stable` · ⭐ 14,000  
`mcp` `search` `brave` `web` `privacy`

> 💡 The privacy-respecting search default. Use this over SerpAPI for non-commercial agent projects.

---

## 🛠️ Tools & Utilities

*5 entries*

#### [Ollama](https://ollama.com) · [GitHub](https://github.com/ollama/ollama)

Run large language models locally on macOS, Linux, and Windows with a single CLI command. Ships with a REST API compatible with OpenAI's API surface for easy swapping.

🟢 `open-source` · 🚀 `production` · ⭐ 98,000  
`local` `inference` `open-source` `cli` `openai-compatible`

> 💡 The easiest way to run open models locally — one command and it just works.

#### [vLLM](https://docs.vllm.ai) · [GitHub](https://github.com/vllm-project/vllm)

High-throughput and memory-efficient LLM inference server using PagedAttention. Supports continuous batching, tensor parallelism, and an OpenAI-compatible API for production serving.

🟢 `open-source` · 🚀 `production` · ⭐ 42,000  
`inference` `serving` `gpu` `throughput` `openai-compatible`

> 💡 PagedAttention makes it 2-24x faster than naive serving — the default choice for GPU inference.

#### [LangSmith](https://smith.langchain.com)

LangChain's platform for tracing, evaluating, and monitoring LLM applications. Captures full chain traces, enables dataset-driven evaluation, and surfaces latency and cost metrics.

🟡 `freemium` · 🚀 `production`  
`observability` `tracing` `evaluation` `langchain` `monitoring`

> 💡 Essential observability layer for any LangChain or LangGraph production deployment.

#### [Weights & Biases](https://wandb.ai)

MLOps platform for tracking experiments, versioning datasets and models, and visualizing training runs. Integrates with PyTorch, HuggingFace, and most major training frameworks.

🟡 `freemium` · 🚀 `production`  
`mlops` `experiment-tracking` `fine-tuning` `visualization` `collaboration`

> 💡 Industry-standard experiment tracker; indispensable for any serious fine-tuning project.

#### [Cursor](https://www.cursor.com)

AI-first code editor built on VS Code with deeply integrated LLM assistance. Supports multi-file edits, codebase-aware chat, and inline completions from frontier models.

🟡 `freemium` · 🚀 `production`  
`ide` `coding` `ai-assistant` `vscode` `productivity`

> 💡 Highest-leverage AI coding tool available; multi-file edits close the loop on agentic coding.

---

## 📊 Datasets & Benchmarks

*5 entries*

#### [LMSYS Chatbot Arena](https://huggingface.co/datasets/lmsys/chatbot_arena_conversations) · [GitHub](https://github.com/lm-sys/FastChat)

Crowdsourced human preference dataset from the Chatbot Arena platform. Contains millions of pairwise model comparisons used to derive Elo-based LLM rankings.

🆓 `free` · 🚀 `production` · ⭐ 37,000  
`preference` `rlhf` `ranking` `human-feedback` `evaluation`

> 💡 The most trusted human-preference signal for LLM ranking; Elo scores are now industry-standard.

#### [HumanEval](https://huggingface.co/datasets/openai/openai_humaneval) · [GitHub](https://github.com/openai/human-eval)

OpenAI's hand-crafted coding benchmark of 164 Python programming problems. Measures functional code correctness by executing unit tests against model-generated solutions.

🆓 `free` · 🚀 `production` · ⭐ 2,200  
`benchmark` `coding` `python` `evaluation` `openai`

> 💡 Gold standard for code generation benchmarking; pass@k metric is widely reproduced.

#### [The Stack](https://huggingface.co/datasets/bigcode/the-stack) · [GitHub](https://github.com/bigcode-project/the-stack)

BigCode's 6TB+ dataset of permissively licensed source code across 300+ programming languages. Used to train StarCoder and other open code models; opt-out mechanism included.

🆓 `free` · 🚀 `production` · ⭐ 1,400  
`code` `pretraining` `open-source` `bigcode` `multilingual`

> 💡 The largest permissively licensed code corpus; essential for training or evaluating code LLMs.

#### [MMLU](https://huggingface.co/datasets/cais/mmlu) · [GitHub](https://github.com/hendrycks/test)

Massive Multitask Language Understanding benchmark covering 57 subjects from STEM to law. The de facto standard for measuring a model's breadth of world knowledge.

🆓 `free` · 🚀 `production` · ⭐ 1,200  
`benchmark` `evaluation` `knowledge` `multiple-choice` `academic`

> 💡 Cited in virtually every LLM paper — the minimum bar for comparing model intelligence.

#### [OpenHermes 2.5](https://huggingface.co/datasets/teknium/OpenHermes-2.5)

High-quality synthetically generated instruction dataset of 1M samples curated by Teknium. Powers the Hermes family of fine-tunes and widely used for chat and tool-use SFT.

🆓 `free` · ✅ `stable`  
`instruction-tuning` `synthetic` `sft` `chat` `tool-use`

> 💡 The most-forked community SFT dataset; starting point for most open-model fine-tunes.

---

## 📄 Must-Read Papers

*5 entries*

#### [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

Vaswani et al. (2017) paper introducing the Transformer architecture. Replaces recurrence with self-attention, enabling parallelizable training and establishing the foundation for every modern LLM.

🆓 `free` · 🚀 `production`  
`transformer` `attention` `architecture` `foundational` `nlp`

> 💡 The most cited paper in AI history — every LLM traces its lineage directly to this work.

#### [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

Yao et al. (2022) paper introducing the ReAct prompting paradigm. Interleaves chain-of-thought reasoning with action execution, forming the basis for most modern LLM agent architectures.

🆓 `free` · 🚀 `production`  
`agents` `reasoning` `prompting` `tool-use` `foundational`

> 💡 The paper that defined how agents think-then-act; directly implemented in LangChain and LlamaIndex.

#### [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)

Wei et al. (2022) Google Brain paper demonstrating that few-shot prompts with step-by-step reasoning examples unlock emergent multi-step reasoning in large language models.

🆓 `free` · 🚀 `production`  
`prompting` `reasoning` `chain-of-thought` `few-shot` `emergent`

> 💡 Introduced CoT — now the default prompting technique in every advanced LLM application.

#### [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)

Anthropic (2022) paper introducing Constitutional AI, where a model critiques and revises its own outputs according to a set of principles, enabling scalable AI alignment without human labels.

🆓 `free` · 🚀 `production`  
`alignment` `rlhf` `safety` `anthropic` `self-critique`

> 💡 Foundation of Claude's safety approach; CAI is now widely adopted for scalable alignment.

#### [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)

Schick et al. (2023) Meta AI paper where a model learns to call external APIs — calculators, search, calendars — by self-supervised insertion of API calls into training text.

🆓 `free` · 🚀 `production`  
`tool-use` `api` `self-supervised` `meta` `function-calling`

> 💡 Pioneered self-taught tool use — directly inspired function-calling in GPT-4 and Claude.

---

## 🎓 Courses & Learning Resources

*5 entries*

#### [fast.ai Practical Deep Learning](https://course.fast.ai) · [GitHub](https://github.com/fastai/fastbook)

Jeremy Howard's top-down practical deep learning course covering computer vision, NLP, and diffusion models using PyTorch and the fastai library. Free with Jupyter notebooks.

🆓 `free` · ✅ `stable` · ⭐ 22,000  
`deep-learning` `pytorch` `free` `practical` `notebooks`

> 💡 The best top-down ML course — gets practitioners building real models within hours of starting.

#### [Andrej Karpathy's Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) · [GitHub](https://github.com/karpathy/nn-zero-to-hero)

Andrej Karpathy's YouTube series building neural networks from scratch in Python — from micrograd to GPT-2. The deepest free treatment of how transformers actually work.

🆓 `free` · ✅ `stable` · ⭐ 20,000  
`foundational` `transformers` `from-scratch` `python` `youtube`

> 💡 No other resource builds deeper intuition for how LLMs work — mandatory for serious practitioners.

#### [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course) · [GitHub](https://github.com/huggingface/course)

Free official course from Hugging Face covering Transformers, fine-tuning, datasets, and deployment using the full HuggingFace ecosystem. Available in 10+ languages with interactive notebooks.

🆓 `free` · 🚀 `production` · ⭐ 4,200  
`huggingface` `transformers` `fine-tuning` `free` `multilingual`

> 💡 Best starting point for working with HuggingFace Transformers — comprehensive and free.

#### [DeepLearning.AI Short Courses](https://www.deeplearning.ai/short-courses/)

Free short courses from Andrew Ng's DeepLearning.AI covering LLM APIs, RAG, agents, fine-tuning, and prompt engineering. Designed for practitioners and taught with industry partners.

🆓 `free` · 🚀 `production`  
`free` `llm` `rag` `agents` `beginner-friendly`

> 💡 Fastest way to go from LLM novice to practitioner — free, concise, and highly practical.

#### [Stanford CS336: Language Models from Scratch](https://stanford-cs336.github.io/spring2024/)

Stanford graduate course covering the full LLM training pipeline: tokenization, pretraining, RLHF, and inference optimization. Lectures and assignments publicly available.

🆓 `free` · ✅ `stable`  
`stanford` `pretraining` `academic` `graduate` `rlhf`

> 💡 The most rigorous public curriculum for understanding LLM internals end-to-end.

---

## 🚀 Example Projects

*5 entries*

#### [AutoGPT](https://agpt.co) · [GitHub](https://github.com/Significant-Gravitas/AutoGPT)

One of the first autonomous LLM agent frameworks. Chains GPT-4 calls with memory, web search, and file I/O to pursue long-horizon goals with minimal human intervention.

🟢 `open-source` · 🔶 `beta` · ⭐ 170,000  
`autonomous` `gpt-4` `memory` `web-search` `open-source`

> 💡 Sparked the autonomous-agent wave in 2023; still the most starred AI agent repo on GitHub.

#### [Open Interpreter](https://openinterpreter.com) · [GitHub](https://github.com/OpenInterpreter/open-interpreter)

Open-source implementation of ChatGPT's Code Interpreter that runs locally. Lets LLMs execute Python, JavaScript, and shell commands on your machine via a natural language interface.

🟢 `open-source` · 🔶 `beta` · ⭐ 58,000  
`code-execution` `local` `open-source` `python` `agentic`

> 💡 The most accessible local code-execution agent — bridges the gap between LLMs and your filesystem.

#### [GPT Engineer](https://gptengineer.app) · [GitHub](https://github.com/gpt-engineer-org/gpt-engineer)

Agentic coding tool that generates an entire codebase from a single natural language prompt. Clarifies requirements interactively before writing and can modify existing projects.

🟢 `open-source` · 🔶 `beta` · ⭐ 52,000  
`code-generation` `scaffolding` `agentic` `open-source` `productivity`

> 💡 The canonical 'spec-to-codebase' project — great for rapid prototyping full applications.

#### [Aider](https://aider.chat) · [GitHub](https://github.com/Aider-AI/aider)

AI pair programming tool for the terminal. Edits code across multiple files guided by natural language, with git integration that commits changes automatically with descriptive messages.

🟢 `open-source` · ✅ `stable` · ⭐ 23,000  
`coding-assistant` `terminal` `git` `multi-file` `open-source`

> 💡 Best terminal-native coding agent — git-aware edits and solid multi-file reasoning make it production-ready.

#### [SWE-agent](https://swe-agent.com) · [GitHub](https://github.com/princeton-nlp/SWE-agent)

Princeton NLP's agent that autonomously resolves real GitHub issues on the SWE-bench benchmark. Uses a custom Agent-Computer Interface (ACI) optimized for code editing tasks.

🟢 `open-source` · 🧪 `experimental` · ⭐ 14,000  
`software-engineering` `github` `benchmark` `agentic` `research`

> 💡 State-of-the-art on SWE-bench; defines the research frontier for autonomous software engineering.


---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add entries, suggest learning paths, or improve the automation scripts.

**Quick add:** Copy `registry/schema.json`, fill in your entry, and open a PR targeting `registry/candidates/`.

---

## Stats

| Category | Entries |
|----------|---------|
| 🎓 Courses & Learning Resources | 5 |
| 📊 Datasets & Benchmarks | 5 |
| 🧠 Large Language Models | 5 |
| 📄 Must-Read Papers | 5 |
| 🚀 Example Projects | 5 |
| 🛠️ Tools & Utilities | 5 |
| 🔍 Vector Databases & Embedding Stores | 5 |
| 🤖 Agent Frameworks & Orchestration | 4 |
| 🔌 MCP Servers | 4 |

*Last compiled: 2026-04-19 by build_readme.py*

---

<div align="center">
Made with ❤️ by the AI-Pulse community · <a href="https://github.com/sam-89/ai-pulse">Star us on GitHub</a>
</div>
