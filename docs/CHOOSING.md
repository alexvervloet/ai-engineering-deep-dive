# Choosing your approach

The single most useful skill in AI engineering is reaching for the simplest thing that
works, then knowing when to climb to the next rung. This guide maps the ladder. Part of
the [AI Engineering Deep Dives](../README.md).

> The rule repeated throughout the series: **start at the bottom and only climb when a
> measurement says you need to.** Every rung up costs more money, more latency, and
> more complexity. Most problems get solved lower than people reach for.

---

## The ladder

```
                                                  more power
                                                  more cost/complexity
   ┌──────────────────────────────────────────────┐   ▲
   │ 6. Agent          model drives a tool loop     │   │
   ├──────────────────────────────────────────────┤   │
   │ 5. Fine-tune      change default behavior      │   │
   ├──────────────────────────────────────────────┤   │
   │ 4. RAG            put your facts in context    │   │
   ├──────────────────────────────────────────────┤   │
   │ 3. Tools          let it act / fetch live data │   │
   ├──────────────────────────────────────────────┤   │
   │ 2. Few-shot       show 2–5 examples            │   │
   ├──────────────────────────────────────────────┤   │
   │ 1. Better prompt  clearer instructions         │   ▼
   └──────────────────────────────────────────────┘  start here
```

Climb only when the rung below genuinely cannot do the job, and prove that with an
[eval](../evals-deep-dive/) rather than a vibe.

---

## What each rung changes

The rungs are not interchangeable. Each one changes a different thing, and that is the
distinction worth internalizing.

| Approach | Changes… | Reach for it when… |
|----------|----------|--------------------|
| **Prompt / few-shot** | how you *ask* | the model can do the task but needs clearer instruction or format |
| **Tools** | what the model *can do* | it needs to act, calculate, or fetch live/private data |
| **RAG / long context** | what's *in the context* (knowledge) | it needs facts that change, are private, or must be cited |
| **Fine-tuning** | how it *behaves by default* | you need the same format/tone/skill every time, or a cheaper model |
| **Agent** | how steps are *chosen* | the path to the answer can't be known up front |

> **Knowledge, behavior, capability.** RAG changes what it knows. Fine-tuning changes
> how it behaves. Tools change what it can do. Pick the lever that matches your actual
> problem. Most "we need to fine-tune" instincts turn out to be a knowledge problem,
> which is RAG, or a phrasing problem, which is a better prompt.

---

## A decision walkthrough

Answer these in order and stop at the first yes.

**1. Is the output just poorly phrased, formatted, or inconsistent?**
→ Fix the **prompt**. Be specific, assign a role, show the exact output format, and say
how to handle missing information. → [Prompt Engineering](../prompt-engineering-deep-dive/)

**2. Does it get the shape wrong, or fumble a few edge cases?**
→ Add two to five **few-shot examples** that demonstrate the format and the tricky
cases. → [Prompt Engineering](../prompt-engineering-deep-dive/) (few-shot, classification)

**3. Does it need to do something, like math, an API call, or a database query?**
→ Give it **tools**. You describe functions, the model asks to call them, and you run
them. → [Agents](../agents-deep-dive/) (tools), the API dives
([OpenAI](../openai-api-deep-dive/), [Claude](../claude-api-deep-dive/)) (function calling)

**4. Does it need facts it doesn't have, like your docs, recent data, or private knowledge?**
→ **RAG.** Retrieve the right text and put it in the context, with citations. Don't
bake changing facts into a model. → [RAG](../rag-deep-dive/)

**5. Does it need to behave a fixed way every time (format, tone, one narrow skill), or
do you want a cheaper and faster model on a high-volume task?**
→ **Fine-tune**, but only once a prompt and RAG have fallen short, and only if you can
measure that it beat your baseline. → [Fine-tuning](../fine-tuning-deep-dive/)
>
> Check where you can still do this before you plan around it. OpenAI is winding down
> self-serve fine-tuning through 2026 and into January 2027, and Anthropic never
> offered it self-serve at all. In practice this rung now means an open-weight model
> you tune yourself with LoRA or PEFT, locally or on rented GPUs, which raises the bar
> for choosing it over a better prompt.

**6. Is the task open-ended and multi-step, with no path you can script?**
→ Build an **agent**, a model-driven loop. If you can draw the flowchart, build a
**workflow** instead, which is cheaper and predictable.
→ [Agents](../agents-deep-dive/) (workflows vs. agents)

> **"But everyone uses agents."** Usually that means everyone uses an agent someone
> else built and hardened, like Cursor, Claude Code, or a framework's prebuilt loop.
> The complexity that puts this rung last gets paid once by the tool's author and then
> hidden, so the hardest rung feels like the cheapest. Building an agent into your own
> product is the decision this ladder is about, and there it is rarely the cheapest
> thing that works. Prove the lower rungs fail first.

---

## Branches for specific needs

These are not higher rungs. They are side doors for particular requirements.

| You need… | Go to |
|-----------|-------|
| To build *on* an agent loop (hooks, permission policies, sandboxing, subagents, headless runs) | [Agent Harnesses](../agent-harness-deep-dive/) |
| A long conversation (or agent) to remember without blowing the context window | [Context Engineering](../context-engineering-deep-dive/) |
| Images or audio in/out (batch) | [Multimodal](../multimodal-deep-dive/) |
| Real-time, spoken conversation (low latency, interruption) | [Realtime Voice](../realtime-voice-deep-dive/) |
| To understand tensor shapes, loss, gradients, attention, sampling, calibration, quantization, or model memory | [ML Foundations for AI Engineers](../ml-foundations-for-ai-engineers/) |
| Privacy, offline, or zero per-token cost | [Local Models](../local-models-deep-dive/) |
| To serve open weights as a fleet, with KV memory, batching, parallelism, admission, GPU placement, scaling, rollouts, and capacity | [Inference Platform Engineering](../inference-platform-deep-dive/) |
| To share tools/data with an LLM across apps | [MCP](../mcp-deep-dive/) |
| To own the corpus behind the index, with versions, lineage, ACLs, and deletes | [AI Data Engineering](../ai-data-engineering-deep-dive/) |
| To know if any change actually helped | [Evals](../evals-deep-dive/), the skill every rung needs |
| To stop it being jailbroken or leaking | [Prompt Injection & Guardrails](../prompt-injection-deep-dive/) |
| To secure the system around the model, meaning identity, supply chain, tenant isolation, egress, budgets, and release gates | [GenAI Security](../genai-security-deep-dive/) |
| To run any of it for real users | [Production](../ai-in-production-deep-dive/) |
| To know it is still working weeks later, watching drift, silent regressions, and alerting | [Observability](../observability-deep-dive/) |
| To decide whether a framework beats what you hand-rolled, measured rather than assumed | [Professional Tools](../professional-tools-deep-dive/) |
| To decide where the pieces go, across state, queues, tiers, and tenant boundaries | [Architecture](../architecture-deep-dive/) |
| To decide whether a specific build qualifies for promotion, on contract, compatibility, supply-chain, rollout, and rollback evidence | [Testing & Delivery](../testing-and-delivery-deep-dive/) |
| To write down who decided, on what evidence, and what would reverse it | [GOVERNANCE.md](GOVERNANCE.md) |
| To have a runbook ready before the 2am page | [INCIDENTS.md](INCIDENTS.md) |
| To make a wrong answer visible, contestable, and undoable | [AI-UX.md](AI-UX.md) |

---

## Three rules that apply at every rung

1. **Measure, don't guess.** "It seems better" ships regressions. Put a number on
   quality and rerun it. → [Evals](../evals-deep-dive/)
2. **Start cheap.** Use the small model (`gpt-5.4-nano` or `claude-haiku-4-5`) and the
   simplest technique. Climb only when an eval forces you to. → [MODELS.md](MODELS.md)
3. **They combine.** Real systems stack rungs. A fine-tuned model for behavior, RAG for
   facts, inside an agent, behind guardrails, measured by evals, operated with the
   production stack. The ladder tells you what to try first, not what to use only.
