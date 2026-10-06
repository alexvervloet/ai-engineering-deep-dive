# Models and pricing

Which models these deep dives use, what they cost, and how to choose one. Part of the
[AI Engineering Deep Dives](../README.md).

> **Prices and models change. This is a snapshot, last verified 2026-10-06.**
> Always confirm against the provider's own page before relying on a number.
> [OpenAI pricing](https://platform.openai.com/docs/pricing) ·
> [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing).
> For Claude you can also query live capability/price data with the **Models API**
> (`client.models.retrieve("claude-opus-5-5")` → `max_input_tokens`, `max_tokens`,
> `capabilities`). The numbers below mirror the pricing modules the repos ship
> (`utils/pricing.py`, `prod/cost.py`), so the cost examples match this table.

---

## The one mental model

You pay per token. Input tokens (the ones you send) and output tokens (the ones the
model generates) are priced separately, and output costs several times more. A token is
roughly three quarters of an English word, about four characters. Prices below are US
dollars per 1,000,000 tokens.

```
cost ≈ (input_tokens × input_price + output_tokens × output_price) / 1,000,000
```

Two levers shrink the bill without changing the model. Prompt caching bills a long,
repeated prefix at about 0.1× on cache reads (0.05× on Claude Opus 5.5), and the Batch
API takes 50% off non-urgent work. The API dives cover both.

---

## Chat models

### OpenAI

Prices and limits verified 2026-10-03. The GPT-6 line now has three tiers, Astra, Sol
and Luna, and the series runs on `gpt-6-luna`. The GPT-5 models below are still served.
The GPT-4 models still work, one generation behind.

| Model | Input $/1M | Output $/1M | Context | Notes |
|-------|-----------:|------------:|--------:|-------|
| `gpt-6-astra` | 10.00 | 50.00 | 1.05M | Current flagship, released 2026-09-03. 128K max output. **Tool calling requires the Responses API**: see the caveat below. |
| `gpt-6.1-sol` | 2.00 | 10.00 | 1.05M | Released 2026-09-29. No `"none"` effort; tool calling requires the Responses API. |
| `gpt-6-sol` | 2.00 | 10.00 | 1.05M | Released 2026-09-22. Mid tier. |
| `gpt-6-luna` | 0.10 | 0.50 | 1.05M | **The series default.** Released 2026-09-22. 128K max output. Reasons by default: see the caveat below. |
| `gpt-5.6-sol` | 4.00 | 20.00 | 1.05M | Top of the 5.6 line. 128K max output. The $4/$20 is promotional through at least 2026-11-21; the list price was $5/$30. |
| `gpt-5.6-terra` | 2.00 | 12.00 | 1.05M | Mid tier; balances cost and intelligence. 128K max output. |
| `gpt-5.6-luna` | 0.20 | 1.20 | 1.05M | Cheap tier. 128K max output. **Reads cheap, behaves differently**: see the caveat below. |
| `gpt-5.5` | 5.00 | 30.00 | 1.05M | Sits between the 5.4 and 5.6 lines. Effort defaults to `"medium"`. |
| `gpt-5.4` | 2.50 | 15.00 | 1.05M | Effort defaults to `"none"`. |
| `gpt-5.4-mini` | 0.75 | 4.50 | 400K | Step up from nano when quality matters (judges, capstones). |
| `gpt-5.4-nano` | 0.20 | 1.25 | 400K | The previous series default. **Deprecated 2026-10-01, shuts down 2027-04-01**; `gpt-6-luna` replaces it. |
| `gpt-5-nano` | 0.05 | 0.40 | 400K | Cheapest model listed, weakest of the line. **Its only snapshot shuts down 2026-12-11**; OpenAI names `gpt-5.6-luna` as the replacement. |
| `gpt-4o` | 2.50 | 10.00 | 128K | Previous generation. Not deprecated. |
| `gpt-4o-mini` | 0.15 | 0.60 | 128K | Previous-generation cheap tier. Still the only line that accepts `stop`. |

Cached input reads bill at 10% of the input rate on the 5.6 tiers and Astra. Cache
*writes* are a separate price line on GPT-5.6 and later, at 1.25x the uncached input
rate: $12.50 per 1M on Astra. Moving code to GPT-6 also means replacing
`prompt_cache_retention` with `prompt_cache_options.ttl` (for example `"30m"`).

Astra also has a new **Ultrafast** service tier (`service_tier: "ultrafast"`, Responses
API only) at $60 in / $300 out per 1M, six times the standard price, for faster
generation. It's the price-for-latency trade the Production dive's routing lesson
describes, taken to an extreme: check whether the wait is the actual problem first.

> **The o-series is being switched off.** `o1`, `o1-pro`, and `o4-mini` shut down on
> **2026-10-23**, and the 2025 `o3` snapshots on **2026-12-11**. Don't start anything on
> them. Reasoning is no longer a separate family of models: it's the `reasoning_effort`
> dial on the mainline tiers. The values are model-dependent and can include `"none"`,
> `"minimal"`, `"low"`, `"medium"`, `"high"`, `"xhigh"`, and `"max"`, and so are the
> defaults: the GPT-5.6 tiers and `gpt-5.4` start at `"none"`, `gpt-6-luna` and
> `gpt-5.5` at `"medium"`, and Astra and 6.1-sol have no `"none"` at all. Check the
> model page rather than assuming.

> **Astra and tools.** GPT-6 Astra supports chat completions for text only. Every Astra
> workflow that calls tools has to move to the Responses API. It also rejects
> `temperature`, `top_p`, `logprobs`, and `top_logprobs` outright, and dropped the
> `"none"` effort level and `prompt_cache_retention` (now `prompt_cache_options.ttl`). The same wall shows up one tier
> down: on chat completions the GPT-5.6 tiers return a 400 for function tools combined
> with any `reasoning_effort` above `"none"`. If you want tools and thinking together,
> you want Responses. The OpenAI dive's `responses/` directory covers it.

> **Why every OpenAI call in the series sends `reasoning_effort="none"`.** `gpt-6-luna`
> defaults to `"medium"` effort. While it's reasoning, it rejects `temperature` and
> `top_p`, rejects function tools on chat completions (a 400, not a weaker answer), and
> spends hidden tokens that count against `max_completion_tokens`. With `"none"` it
> behaves like `gpt-5.4-nano` did: temperature, tools, structured outputs, logprobs, and
> vision all work, at half nano's price. All of that was probed against the live API on
> 2026-10-03. The catch is that `"none"` isn't universal. It works on every `gpt-5.x`
> id, `gpt-6-luna`, and `gpt-6-sol`. It's a 400 on `gpt-5-nano`, `gpt-6-astra`, and
> `gpt-6.1-sol`, and `gpt-4o`/`gpt-4o-mini` reject the parameter entirely. So code that
> lets you pick the model only sends it to models that take it.

> **Images cost more on luna unless you set `detail`.** Both nano and luna bill about
> 1.2 tokens per 32x32-pixel patch, and `"high"` shrinks big images to cap at 3,000
> tokens. Leave `detail` out and nano treated it like `"high"`, but luna doesn't shrink
> at all: a 3000x3000 photo cost 10,603 tokens on luna against 3,000 on nano. Half the
> price per token, about 1.8 times the price per photo. Past 30,000 patches luna returns
> a 400. The Multimodal dive has the measured table.

> **One dive deliberately stays on an older model.** Prompt Injection attacks
> `gpt-4o-mini`. Its indirect attacks landed 30 of 40 times on `gpt-4o-mini` and on
> nano, and 0 of 40 on luna. A lesson about building defenses needs an attack that
> works first, and the zero is resistance to four public strings, not safety.

> **Long-context pricing.** On the models with a 1.05M window (the GPT-5.4, 5.5, 5.6
> and 6 lines), a request with more than 272K input tokens bills at 2× input and 1.5×
> output for the whole request. Cache writes
> cost 1.25× the uncached input rate. A 1.05M context window is a capacity limit, not
> a promise that every token costs the base rate.

Three parameter changes on the GPT-5 line will bite code written for GPT-4.

| Parameter | What happened |
|-----------|---------------|
| `max_tokens` | Rejected. Use `max_completion_tokens`. It also covers reasoning tokens you never see, so a generous cap can still return an empty string. |
| `stop` | Removed from the whole GPT-5 line. Use structured outputs for a shape, `max_completion_tokens` for a length. |
| `temperature` / `top_p` | Only accepted with reasoning off. Luna and the 5.6 tiers take them at `reasoning_effort="none"` and reject them at any other effort; Astra and 6.1-sol can't switch reasoning off, so they never take them. |

### Anthropic (Claude)

| Model | Model ID | Input $/1M | Output $/1M | Context |
|-------|----------|-----------:|------------:|--------:|
| Claude Haiku 4.5 | `claude-haiku-4-5` | 1.00 | 5.00 | 200K |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 2.00 | 10.00 | 1M |
| Claude Sonnet 5 | `claude-sonnet-5` | 2.00 | 10.00 | 1M |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 3.00 | 15.00 | 1M |
| Claude Opus 5.5 | `claude-opus-5-5` | 4.00 | 20.00 | 1M |
| Claude Opus 5 | `claude-opus-5` | 5.00 | 25.00 | 1M |
| Claude Opus 4.8 | `claude-opus-4-8` | 5.00 | 25.00 | 1M |
| Claude Fable 5.1 | `claude-fable-5-1` | 10.00 | 50.00 | 1M |
| Claude Fable 5 | `claude-fable-5` | 10.00 | 50.00 | 1M |

The Claude dives default to `claude-haiku-4-5` for cheap iteration. Use the exact model
IDs as written and don't append date suffixes. Older Opus 4.6 and 4.7 are also active,
at the same $5/$25 as 4.8. Fable 5.1 is the most capable widely released model.

Read the Sonnet and Opus rows in order. Sonnet 5 is **cheaper** than the Sonnet 4.6 it
succeeded, $2/$10 against $3/$15, and Sonnet 5.5 kept that price. Opus 5.5 is cheaper
than Opus 5, $4/$20 against $5/$25, and bills cache hits at 0.05× input instead of the
usual 0.1×. "Pick the older model to save money" is a guess that's now been wrong twice,
and the only way to know is to look.

Four things to know if you move the Claude dives off Haiku 4.5:

- **Thinking.** On 4.6 and newer, the fixed `budget_tokens` thinking budget is
  gone; you use `thinking: {"type": "adaptive"}` plus `output_config.effort`.
  It's deprecated but still functional on Opus 4.6 and Sonnet 4.6, and returns a
  400 on Opus 4.7 and everything after. Haiku 4.5 still uses the older
  `budget_tokens` form, which is why the dives read the way they do.
- **Sampling knobs.** `temperature`, `top_p`, and `top_k` are **removed** on 4.7
  and newer, and return a 400. Haiku 4.5 still accepts them. The `anthropic` SDK
  dropped them from the Messages method signatures in 1.0 as well, so on a model
  that still takes them you now pass `extra_body={"temperature": 0.2}`. The
  Claude dive's temperature and top-p lessons run on Haiku for exactly this
  reason.
- **Assistant prefill.** Putting words in the assistant's mouth as the last
  message returns a 400 on Opus/Sonnet 4.6 and newer. Haiku 4.5 still allows it,
  and a couple of dives use it to force JSON. Use structured outputs instead if
  you upgrade.
- **Forced tool use.** `tool_choice` of `{"type": "any"}` or a named tool returns a
  400 on Opus 5.5, Sonnet 5.5, and Fable 5.1. The Prompt Engineering dive's
  `structured()` and the TypeScript dive's provider force a tool on the Claude path
  to get JSON back; that works on Haiku and breaks on those three. Use
  `tool_choice: auto` with `strict: true`, or structured outputs. Thinking also
  changed: it can't be turned off at all on Opus 5.5 (lower the effort instead, whose
  default there is `"medium"`), and Sonnet 5.5 turns it off with
  `thinking: {"type": "between_tools"}` rather than `"disabled"`.

> Anthropic has no first-party embeddings model and recommends Voyage AI, which needs
> its own SDK and key. Voyage embedding prices per 1M input tokens: `voyage-3.5-lite`
> $0.02, `voyage-3.5` $0.06, `voyage-3-large` and `voyage-code-3` $0.18.

---

## Embedding models

Embeddings turn text into a vector for search and RAG. There's no output, so you pay
for input tokens only, and they're cheap.

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

## Audio models

Speech doesn't ride in a chat content block on these APIs. It goes to dedicated
endpoints, and it's billed per minute rather than per token. OpenAI only; Claude has no
native audio API.

| Model | Job | $/minute |
|-------|-----|---------:|
| `gpt-transcribe` | Speech to text on a completed file | 0.0045 |
| `gpt-live-transcribe` | Speech to text on a live stream | 0.017 |
| `gpt-4o-mini-tts` | Text to speech | billed per token of input text |
| `gpt-live-1` | Full-duplex voice sessions on `v1/live/sessions`, GA 2026-09-10 | 0.05 |

`gpt-4o-mini-tts`, `tts-1` and `tts-1-hd` were deprecated on 2026-10-01 and shut down
**2027-01-06**. OpenAI's named replacement, `gpt-realtime-2.1-mini`, only runs over the
Realtime API, a streaming session, so there's no like-for-like swap on the simple speech
endpoint yet. The older realtime and audio models (`gpt-realtime`, `gpt-realtime-mini`,
`gpt-4o-realtime`, `gpt-4o-mini-realtime`, `gpt-audio`, `gpt-audio-mini`) shut down
**2027-01-20**; the Realtime Voice dive runs on a simulator, so it isn't affected.

`whisper-1` is deprecated and shuts down **2027-02-26**. `gpt-transcribe` replaced it,
with lower error rates at a lower price, but it doesn't do everything Whisper did: no
word-level timestamps, no SRT or VTT subtitle export, and no translate-to-English
endpoint. If you depend on any of those, that date is your deadline to find another
source. The open Whisper weights are one, since those don't retire with the endpoint.

---

## Image generation models

Billed in tokens like chat, but image output tokens are expensive. OpenAI only.

| Model | Text in $/1M | Image in $/1M | Image out $/1M | Notes |
|-------|-------------:|--------------:|---------------:|-------|
| `gpt-image-2.5-flare` | 5.00 | 8.00 | 30.00 | Fast, everyday generation. The Multimodal dive's default. |
| `gpt-image-2.5-sunburst` | 5.00 | 8.00 | 30.00 | For edits where precision matters. |

Both take `quality` from `"low"` to `"max"`, plus `"auto"`, the default, which lets the
model choose. Set it on purpose: a 1024x1024 Flare image measured about $0.006 at
`"low"` and $0.013 at `"medium"` on 2026-10-05. `gpt-image-1` shuts down **2026-10-23**,
and `gpt-image-1-mini` and `gpt-image-1.5` follow on **2026-12-01**.

---

## Which model should I pick?

| Situation | Reach for |
|-----------|-----------|
| Learning, prototyping, high-volume simple tasks | **`gpt-6-luna`** (reasoning off) / **`claude-haiku-4-5`**, cheap and fast |
| Harder reasoning, code, nuanced writing | a mid tier (`gpt-6-sol`, `claude-sonnet-5-5`), or luna with the effort dial turned up |
| The hardest multi-step / agentic / long-horizon work | a top model (`gpt-6-astra`, `claude-opus-5-5`, `claude-fable-5-1`) |
| Math/logic/planning puzzles | any current tier with the thinking dial turned up: `reasoning_effort` on OpenAI, adaptive thinking plus `output_config.effort` on Claude |
| Privacy-sensitive or very high volume | a **local** open-weight model (zero per-token cost; see the Local Models dive) |
| A repeated, fixed-format task you can cheapen | **fine-tune** a small model, if you still can (see the Fine-tuning dive; OpenAI's self-serve fine-tuning is winding down and closes to existing customers on 2027-01-06) |

Four rules of thumb. Start cheap and move up only when an eval says you need to, which
is what the Evals dive is for. Don't pay top-tier prices for bottom-tier questions, so
route by difficulty, as the Production dive's model-routing lesson shows. Measure cost
before you ship rather than after.

And try the effort dial before you try a bigger model. Effort is a per-request setting
that trades tokens for thoroughness inside one model, and it's usually the cheaper
experiment: the same model at lower effort often beats the previous generation at high
effort, and staying on one model keeps one prompt cache rather than splitting it across
a cascade. Caches are model-scoped, so a routing cascade forfeits reuse between its
models. That's a real cost that model-routing comparisons usually leave out.

---

## Keeping this current

When a number here looks stale:

1. Check the provider pricing pages linked at the top.
2. For Claude, query the Models API for live context windows and capabilities.
3. Update the matching `utils/pricing.py` (OpenAI/Claude dives) and
   `ai-in-production-deep-dive/prod/cost.py` so the cost examples stay accurate.
