<div align="center">

# ⚡ AI-Pulse

### The structured, high-density AI resource repository for 2026

[![GitHub Stars](https://img.shields.io/github/stars/sam-89/ai-pulse?style=flat-square&color=gold)](https://github.com/sam-89/ai-pulse/stargazers)
[![Last Updated](https://img.shields.io/badge/updated-2026-04-14-blue?style=flat-square)](https://github.com/sam-89/ai-pulse/commits/main)
[![Entries](https://img.shields.io/badge/entries-13-green?style=flat-square)](https://github.com/sam-89/ai-pulse/tree/main/registry)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

*Not just a list — a living, structured database of the AI ecosystem.*
*Updated weekly. Every entry is curated, not scraped.*

[🗺️ Learning Paths](#learning-paths) · [🧠 LLMs](#llms) · [🤖 Agent Frameworks](#agent-frameworks) · [🔌 MCP Servers](#mcp-servers) · [📄 Papers](#papers) · [🤝 Contribute](CONTRIBUTING.md)

</div>

---

## What makes this different?

Most "Awesome AI" lists are link dumps. AI-Pulse is a **structured registry**:

- 📋 **JSON schema** — every entry has consistent fields (pricing, maturity, curator note)
- 🤖 **Weekly auto-updates** — GitHub Actions + AI scraper finds new tools every Monday
- 🗺️ **Role-based learning paths** — not just links, but curated journeys
- 💬 **Curator notes** — a human insight on *why* each entry matters
- ✅ **Human reviewed** — all entries pass a quality gate before merging

---

## Learning Paths

| Path | Target Role | Duration |
|------|------------|----------|
| [Zero to AI Agent Engineer](learning-paths/zero-to-agent-engineer.md) | AI/Agentic Platform Engineer | 12–16 weeks |
| [LLM Researcher Track](learning-paths/llm-researcher.md) *(coming soon)* | ML Researcher | 20–24 weeks |
| [AI Product Manager Track](learning-paths/ai-pm.md) *(coming soon)* | AI Product Manager | 6–8 weeks |

---

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add entries, suggest learning paths, or improve the automation scripts.

**Quick add:** Copy `registry/schema.json`, fill in your entry, and open a PR targeting `registry/candidates/`.

---

## Stats

| Category | Entries |
|----------|---------|
| 🧠 Large Language Models | 5 |
| 🤖 Agent Frameworks & Orchestration | 4 |
| 🔌 MCP Servers | 4 |

*Last compiled: 2026-04-14 by build_readme.py*

---

<div align="center">
Made with ❤️ by the AI-Pulse community · <a href="https://github.com/sam-89/ai-pulse">Star us on GitHub</a>
</div>
