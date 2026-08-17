# Models & Pricing: a reference for the series

A quick, practical reference: the models these deep dives use, what they cost, and
how to choose one. Part of the [AI Engineering Deep Dives](README.md).

> ⚠️ **Prices and models change. This is a snapshot, last verified 2026-08-17.**
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

Prices and limits verified 2026-08-17. Everything current is on the GPT-5 line; the GPT-4
models below still serve but are a generation behind.

| Model | Input $/1M | Output $/1M | Context | Notes |
|-------|-----------:|------------:|--------:|-------|
| `gpt-5.6-sol` | 5.00 | 30.00 | 1.05M | Current flagship. Complex professional work. 128K max output. |
| `gpt-5.6-terra` | 2.00 | 12.00 | 1.05M | Current mid tier; balances cost and intelligence. 128K max output. |
| `gpt-5.6-luna` | 0.20 | 1.20 | 1.05M | Current cheap tier. 128K max output. **Reads cheap, behaves differently**: see the caveat below. |
| `gpt-5.4-mini` | 0.75 | 4.50 | 400K | Step up from nano when quality matters (judges, capstones). |
| `gpt-5.4-nano` | 0.20 | 1.25 | 400K | **The series default.** Vision, tools, and structured outputs, and it still accepts `temperature`. |
| `gpt-5-nano` | 0.05 | 0.40 | 400K | Cheapest current model. Weakest of the line; fine for classification. |
| `gpt-4o` | 2.50 | 10.00 | 128K | Previous generation. |
| `gpt-4o-mini` | 0.15 | 0.60 | 128K | Previous-generation cheap tier. Still the only line that accepts `stop`. |
| o-series (`o4-mini`, `o3`, `o1`) | varies | varies | large | **Reasoning models**: think before answering; billed for hidden reasoning tokens. See the OpenAI dive's reasoning lesson. |

> **Why the series defaults to `gpt-5.4-nano` and not the newer `gpt-5.6-luna`.**
> The 5.6 tiers reject `temperature`, `top_p`, and function calling on
> `/v1/chat/completions` unless you set `reasoning_effort: "none"` or move to the
> Responses API. `gpt-5.4-nano` defaults `reasoning.effort` to `none`, so tools
> and sampling knobs work the way the lessons describe, at the same price. This
> is a real tradeoff, not an oversight: the newest model is not automatically
> the right teaching default.

> **Long-context pricing:** for all three GPT-5.6 tiers, requests with more than
> 272K input tokens are billed at **2× input and 1.5× output for the full
> request**. Cache writes cost 1.25× the uncached input rate. A 1.05M context
> window is a capacity limit, not a promise that every token costs the base rate.

**Three parameter changes on the GPT-5 line** that will bite code written for
GPT-4:

| Parameter | What happened |
|-----------|---------------|
| `max_tokens` | Rejected. Use `max_completion_tokens`. It also covers reasoning tokens you never see, so a generous cap can still return an empty string. |
| `stop` | Removed from the whole GPT-5 line. Use structured outputs for a shape, `max_completion_tokens` for a length. |
| `temperature` / `top_p` | Fine on the 5.4 line; rejected on 5.6, which only accepts the default. |

### Anthropic (Claude)

| Model | Model ID | Input $/1M | Output $/1M | Context |
|-------|----------|-----------:|------------:|--------:|
| Claude Haiku 4.5 | `claude-haiku-4-5` | 1.00 | 5.00 | 200K |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 3.00 | 15.00 | 1M |
| Claude Sonnet 5 | `claude-sonnet-5` | 3.00 | 15.00 | 1M |
| Claude Opus 4.8 | `claude-opus-4-8` | 5.00 | 25.00 | 1M |
| Claude Opus 5 | `claude-opus-5` | 5.00 | 25.00 | 1M |
| Claude Fable 5 | `claude-fable-5` | 10.00 | 50.00 | 1M |

The Claude dives default to **`claude-haiku-4-5`** for cheap iteration. Use exact
model IDs as written; don't append date suffixes. (Older Opus 4.6/4.7 are also
active at the same $5/$25 as 4.8.)

Two things to know if you move the Claude dives off Haiku 4.5:

- **Thinking.** On 4.6 and newer, the fixed `budget_tokens` thinking budget is
  gone; you use `thinking: {"type": "adaptive"}` plus `output_config.effort`.
  Haiku 4.5 still uses the older `budget_tokens` form, which is why the dives
  read the way they do.
- **Assistant prefill.** Putting words in the assistant's mouth as the last
  message returns a 400 on Opus/Sonnet 4.6 and newer. Haiku 4.5 still allows it,
  and a couple of dives use it to force JSON. Use structured outputs instead if
  you upgrade.

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
| Learning, prototyping, high-volume simple tasks | **`gpt-5.4-nano`** / **`claude-haiku-4-5`**, cheap and fast |
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
