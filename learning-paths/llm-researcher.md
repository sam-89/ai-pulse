# 🗺️ Learning Path: LLM Researcher

> **Time investment:** 20–24 weeks part-time (10h/week)  
> **Target role:** ML Researcher / Research Scientist (LLMs)  
> **Last updated:** 2026-04-14

---

## Overview

This path takes you from solid ML fundamentals to conducting original research on large language models. It mirrors the reading list and skills expected at top AI labs (Anthropic, Google DeepMind, Meta AI, Mistral) and top PhD programs in 2026.

```
[Foundations] → [Transformers In Depth] → [Training at Scale] → [RLHF & Alignment] → [Evaluation] → [Research Frontiers]
```

---

## Stage 1 — Foundations (weeks 1–3)

**Goal:** Ensure your math and ML foundations are solid before diving into LLM-specific work.

| Topic | Resource | Time |
|---|---|---|
| Linear algebra & probability | [Gilbert Strang — Linear Algebra (MIT OCW)](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) | 10h |
| Calculus & backprop by hand | [Karpathy — micrograd walkthrough](https://github.com/karpathy/micrograd) | 6h |
| Deep learning fundamentals | [Fast.ai Part 1](https://course.fast.ai/) | 15h |
| PyTorch fluency | [PyTorch official tutorials](https://pytorch.org/tutorials/) | 8h |
| The classic CNN → RNN journey | [CS231n Stanford lecture notes](https://cs231n.github.io/) | 5h |

**Milestone:** Implement a character-level language model (bigram → MLP → RNN) from scratch in PyTorch.

---

## Stage 2 — Transformers In Depth (weeks 4–6)

**Goal:** Understand every component of the transformer architecture at the code level.

| Topic | Resource | Time |
|---|---|---|
| Attention mechanism (visual) | [3Blue1Brown — Attention in transformers](https://www.youtube.com/watch?v=eMlx5fFNoYc) | 2h |
| "Attention Is All You Need" | [Vaswani et al. (2017)](https://arxiv.org/abs/1706.03762) | 3h |
| Build GPT from scratch | [Karpathy — nanoGPT walkthrough](https://github.com/karpathy/nanoGPT) | 10h |
| Positional encodings (RoPE, ALiBi) | [Su et al. — RoPE (2021)](https://arxiv.org/abs/2104.09864) | 3h |
| Flash Attention & efficiency | [Dao et al. — FlashAttention (2022)](https://arxiv.org/abs/2205.14135) | 4h |
| Mixture of Experts (MoE) | [Fedus et al. — Switch Transformer (2021)](https://arxiv.org/abs/2101.03961) | 3h |
| Tokenization deep dive | [Karpathy — Let's build the GPT tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) | 3h |

**Milestone:** Train a 10M-parameter GPT on the TinyShakespeare dataset; ablate positional encodings and report perplexity differences.

---

## Stage 3 — Training at Scale (weeks 7–11)

**Goal:** Understand how to pretrain, continue-pretrain, and fine-tune models across dozens to thousands of GPUs.

| Topic | Resource | Time |
|---|---|---|
| Pretraining objectives & scaling laws | [Hoffmann et al. — Chinchilla (2022)](https://arxiv.org/abs/2203.15556) | 4h |
| The neural scaling laws paper | [Kaplan et al. (2020)](https://arxiv.org/abs/2001.08361) | 3h |
| Distributed training (DDP, FSDP) | [PyTorch distributed training guide](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html) | 6h |
| Model parallelism (tensor, pipeline) | [Megatron-LM paper](https://arxiv.org/abs/1909.08053) | 4h |
| Data curation & deduplication | [Lee et al. — Deduplicating Training Data (2021)](https://arxiv.org/abs/2107.06499) | 3h |
| The Pile & RedPajama datasets | [Gao et al. — The Pile (2020)](https://arxiv.org/abs/2101.00027) | 2h |
| Instruction fine-tuning (SFT) | [Wei et al. — FLAN (2021)](https://arxiv.org/abs/2109.01652) | 3h |
| LoRA & parameter-efficient fine-tuning | [Hu et al. — LoRA (2021)](https://arxiv.org/abs/2106.09685) | 3h |
| The LLaMA family | [Touvron et al. — LLaMA 2 (2023)](https://arxiv.org/abs/2307.09288) | 3h |

**Milestone:** Continue-pretrain a 1B open model on a custom domain corpus using Hugging Face Accelerate; measure perplexity delta vs. base model.

---

## Stage 4 — RLHF & Alignment (weeks 12–15)

**Goal:** Understand how models are aligned with human intent — RLHF, DPO, Constitutional AI, and beyond.

| Topic | Resource | Time |
|---|---|---|
| InstructGPT — the RLHF blueprint | [Ouyang et al. (2022)](https://arxiv.org/abs/2203.02155) | 4h |
| Proximal Policy Optimization (PPO) | [Schulman et al. — PPO (2017)](https://arxiv.org/abs/1707.06347) | 4h |
| Reward model training | [Ziegler et al. — Fine-tuning LMs from human preferences (2019)](https://arxiv.org/abs/1909.08593) | 3h |
| Direct Preference Optimization (DPO) | [Rafailov et al. — DPO (2023)](https://arxiv.org/abs/2305.18290) | 3h |
| Constitutional AI | [Bai et al. — Constitutional AI (2022)](https://arxiv.org/abs/2212.08073) | 3h |
| RLAIF & synthetic feedback | [Lee et al. — RLAIF (2023)](https://arxiv.org/abs/2309.00267) | 2h |
| Alignment tax & capability vs. safety tradeoffs | Anthropic research blog posts | 3h |

**Milestone:** Train a small reward model on a preference dataset (e.g. Anthropic HH-RLHF); run DPO fine-tuning and compare outputs qualitatively.

---

## Stage 5 — Evaluation & Benchmarking (weeks 16–18)

**Goal:** Know how to rigorously measure what a model can and cannot do.

| Topic | Resource | Time |
|---|---|---|
| BIG-Bench & MMLU | [Srivastava et al. — BIG-Bench (2022)](https://arxiv.org/abs/2206.04615) | 3h |
| Holistic Evaluation (HELM) | [Liang et al. — HELM (2022)](https://arxiv.org/abs/2211.09110) | 3h |
| LLM-as-judge methodology | [Zheng et al. — MT-Bench & Chatbot Arena (2023)](https://arxiv.org/abs/2306.05685) | 3h |
| Calibration & hallucination measurement | [Kadavath et al. — Language Models (Mostly) Know What They Know (2022)](https://arxiv.org/abs/2207.05221) | 3h |
| Red teaming & adversarial evals | [Perez et al. — Red Teaming LMs (2022)](https://arxiv.org/abs/2202.03286) | 3h |
| lm-evaluation-harness (EleutherAI) | [GitHub repo](https://github.com/EleutherAI/lm-evaluation-harness) | 4h |

**Milestone:** Run lm-evaluation-harness on two models of your choice; write a 2-page comparison report with a critical analysis of benchmark validity.

---

## Stage 6 — Research Frontiers (weeks 19–24)

**Goal:** Engage with the current research frontier and develop your own research taste.

| Topic | Resource | Time |
|---|---|---|
| Chain-of-thought & reasoning | [Wei et al. — CoT (2022)](https://arxiv.org/abs/2201.11903) | 3h |
| Tree of Thought & search | [Yao et al. — Tree of Thoughts (2023)](https://arxiv.org/abs/2305.10601) | 2h |
| Long-context & memory | [Liu et al. — Lost in the Middle (2023)](https://arxiv.org/abs/2307.03172) | 2h |
| Mechanistic interpretability | [Elhage et al. — A Mathematical Framework for Transformer Circuits (2021)](https://transformer-circuits.pub/2021/framework/index.html) | 8h |
| Sparse autoencoders (SAEs) | [Anthropic — Towards Monosemanticity (2023)](https://transformer-circuits.pub/2023/monosemantic-features/index.html) | 5h |
| Multimodal LLMs | [Liu et al. — LLaVA (2023)](https://arxiv.org/abs/2304.08485) | 3h |
| Retrieval-Augmented Generation | [Lewis et al. — RAG (2020)](https://arxiv.org/abs/2005.11401) | 3h |
| Speculative decoding | [Chen et al. — Speculative Decoding (2023)](https://arxiv.org/abs/2302.01318) | 3h |
| How to write a research paper | [Whitesides' Group: Writing a Paper](https://intra.ece.ucr.edu/~rlake/Whitesides_writing_res_paper.pdf) | 2h |
| How to do research (meta) | [Hamming — You and Your Research](https://www.cs.virginia.edu/~robins/YouAndYourResearch.html) | 1h |

**Milestone:** Reproduce the results of one paper (any from the list above) and write a short blog post explaining what you found and any deviations.

---

## Key Papers Reading List

### Must-Read Foundations
- **Attention Is All You Need** (Vaswani et al., 2017) — [arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- **BERT** (Devlin et al., 2018) — [arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805)
- **GPT-3** (Brown et al., 2020) — [arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)
- **Scaling Laws** (Kaplan et al., 2020) — [arxiv.org/abs/2001.08361](https://arxiv.org/abs/2001.08361)
- **Chinchilla** (Hoffmann et al., 2022) — [arxiv.org/abs/2203.15556](https://arxiv.org/abs/2203.15556)

### Alignment
- **InstructGPT** (Ouyang et al., 2022) — [arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155)
- **Constitutional AI** (Bai et al., 2022) — [arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)
- **DPO** (Rafailov et al., 2023) — [arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290)

### Interpretability
- **Transformer Circuits** (Elhage et al., 2021) — [transformer-circuits.pub](https://transformer-circuits.pub/2021/framework/index.html)
- **Towards Monosemanticity** (Anthropic, 2023) — [transformer-circuits.pub](https://transformer-circuits.pub/2023/monosemantic-features/index.html)

---

## Community & Research Venues

| Resource | Link |
|---|---|
| ArXiv cs.CL | [arxiv.org/list/cs.CL/recent](https://arxiv.org/list/cs.CL/recent) |
| Hugging Face Papers | [huggingface.co/papers](https://huggingface.co/papers) |
| ACL Anthology | [aclanthology.org](https://aclanthology.org/) |
| NeurIPS / ICML / ICLR proceedings | Various |
| Alignment Forum | [alignmentforum.org](https://www.alignmentforum.org/) |
| Latent Space podcast | Podcast |
| Dwarkesh Patel podcast | Podcast |

---

*Part of the [AI-Pulse](../README.md) repository. Contributions welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md)*
