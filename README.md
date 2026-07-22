# AI Engineering: Deep Dives

A series of **hands-on, build-it-from-scratch** courses for learning to build with
LLMs. Each one is a standalone repository you *walk through*: every concept is a
small, runnable Python script, every section ends with something to run, and the
first runnable thing in most repos is **offline and free**. No frameworks, no magic
and just enough code to see how each piece works.

They share one house style: provider-agnostic where it makes sense (OpenAI **or**
Claude, often a local model too), offline-first examples, a real capstone, and an
`EXERCISES.md` with predict-then-run prompts. Assumes only basic Python.

> New here? Start with [**openai-api-deep-dive**](openai-api-deep-dive/) (or
> [claude-api-deep-dive](claude-api-deep-dive/) if you prefer Anthropic). Then follow
> the sequence below. Already comfortable with the API? Jump to whatever you need.

See also: [**HOW-LLMS-WORK.md**](HOW-LLMS-WORK.md), what an LLM actually is ·
[**CHOOSING.md**](CHOOSING.md), which technique to reach for ·
[**MODELS.md**](MODELS.md), models & pricing · [**GLOSSARY.md**](GLOSSARY.md), the
vocabulary · [**CAREERS.md**](CAREERS.md), what each dive is called on a job
description · [**SAFETY.md**](SAFETY.md), the cross-cutting safety view ·
[**RESPONSIBILITY.md**](RESPONSIBILITY.md), building it responsibly ·
[**SECRETS.md**](SECRETS.md), where your API keys go (not `.env`).

---

## The core path (do these in order)

The eight build on each other: the first two teach the API call, then each adds a
layer until you're operating a real app end to end.

| # | Deep dive | The one big idea |
|---|-----------|------------------|
| 1 | [**OpenAI API**](openai-api-deep-dive/) | You send a list of messages. You get back a message. Everything else is detail on that request. |
| 2 | [**Claude API**](claude-api-deep-dive/) | The same idea, the Anthropic way: content blocks, tool use, and extended thinking. |
| 3 | [**Prompt Engineering**](prompt-engineering-deep-dive/) | Shape what the model does with how you ask: zero/few-shot, chain-of-thought, roles, structure. |
| 4 | [**RAG**](rag-deep-dive/) | A model can only answer from what's in its context window. RAG is the discipline of putting the *right* text there. |
| 5 | [**Evals**](evals-deep-dive/) | If you can't measure it, you can't improve it: make your app's quality a number you can rerun. |
| 6 | [**Agents**](agents-deep-dive/) | An agent is a loop: the model picks a tool, you run it, you feed the result back, until it's done. |
| 7 | [**Prompt Injection & Guardrails**](prompt-injection-deep-dive/) | Treat everything the model reads and writes as untrusted: contain the blast radius. |
| 8 | [**Production**](ai-in-production-deep-dive/) | The model call is one line. Production is the dozen lines around it that make it safe, cheap, observable, and reliable. |

## Bonus dives

Standalone deep dives that extend the core path. Each notes where it slots in.

| Deep dive | The one big idea | Slots in after |
|-----------|------------------|----------------|
| [**Agent Harnesses**](agent-harness-deep-dive/) | Once you've hand-written the loop, most agent work is building *on* a harness: the layer that adds hooks, permission policies, sandboxing, subagents, and headless runs around it. | Agents (6) |
| [**Context Engineering**](context-engineering-deep-dive/) | The model only knows what's in its context window, so manage it: conversation memory, compaction, long-term recall, and what to drop when it won't all fit. | Agents (6); pairs with RAG (4) |
| [**Multimodal**](multimodal-deep-dive/) | A multimodal model takes more than text: images and audio. Put the right modality in the right slot, and mind the token cost. | the API dives (1–2); pairs with RAG (4) |
| [**Realtime Voice**](realtime-voice-deep-dive/) | Conversational voice is a low-latency, full-duplex loop: stream audio both ways, handle interruption (barge-in), and choose a pipeline vs a speech-to-speech model. | Multimodal; the API dives (1–2) |
| [**Fine-tuning**](fine-tuning-deep-dive/) | Fine-tuning changes how a model *behaves*, not what it *knows*: teach behavior by example, then *prove* it beat your baseline. | RAG (4) + Evals (5) |
| [**MCP**](mcp-deep-dive/) | The Model Context Protocol: hand an LLM tools, data, and prompts from a separate process: write the server once, any client can use it. | Agents (6) |
| [**Local Models**](local-models-deep-dive/) | An open-weight model on your machine speaks the same OpenAI API, so "local" is mostly an *ops* choice: privacy, cost, control. | the API dives (1–2); pairs with Fine-tuning |
| [**Observability**](observability-deep-dive/) | A prototype is judged once; a production system is judged continuously, so watch quality as a *trend*: drift, silent regressions, and alerting that doesn't cry wolf. | Production (8); pairs with Evals (5) |
| [**Professional Tools**](professional-tools-deep-dive/) | "Volume 2": rebuild each from-scratch primitive with the tool professionals actually reach for (LiteLLM, Instructor, LlamaIndex, DeepEval, LangGraph, Llama Guard, Langfuse) and measure both on the same eval, so "should we adopt this framework?" becomes an experiment, not a taste. | Everything (you need the primitives first) |

---

## How they fit together

```
        ┌─────────────┐   ┌─────────────┐
        │  OpenAI API │   │  Claude API │      1 · 2: the API call
        └──────┬──────┘   └──────┬──────┘
               └────────┬─────────┘
        ┌───────────────┼───────────────────────────┐
        ▼               ▼                            ▼
 ┌──────────────┐  ┌─────────┐               ┌──────────────┐
 │   Prompt     │  │   RAG   │               │  Multimodal ─┼─▶ Realtime Voice  (bonus)
 │ Engineering  │  │   (4)   │               │  Local Models│  (bonus)
 │     (3)      │  └────┬────┘               └──────────────┘
 └──────┬───────┘       │
        │          ┌────▼────┐
        │          │  Evals  │ ─────────────▶ Fine-tuning   (bonus)
        │          │   (5)   │
        │          └────┬────┘
        ▼               ▼
 ┌──────────────────────────────┐
 │           Agents (6)         │ ──────▶ Agent Harnesses · MCP · Context Eng.  (bonus)
 └──────────────┬───────────────┘
                ▼
 ┌──────────────────────────────┐
 │ Prompt Injection & Guardrails│  (7): attack & defend all of the above
 └──────────────┬───────────────┘
                ▼
 ┌──────────────────────────────┐
 │         Production (8)        │ ──────▶ Observability  (bonus)
 └──────────────────────────────┘  operate one app end to end
```

The thread: **build the call (1–2) → ask well (3) → ground it (4) → measure it (5) →
let it act (6) → harden it (7) → operate it (8).** The bonus dives branch off where
they're most useful. **Observability** extends Production from one request to six
weeks of them.

---

## Setup (the same everywhere)

Every repo is self-contained with an identical setup. Inside any one:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # config only (PROVIDER, MODEL); no keys go here
python check_setup.py              # verifies your environment; makes no API call
```

**Your API key does not go in `.env`.** Store it in your OS keychain and inject
it per-command with `secrun`: a 2-minute, one-time setup in
[**SECRETS.md**](SECRETS.md). Then run any key-using script as
`secrun python examples/…`; offline examples need no wrapper. (`.env` is for the
non-secret `PROVIDER`/`MODEL` config only.)

`check_setup.py` is always your first stop; it checks your Python version,
packages, provider, and key, and tells you exactly what to fix. Run it as
`secrun python check_setup.py` so it can see your keychain-stored key.

**You can learn a lot for free.** The Production dive runs entirely on an offline
mock (no key, ever); the Local Models dive runs open weights on your own machine;
and most other repos have offline, no-cost first sections (token math, chunking,
the eval anatomy, the injection attack catalog, the quantization calculator).

| To run for $0 | Use |
|---------------|-----|
| The whole ops stack, no key | [Production](ai-in-production-deep-dive/) (mock provider) |
| Six weeks of monitoring, no key | [Observability](observability-deep-dive/) (synthetic traffic) |
| Real models, no per-token bill | [Local Models](local-models-deep-dive/) (Ollama on your machine) |
| Offline sections | the first lesson in most repos (look for "offline, no key") |

---

## Reference docs

- [**HOW-LLMS-WORK.md**](HOW-LLMS-WORK.md): the mental model underneath the whole
  series: next-token prediction, training, why models hallucinate, the context
  window. No math. Read it first if "what *is* an LLM?" is still fuzzy.
- [**CHOOSING.md**](CHOOSING.md): a decision guide: prompt → few-shot → RAG →
  fine-tune → agent, and when to reach for multimodal, local, or MCP.
- [**MODELS.md**](MODELS.md): the models the series uses, their context windows and
  prices, and how to pick one. Dated; tells you how to get current numbers.
- [**GLOSSARY.md**](GLOSSARY.md): every term the series assumes (token, embedding,
  context window, temperature, RAG, agent, eval, guardrail, quantization, …).
- [**CAREERS.md**](CAREERS.md): the hirability map: each dive translated into the
  résumé lines, job-description phrases, and industry tools (Braintrust, Langfuse,
  pgvector, vLLM, LiveKit, …) it corresponds to, so you can turn the work into
  interview answers.
- [**SAFETY.md**](SAFETY.md): the cross-cutting view: injection, moderation, PII,
  hallucination, and unsafe actions: what each is and which dive covers it.
- [**RESPONSIBILITY.md**](RESPONSIBILITY.md): the other half of safety: honest
  capability claims, bias & fairness, disclosure, data consent, human accountability,
  and the question upstream of all of them: *should* this be an LLM?
- [**SECRETS.md**](SECRETS.md): where your API keys actually go (your OS keychain,
  injected per-command with `secrun`) and why not `.env`. The `.env` → keychain
  progression is itself a lesson in the AI-agent threat model.
- [**CAPSTONE.md**](CAPSTONE.md): the whole-series capstone: a codebase Q&A tool
  (`askrepo`) built step by step, one dive per tag, with its eval set pointed at
  this very repo. The build itself lives in
  [**deep-dive-capstone**](deep-dive-capstone/), one tag per step from
  `v00-scaffold` to `v07-production`.
- [**AUTHORING-LESSONS.md**](AUTHORING-LESSONS.md): for anyone extending these dives:
  principles for writing runnable teaching examples that actually prove their own
  claim, drawn from hardening the RAG examples. The reader believes the output, so
  the output has to be worth believing.

---

## A note on cost & safety

- **Cost:** most lessons cost a fraction of a cent; the ones that make no API call
  are marked **(offline)**. The token-counting and cost sections teach you to
  estimate spend *before* you send. See [MODELS.md](MODELS.md).
- **Safety:** the [Prompt Injection & Guardrails](prompt-injection-deep-dive/) dive
  is strictly *defensive*: every attack targets only its own toy bot, whose
  "secret" is a made-up passphrase that protects nothing. Use it to harden systems
  you own or are authorized to test.
