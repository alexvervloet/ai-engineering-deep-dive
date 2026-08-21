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

See also: [**HOW-LLMS-WORK.md**](docs/HOW-LLMS-WORK.md), what an LLM actually is ·
[**CHOOSING.md**](docs/CHOOSING.md), which technique to reach for ·
[**MODELS.md**](docs/MODELS.md), models & pricing · [**GLOSSARY.md**](docs/GLOSSARY.md), the
vocabulary · [**CAREERS.md**](docs/CAREERS.md), what each dive is called on a job
description · [**SAFETY.md**](docs/SAFETY.md), the cross-cutting safety view ·
[**RESPONSIBILITY.md**](docs/RESPONSIBILITY.md), building it responsibly ·
[**GOVERNANCE.md**](docs/GOVERNANCE.md), who decides and on what record ·
[**INCIDENTS.md**](docs/INCIDENTS.md), playbooks for when it goes wrong ·
[**AI-UX.md**](docs/AI-UX.md), the interface as part of the safety system ·
[**SECRETS.md**](docs/SECRETS.md), where your API keys go (not `.env`).

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
| [**AI Data Engineering**](ai-data-engineering-deep-dive/) | A retrieval index is a disposable view of source truth: ingest and version documents, preserve lineage and ACLs, propagate deletes, reconcile drift, and prove the corpus can be rebuilt. | RAG (4); before Production (8) |
| [**GenAI Security**](genai-security-deep-dive/) | Treat the model as an untrusted principal, not a security boundary: authorize effects in code, verify the supply chain, isolate data and execution, bound resources, and make attacks block releases. | Prompt Injection (7); before Production (8) |
| [**Multimodal**](multimodal-deep-dive/) | A multimodal model takes more than text: images and audio. Put the right modality in the right slot, and mind the token cost. | the API dives (1–2); pairs with RAG (4) |
| [**Realtime Voice**](realtime-voice-deep-dive/) | Conversational voice is a low-latency, full-duplex loop: stream audio both ways, handle interruption (barge-in), and choose a pipeline vs a speech-to-speech model. | Multimodal; the API dives (1–2) |
| [**Fine-tuning**](fine-tuning-deep-dive/) | Fine-tuning changes how a model *behaves*, not what it *knows*: teach behavior by example, then *prove* it beat your baseline. | RAG (4) + Evals (5) |
| [**MCP**](mcp-deep-dive/) | The Model Context Protocol: hand an LLM tools, data, and prompts from a separate process: write the server once, any client can use it. | Agents (6) |
| [**Local Models**](local-models-deep-dive/) | An open-weight model on your machine speaks the same OpenAI API, so "local" is mostly an *ops* choice: privacy, cost, control. | the API dives (1–2); pairs with Fine-tuning |
| [**Inference Platform Engineering**](inference-platform-deep-dive/) | A self-hosted model becomes a service only when memory and queue scheduling turn finite GPUs into measured latency, throughput, reliability, and cost. | Local Models; Production; Architecture |
| [**Observability**](observability-deep-dive/) | A prototype is judged once; a production system is judged continuously, so watch quality as a *trend*: drift, silent regressions, and alerting that doesn't cry wolf. | Production (8); pairs with Evals (5) |
| [**Architecture**](architecture-deep-dive/) | The seams between the components: where conversation state lives, what a queue buys, what streaming costs your guardrails, and where the tenant boundary goes. Each decision measured, not asserted. | Production (8); pairs with Observability |
| [**Testing & Delivery**](testing-and-delivery-deep-dive/) | A release is an evidence pipeline, not a push: independently defined requirements decide whether reproducible behavior, compatibility, security, rollout, and recovery evidence earns promotion. | Evals (5) + Production (8); pairs with GenAI Security |
| [**Professional Tools**](professional-tools-deep-dive/) | "Volume 2": rebuild each from-scratch primitive with the tool professionals actually reach for (LiteLLM, Instructor, LlamaIndex, DeepEval, LangGraph, Llama Guard, Langfuse) and measure both on the same eval, so "should we adopt this framework?" becomes an experiment, not a taste. | Everything (you need the primitives first) |

---

## Building this in TypeScript?

The series teaches in Python, because that is where the AI ecosystem's centre of
gravity still is. But most software that will call a language model is already
written, and a great deal of it is written in TypeScript.

> **[TypeScript AI Deep Dive](typescript-ai-deep-dive/)**: the same ideas in
> TypeScript, and an honest account of what actually changes. Your types stop at
> the network boundary, so everything a model says is `unknown` until you check
> it at runtime; every call is a promise; and one blocking handler stalls the
> whole process in a way you cannot detect from inside it. Thirteen runnable
> examples, twelve of which need no API key.

It is a **companion, not a step in the sequence**. Nothing above depends on it,
and it does not replace any dive: for depth on any subject it touches, the Python
dive on that subject goes much further. Read it if your AI work ships in
TypeScript, or if you want to know which of the differences are real and which
are folklore.

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
 │ Engineering  │  │   (4)   │               │  Local Models├─▶ Inference Platform (bonus)
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
 │   GenAI Security (bonus)     │  enforce identity, data, supply-chain,
 └──────────────┬───────────────┘  network, isolation & release boundaries
                ▼
 ┌──────────────────────────────┐
 │         Production (8)        │ ──────▶ Observability · Architecture  (bonus)
 └──────────────────────────────┘ ──────▶ Testing & Delivery             (bonus)
```

The thread: **build the call (1–2) → ask well (3) → ground it (4) → measure it (5) →
let it act (6) → harden it (7) → operate it (8).** The bonus dives branch off where
they're most useful. **Observability** extends Production from one request to six
weeks of them, and **Architecture** asks where all these parts belong once there
is more than one of everything. **Testing & Delivery** turns those quality,
security, and operational signals into reproducible promotion and rollback evidence.

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
[**SECRETS.md**](docs/SECRETS.md). Then run any key-using script as
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
| A complete document lifecycle, no key | [AI Data Engineering](ai-data-engineering-deep-dive/) (deterministic corpus and embeddings) |
| The complete AI security control plane, no key | [GenAI Security](genai-security-deep-dive/) (deterministic attacks and release gate) |
| A complete inference fleet control plane, no GPU | [Inference Platform Engineering](inference-platform-deep-dive/) (deterministic memory, scheduling, scaling, and rollout decisions) |
| A complete release-evidence pipeline, no services | [Testing & Delivery](testing-and-delivery-deep-dive/) (deterministic tests, gates, rollout, and rollback) |
| Six weeks of monitoring, no key | [Observability](observability-deep-dive/) (synthetic traffic) |
| Real models, no per-token bill | [Local Models](local-models-deep-dive/) (Ollama on your machine) |
| Offline sections | the first lesson in most repos (look for "offline, no key") |

---

## Reference docs

The series-level docs live in [**docs/**](docs/), grouped by what you need them
for. The full annotated index is [docs/README.md](docs/README.md).

**Foundations**, the shared vocabulary and the up-front decisions:
[HOW-LLMS-WORK.md](docs/HOW-LLMS-WORK.md) (what an LLM actually is) ·
[GLOSSARY.md](docs/GLOSSARY.md) (every term the series assumes) ·
[CHOOSING.md](docs/CHOOSING.md) (prompt → RAG → fine-tune → agent, and when) ·
[MODELS.md](docs/MODELS.md) (context windows, prices, which to default to).

**Practice**, how to run the lessons and what to build:
[SECRETS.md](docs/SECRETS.md) (where your API keys go, which is not `.env`) ·
[CAPSTONE.md](docs/CAPSTONE.md) (the whole-series build, one tag per dive) ·
[CAREERS.md](docs/CAREERS.md) (each dive as a résumé line and an interview answer) ·
[AUTHORING-LESSONS.md](docs/AUTHORING-LESSONS.md) (for anyone extending the series).

**Operating responsibly**, the concerns no single dive owns:
[SAFETY.md](docs/SAFETY.md) (injection, moderation, PII, hallucination) ·
[RESPONSIBILITY.md](docs/RESPONSIBILITY.md) (honest claims, bias, disclosure, and
whether this should be an LLM at all) ·
[GOVERNANCE.md](docs/GOVERNANCE.md) (who decides, on what record) ·
[INCIDENTS.md](docs/INCIDENTS.md) (what to do at 2am) ·
[AI-UX.md](docs/AI-UX.md) (the interface as part of the safety system).

Four docs stay at the root, because each mirrors a file every dive also has:
[TEXTBOOK.md](TEXTBOOK.md), the series read as one book ·
[LESSONS.md](LESSONS.md), what went wrong building it ·
[CHANGELOG.md](CHANGELOG.md), what changed and when · and this README.

---

## A note on cost & safety

- **Cost:** most lessons cost a fraction of a cent; the ones that make no API call
  are marked **(offline)**. The token-counting and cost sections teach you to
  estimate spend *before* you send. See [MODELS.md](docs/MODELS.md).
- **Safety:** the [Prompt Injection & Guardrails](prompt-injection-deep-dive/) and
  [GenAI Security](genai-security-deep-dive/) dives are strictly *defensive*: every
  attack targets only a deterministic toy system and uses made-up secrets that protect
  nothing. Use them to harden systems you own or are authorized to test.
