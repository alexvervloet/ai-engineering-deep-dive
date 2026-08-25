# AI Engineering: Deep Dives

[![Verify offline paths](https://github.com/alexvervloet/ai-engineering-deep-dive/actions/workflows/verify-offline.yml/badge.svg)](https://github.com/alexvervloet/ai-engineering-deep-dive/actions/workflows/verify-offline.yml)

A series of hands-on, build-it-from-scratch courses for learning to build with LLMs.
Each one is a standalone repository you walk through. Every concept is a small
runnable Python script, every section ends with something to run, and in most repos
the first runnable thing needs no API key. No frameworks, no magic, just enough code
to see how each piece works.

They share one house style. Provider-agnostic where it makes sense (OpenAI or Claude,
often a local model too), offline-first examples, a real capstone, and an
`EXERCISES.md` full of predict-then-run prompts. Assumes only basic Python.

> New here? Start with [openai-api-deep-dive](openai-api-deep-dive/), or
> [claude-api-deep-dive](claude-api-deep-dive/) if you prefer Anthropic. Then follow
> the sequence below. Already comfortable with the API? Jump to whatever you need.

See also: [HOW-LLMS-WORK.md](docs/HOW-LLMS-WORK.md), what an LLM actually is ·
[CHOOSING.md](docs/CHOOSING.md), which technique to reach for ·
[MODELS.md](docs/MODELS.md), models and pricing · [GLOSSARY.md](docs/GLOSSARY.md), the
vocabulary · [CAREERS.md](docs/CAREERS.md), what each dive is called on a job
description · [SAFETY.md](docs/SAFETY.md), the cross-cutting safety view ·
[RESPONSIBILITY.md](docs/RESPONSIBILITY.md), building it responsibly ·
[GOVERNANCE.md](docs/GOVERNANCE.md), who decides and on what record ·
[INCIDENTS.md](docs/INCIDENTS.md), playbooks for when it goes wrong ·
[AI-UX.md](docs/AI-UX.md), the interface as part of the safety system ·
[SECRETS.md](docs/SECRETS.md), where your API keys go (not `.env`).

---

## Is this safe to run?

A fair thing to ask of a stranger's repo, so here is the short version. The details,
including what to do if you find something, are in [SECURITY.md](SECURITY.md).

- No install script, and nothing here asks you to pipe a URL into a shell.
- No binaries. The parent repo is markdown, two Python scripts, one workflow file,
  and the social cards.
- No telemetry. The only network calls go to the model provider you configure, and
  lessons marked **(offline)** make none at all.
- All 25 submodules point at repos under this same account. Check for yourself with
  `git config -f .gitmodules --get-regexp url`.
- Every commit is signed, and CI installs and runs the offline path of all 25 dives
  on a clean GitHub runner on every push. Those logs are public and I do not control
  the machine.

What you are actually trusting is PyPI, because dependencies are version ranges
rather than hash pins, and whichever model provider you point at. If you would rather
not trust me at all, everything runs in a container, and the offline paths run with
the network switched off.

---

## The core path (do these in order)

The eight build on each other. The first two teach the API call, then each one adds a
layer until you are operating a real app end to end.

| # | Deep dive | The one big idea |
|---|-----------|------------------|
| 1 | [OpenAI API](openai-api-deep-dive/) | You send a list of messages. You get back a message. Everything else is detail on that request. |
| 2 | [Claude API](claude-api-deep-dive/) | The same idea done the Anthropic way, with content blocks, tool use, and extended thinking. |
| 3 | [Prompt Engineering](prompt-engineering-deep-dive/) | How you ask shapes what the model does. Zero-shot, few-shot, chain-of-thought, roles, structure. |
| 4 | [RAG](rag-deep-dive/) | A model can only answer from what is in its context window. RAG is the discipline of putting the right text there. |
| 5 | [Evals](evals-deep-dive/) | If you cannot measure it you cannot improve it. Turn your app's quality into a number you can rerun. |
| 6 | [Agents](agents-deep-dive/) | An agent is a loop. The model picks a tool, you run it, you feed the result back, and you repeat until it is done. |
| 7 | [Prompt Injection & Guardrails](prompt-injection-deep-dive/) | Everything the model reads and writes is untrusted. Contain the blast radius. |
| 8 | [Production](ai-in-production-deep-dive/) | The model call is one line. Production is the dozen lines around it that make it safe, cheap, observable, and reliable. |

## Bonus dives

Standalone deep dives that extend the core path. Each one notes where it slots in.

| Deep dive | The one big idea | Slots in after |
|-----------|------------------|----------------|
| [Agent Harnesses](agent-harness-deep-dive/) | Once you have hand-written the loop, most agent work happens on top of a harness. That layer adds hooks, permission policies, sandboxing, subagents, and headless runs. | Agents (6) |
| [Context Engineering](context-engineering-deep-dive/) | The model only knows what is in its context window, so manage it. Conversation memory, compaction, long-term recall, and what to drop when it will not all fit. | Agents (6); pairs with RAG (4) |
| [AI Data Engineering](ai-data-engineering-deep-dive/) | A retrieval index is a disposable view of source truth. Ingest and version documents, preserve lineage and ACLs, propagate deletes, reconcile drift, and prove the corpus can be rebuilt. | RAG (4); before Production (8) |
| [GenAI Security](genai-security-deep-dive/) | The model is an untrusted principal, not a security boundary. Authorize effects in code, verify the supply chain, isolate data and execution, bound resources, and make attacks block releases. | Prompt Injection (7); before Production (8) |
| [Multimodal](multimodal-deep-dive/) | A multimodal model takes more than text. Put the right images and audio in the right slot, and mind the token cost. | the API dives (1–2); pairs with RAG (4) |
| [Realtime Voice](realtime-voice-deep-dive/) | Conversational voice is a low-latency, full-duplex loop. Stream audio both ways, handle interruption (barge-in), and choose between a pipeline and a speech-to-speech model. | Multimodal; the API dives (1–2) |
| [ML Foundations for AI Engineers](ml-foundations-for-ai-engineers/) | A model is a chain of numeric contracts. Trace shapes, logits, loss, gradients, masked attention, sampling, calibration, quantization, and retained memory through runnable NumPy and PyTorch code. | the API dives (1–2); before Fine-tuning, Local Models, and Inference Platforms |
| [Fine-tuning](fine-tuning-deep-dive/) | Fine-tuning changes how a model behaves, not what it knows. Teach behavior by example, then prove it beat your baseline. | RAG (4) + Evals (5) |
| [MCP](mcp-deep-dive/) | The Model Context Protocol hands an LLM tools, data, and prompts from a separate process. Write the server once and any client can use it. | Agents (6) |
| [Local Models](local-models-deep-dive/) | An open-weight model on your machine speaks the same OpenAI API, so running local is mostly an ops choice about privacy, cost, and control. | the API dives (1–2); pairs with Fine-tuning |
| [Inference Platform Engineering](inference-platform-deep-dive/) | A self-hosted model becomes a service only when memory and queue scheduling turn finite GPUs into measured latency, throughput, reliability, and cost. | Local Models; Production; Architecture |
| [Observability](observability-deep-dive/) | A prototype gets judged once. A production system gets judged continuously, so watch quality as a trend: drift, silent regressions, and alerting that does not cry wolf. It ends by emitting the same telemetry as real OpenTelemetry over OTLP, so you can see which half of the problem the standard actually solves. | Production (8); pairs with Evals (5) |
| [Architecture](architecture-deep-dive/) | The seams between the components. Where conversation state lives, what a queue buys, what streaming costs your guardrails, and where the tenant boundary goes. Every decision measured rather than asserted. | Production (8); pairs with Observability |
| [Testing & Delivery](testing-and-delivery-deep-dive/) | A release is an evidence pipeline. Requirements defined independently decide whether the reproducibility, compatibility, security, rollout, and recovery evidence is good enough to promote. | Evals (5) + Production (8); pairs with GenAI Security |
| [Professional Tools](professional-tools-deep-dive/) | Volume 2. Rebuild each from-scratch piece with the tool professionals actually reach for (LiteLLM, Instructor, LlamaIndex, DeepEval, LangGraph, Llama Guard, Langfuse) and measure both on the same eval, so "should we adopt this framework?" becomes an experiment instead of a taste. | Everything (you need the pieces first) |

---

## Building this in TypeScript?

The series teaches in Python, because that is where the AI world's centre of gravity
still sits. But most software that will end up calling a language model is already
written, and a great deal of it is written in TypeScript.

> [TypeScript AI Deep Dive](typescript-ai-deep-dive/): the same ideas in TypeScript,
> and an honest account of what actually changes. Your types stop at the network
> boundary, so everything a model says is `unknown` until you check it at runtime.
> Every call is a promise. And one blocking handler stalls the whole process in a way
> you cannot detect from inside it. Thirteen runnable examples, twelve of which need
> no API key.

It is a companion rather than a step in the sequence. Nothing above depends on it, and
it replaces no dive. For depth on any subject it touches, the Python dive on that
subject goes much further. Read it if your AI work ships in TypeScript, or if you want
to know which of the differences are real and which are folklore.

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

 OpenAI API · Claude API ───────────────▶ ML Foundations ─▶ Local Models
                                                        └─▶ Inference Platforms
```

The thread runs: build the call (1–2), ask well (3), ground it (4), measure it (5),
let it act (6), harden it (7), operate it (8). The bonus dives branch off where they
are most useful. Observability extends Production from one request to six weeks of
them, and Architecture asks where all these parts belong once there is more than one
of everything. Testing & Delivery turns those quality, security, and operational
signals into promotion and rollback evidence you can reproduce.
ML Foundations takes the numeric path beneath the API call. It belongs before the
dives where you tune weights, compress them, or schedule their memory.

---

## Setup (the same everywhere)

Every repo is self-contained and sets up identically. Inside any one:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # when the repo has one; config only, no keys
python check_setup.py              # verifies your environment; makes no API call
```

Your API key does not go in `.env`. Store it in your OS keychain and inject it per
command with `secrun`, a one-time setup that takes about two minutes and is written up
in [SECRETS.md](docs/SECRETS.md). Then run any key-using script as
`secrun python examples/…`; offline examples need no wrapper. `.env` holds the
non-secret `PROVIDER` and `MODEL` config and nothing else.

`check_setup.py` is always your first stop. It checks your Python version, packages,
provider, and key, and tells you exactly what to fix. Run it as
`secrun python check_setup.py` so it can see your keychain-stored key.

You can learn a lot for free. The Production dive runs entirely on an offline mock and
never needs a key; the Local Models dive runs open weights on your own machine; and
most other repos open with offline sections that cost nothing (token math, chunking,
the eval anatomy, the injection attack catalog, the quantization calculator).

| To run for $0 | Use |
|---------------|-----|
| The whole ops stack, no key | [Production](ai-in-production-deep-dive/) (mock provider) |
| A complete document lifecycle, no key | [AI Data Engineering](ai-data-engineering-deep-dive/) (deterministic corpus and embeddings) |
| The complete AI security control plane, no key | [GenAI Security](genai-security-deep-dive/) (deterministic attacks and release gate) |
| A complete inference fleet control plane, no GPU | [Inference Platform Engineering](inference-platform-deep-dive/) (deterministic memory, scheduling, scaling, and rollout decisions) |
| A complete release-evidence pipeline, no services | [Testing & Delivery](testing-and-delivery-deep-dive/) (deterministic tests, gates, rollout, and rollback) |
| Model mechanics, no API key or GPU | [ML Foundations for AI Engineers](ml-foundations-for-ai-engineers/) (NumPy math and a tiny CPU transformer) |
| Six weeks of monitoring, no key | [Observability](observability-deep-dive/) (synthetic traffic) |
| Real models, no per-token bill | [Local Models](local-models-deep-dive/) (Ollama on your machine) |
| Offline sections | the first lesson in most repos (look for "offline, no key") |

---

## Reference docs

The series-level docs live in [docs/](docs/), grouped by what you need them for. The
full annotated index is [docs/README.md](docs/README.md).

Foundations, the shared vocabulary and the up-front decisions:
[HOW-LLMS-WORK.md](docs/HOW-LLMS-WORK.md) (what an LLM actually is) ·
[GLOSSARY.md](docs/GLOSSARY.md) (every term the series assumes) ·
[CHOOSING.md](docs/CHOOSING.md) (prompt, RAG, fine-tune, agent, and when to pick each) ·
[MODELS.md](docs/MODELS.md) (context windows, prices, which to default to).

Practice, how to run the lessons and what to build:
[SECRETS.md](docs/SECRETS.md) (where your API keys go, which is not `.env`) ·
[CAPSTONE.md](docs/CAPSTONE.md) (the whole-series build, one tag per dive) ·
[CAREERS.md](docs/CAREERS.md) (each dive as a résumé line and an interview answer) ·
[AUTHORING-LESSONS.md](docs/AUTHORING-LESSONS.md) (for anyone extending the series).

Operating responsibly, the concerns no single dive owns:
[SAFETY.md](docs/SAFETY.md) (injection, moderation, PII, hallucination) ·
[RESPONSIBILITY.md](docs/RESPONSIBILITY.md) (honest claims, bias, disclosure, and
whether this should be an LLM at all) ·
[GOVERNANCE.md](docs/GOVERNANCE.md) (who decides, on what record) ·
[INCIDENTS.md](docs/INCIDENTS.md) (what to do at 2am) ·
[AI-UX.md](docs/AI-UX.md) (the interface as part of the safety system) ·
[SECURITY.md](SECURITY.md) (what this code does on your machine, and how to check).

Four docs stay at the root, because each one mirrors a file every dive also has:
[TEXTBOOK.md](TEXTBOOK.md), the series read as one book ·
[LESSONS.md](LESSONS.md), what went wrong building it ·
[CHANGELOG.md](CHANGELOG.md), what changed and when · and this README.

---

## A note on cost and safety

Most lessons cost a fraction of a cent, and the ones that make no API call are marked
**(offline)**. The token-counting and cost sections teach you to estimate spend before
you send. See [MODELS.md](docs/MODELS.md).

The [Prompt Injection & Guardrails](prompt-injection-deep-dive/) and
[GenAI Security](genai-security-deep-dive/) dives are strictly defensive. Every attack
targets a deterministic toy system and uses made-up secrets that protect nothing. Use
them to harden systems you own or are authorized to test.
