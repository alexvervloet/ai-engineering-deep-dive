# Models & Pricing: a reference for the series

A quick, practical reference: the models these deep dives use, what they cost, and
how to choose one. Part of the [AI Engineering Deep Dives](README.md).

> ⚠️ **Prices and models change. This is a snapshot, last updated 2026-06-26.**
> Always confirm against the provider's own page before relying on a number:
> [OpenAI pricing](https://platform.openai.com/docs/pricing) ·
> [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing).
> For Claude you can also query live capability/price data with the **Models API**
> (`client.models.retrieve("claude-opus-4-8")` → `max_input_tokens`, `max_tokens`,
> `capabilities`). The numbers below mirror the pricing modules the repos ship
> (`utils/pricing.py`, `prod/cost.py`), so the cost examples match this table.

---

## The one mental model

You pay **per token**, and **input** (tokens you send) and **output** (tokens the
model generates) are priced **separately**; output is several times more expensive.
A "token" is roughly ¾ of a word (~4 characters) of English. Prices below are in
**US dollars per 1,000,000 tokens**.

```
cost ≈ (input_tokens × input_price + output_tokens × output_price) / 1,000,000
```

Two levers shrink the bill without changing the model: **prompt caching** (a long,
repeated prefix bills at ~0.1× on cache reads) and the **Batch API** (non-urgent
work at 50% off). Both are covered in the API dives.

---

## Chat models

### OpenAI

| Model | Input $/1M | Output $/1M | Context | Notes |
|-------|-----------:|------------:|--------:|-------|
| `gpt-4o-mini` | 0.15 | 0.60 | ~128K | **The series default.** Cheap, fast, multimodal, great for learning and most tasks. |
| `gpt-4o` | 2.50 | 10.00 | ~128K | Stronger general model; reach for it on harder reasoning/vision. |
| `gpt-4-turbo` | 10.00 | 30.00 | ~128K | Older flagship; usually superseded by 4o. |
| `gpt-3.5-turbo` | 0.50 | 1.50 | ~16K | Legacy; cheap but weaker. |
| o-series (`o4-mini`, …) | varies | varies | large | **Reasoning models**: think before answering; priced higher, billed for hidden reasoning tokens. See the OpenAI dive's reasoning lesson. |

### Anthropic (Claude)

| Model | Model ID | Input $/1M | Output $/1M | Context |
|-------|----------|-----------:|------------:|--------:|
| Claude Haiku 4.5 | `claude-haiku-4-5` | 1.00 | 5.00 | 200K |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 3.00 | 15.00 | 1M |
| Claude Opus 4.8 | `claude-opus-4-8` | 5.00 | 25.00 | 1M |
| Claude Fable 5 | `claude-fable-5` | 10.00 | 50.00 | 1M |

The Claude dives default to **`claude-haiku-4-5`** for cheap iteration. Use exact
model IDs as written; don't append date suffixes. (Older Opus 4.6/4.7 are also
active at the same $5/$25 as 4.8.)

> Anthropic has no first-party embeddings model; it recommends **Voyage AI**
> (separate SDK + key). Voyage embedding prices: `voyage-3.5-lite` $0.02,
> `voyage-3.5` $0.06, `voyage-3-large` / `voyage-code-3` $0.18 per 1M input tokens.

---

## Embedding models

Embeddings turn text into a vector for search/RAG. There's no "output," so you pay
only for **input** tokens, and they're cheap.

| Model | Provider | $/1M input |
|-------|----------|-----------:|
| `text-embedding-3-small` | OpenAI | 0.02 |
| `text-embedding-3-large` | OpenAI | 0.13 |
| `text-embedding-ada-002` | OpenAI | 0.10 |
| `voyage-3.5-lite` | Voyage (Claude stack) | 0.02 |
| `voyage-3.5` | Voyage | 0.06 |
| `voyage-3-large` / `voyage-code-3` | Voyage | 0.18 |
| local (e.g. `nomic-embed-text`) | your machine | **$0** |

---

## Which model should I pick?

| Situation | Reach for |
|-----------|-----------|
| Learning, prototyping, high-volume simple tasks | **`gpt-4o-mini`** / **`claude-haiku-4-5`**, cheap and fast |
| Harder reasoning, code, nuanced writing | a mid/large model (`gpt-4o`, `claude-sonnet-4-6`) |
| The hardest multi-step / agentic / long-horizon work | a top model (`claude-opus-4-8`, `claude-fable-5`) |
| Math/logic/planning puzzles | a **reasoning** model (o-series; or Claude with extended thinking) |
| Privacy-sensitive or very high volume | a **local** open-weight model (zero per-token cost; see the Local Models dive) |
| A repeated, fixed-format task you can cheapen | **fine-tune** a small model (see the Fine-tuning dive) |

Rules of thumb: **start cheap and only move up when an eval says you need to**
(that's what the Evals dive is for); **don't pay top-tier prices for bottom-tier
questions** (route by difficulty; see the Production dive's model-routing lesson);
and **measure cost before you ship**, not after.

---

## Keeping this current

When a number here looks stale:

1. Check the provider pricing pages linked at the top.
2. For Claude, query the Models API for live context windows and capabilities.
3. Update the matching `utils/pricing.py` (OpenAI/Claude dives) and
   `ai-in-production-deep-dive/prod/cost.py` so the cost examples stay accurate.
