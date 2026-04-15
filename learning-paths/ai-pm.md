# 🗺️ Learning Path: AI Product Manager

> **Time investment:** 6–8 weeks part-time (8h/week)  
> **Target role:** AI Product Manager / Head of AI Product  
> **Last updated:** 2026-04-14

---

## Overview

This path turns a product manager with general software experience into one who can confidently lead AI-powered product initiatives — from defining the right problems for AI to solve, through responsible launch, to measuring outcomes in production.

```
[AI Literacy] → [Product Frameworks] → [Safety & Ethics] → [Launch & Growth]
```

---

## Stage 1 — AI Literacy (weeks 1–2)

**Goal:** Build enough technical understanding to have credible conversations with ML engineers and make informed trade-offs.

| Topic | Resource | Time |
|---|---|---|
| How LLMs work (intuition, no math) | [3Blue1Brown — But what is a GPT?](https://www.youtube.com/watch?v=wjZofJX0v4M) | 1h |
| Transformer architecture (visual) | [3Blue1Brown — Attention in transformers](https://www.youtube.com/watch?v=eMlx5fFNoYc) | 1h |
| What models can and cannot do | [Anthropic model overview](https://docs.anthropic.com/en/docs/about-claude/models/overview) | 1h |
| Prompt engineering fundamentals | [Anthropic prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) | 3h |
| AI product landscape overview | AI-Pulse registry (this repo!) | 2h |
| Tokens, context windows, cost basics | OpenAI / Anthropic pricing docs | 1h |
| Embeddings & RAG (conceptual) | [What are embeddings? — OpenAI cookbook](https://cookbook.openai.com/articles/what_are_embeddings) | 2h |

**Milestone:** Write a 1-page "AI capabilities brief" that explains to a non-technical stakeholder what a specific LLM can and cannot reliably do.

---

## Stage 2 — Product Frameworks for AI (weeks 3–4)

**Goal:** Adapt your PM toolkit to the unique challenges of building AI-powered products.

| Topic | Resource | Time |
|---|---|---|
| Jobs-to-be-done applied to AI features | [JTBD by Clayton Christensen (summary)](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done) | 1h |
| AI product spec template | [Lenny's Newsletter — AI product specs](https://www.lennysnewsletter.com/) | 2h |
| Defining success metrics for AI | [Eugene Yan — Evaluating LLM products](https://eugeneyan.com/writing/llm-patterns/) | 2h |
| Build vs. buy vs. fine-tune decisions | Anthropic / AWS Bedrock documentation | 2h |
| Latency, cost, and quality trade-offs | OpenAI / Anthropic platform guides | 2h |
| Evals as a PM discipline | [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) | 3h |
| Roadmapping with AI uncertainty | Reforge AI product resources | 2h |

**Milestone:** Write a full PRD for an AI feature in a product you know, including success metrics, eval criteria, and a build/buy/fine-tune recommendation.

---

## Stage 3 — Safety, Ethics & Responsible AI (weeks 5–6)

**Goal:** Understand the risks, regulatory landscape, and responsible deployment practices so you never ship something that blows up.

| Topic | Resource | Time |
|---|---|---|
| AI hallucination & reliability risks | [Anthropic — Model limitations](https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests) | 2h |
| Bias in AI systems | [Barocas et al. — Fairness and Machine Learning](https://fairmlbook.org/) (intro chapter) | 2h |
| EU AI Act overview | [EU AI Act summary (official)](https://artificialintelligenceact.eu/the-act/) | 2h |
| AI safety principles | [Anthropic's core views on AI safety](https://www.anthropic.com/news/core-views-on-ai-safety) | 1h |
| Privacy & data governance for AI | [GDPR and AI guidance (ICO)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/) | 2h |
| Red teaming your AI product | [NIST AI Risk Management Framework](https://airc.nist.gov/Home) | 2h |
| Content policy design | Anthropic & OpenAI usage policy documentation | 2h |
| Human-in-the-loop design patterns | Research & product case studies | 2h |

**Milestone:** Complete a risk assessment and responsible AI checklist for the PRD you wrote in Stage 2.

---

## Stage 4 — Launch & Growth (weeks 7–8)

**Goal:** Know how to take an AI feature from beta to production, monitor it, and iterate.

| Topic | Resource | Time |
|---|---|---|
| A/B testing AI features (pitfalls) | [Ronny Kohavi — Trustworthy Online Experiments](https://experimentguide.com/) (Ch. 1–3) | 3h |
| Monitoring LLM outputs in production | [LangSmith](https://www.langchain.com/langsmith) / [Langfuse](https://langfuse.com/) docs | 3h |
| Feedback loops & annotation pipelines | [Scale AI — Data Engine overview](https://scale.com/data-engine) | 1h |
| User trust & AI disclosure norms | [Nielsen Norman Group — AI UX guidelines](https://www.nngroup.com/topic/artificial-intelligence/) | 2h |
| Pricing AI features | Reforge / Lenny's Newsletter case studies | 2h |
| Communicating AI limitations to users | Product case studies (Notion AI, GitHub Copilot) | 2h |
| Iterating with evals, not just A/B tests | [Chip Huyen — Real-world LLM challenges](https://huyenchip.com/2023/04/11/llm-engineering.html) | 2h |

**Milestone:** Design a launch plan for your AI feature including phased rollout, monitoring dashboard, feedback collection, and rollback criteria.

---

## Key Reading List

### Books
- **"AI Snake Oil"** — Arvind Narayanan & Sayash Kapoor (2024)
- **"The Alignment Problem"** — Brian Christian (2020)
- **"Competing in the Age of AI"** — Iansiti & Lakhani (2020)

### Essential Articles
- [Chip Huyen — LLM Engineering](https://huyenchip.com/2023/04/11/llm-engineering.html)
- [Eugene Yan — Patterns for Building LLM-based Systems](https://eugeneyan.com/writing/llm-patterns/)
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)
- [Ethan Mollick — One Useful Thing (Substack)](https://www.oneusefulthing.org/)

---

## Community & Newsletters

| Resource | Link |
|---|---|
| Lenny's Newsletter (AI PM content) | [lennysnewsletter.com](https://www.lennysnewsletter.com/) |
| One Useful Thing (Ethan Mollick) | [oneusefulthing.org](https://www.oneusefulthing.org/) |
| The Pragmatic Engineer | [newsletter.pragmaticengineer.com](https://newsletter.pragmaticengineer.com/) |
| AI Product Institute | [aiproductinstitute.com](https://aiproductinstitute.com/) |
| Latent Space podcast | Podcast |
| Product Hunt AI launches | [producthunt.com](https://www.producthunt.com/) |

---

*Part of the [AI-Pulse](../README.md) repository. Contributions welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md)*
