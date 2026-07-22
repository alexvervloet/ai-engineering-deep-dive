# Choosing your approach

The single most useful skill in AI engineering is **reaching for the simplest thing
that works**, and knowing when to climb to the next rung. This guide maps the
ladder. Part of the [AI Engineering Deep Dives](README.md).

> The golden rule, repeated throughout the series: **start at the bottom and only
> climb when a measurement says you need to.** Each rung up costs more money, more
> latency, more complexity. Most problems are solved lower than people reach for.

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

Climb only when the rung below genuinely can't do the job, and prove it with an
[eval](evals-deep-dive/), not a vibe.

---

## What each rung changes

The rungs aren't interchangeable; they change *different* things. This is the key
distinction to internalize:

| Approach | Changes… | Reach for it when… |
|----------|----------|--------------------|
| **Prompt / few-shot** | how you *ask* | the model can do the task but needs clearer instruction or format |
| **Tools** | what the model *can do* | it needs to act, calculate, or fetch live/private data |
| **RAG / long context** | what's *in the context* (knowledge) | it needs facts that change, are private, or must be cited |
| **Fine-tuning** | how it *behaves by default* | you need the same format/tone/skill every time, or a cheaper model |
| **Agent** | how steps are *chosen* | the path to the answer can't be known up front |

> **Knowledge vs. behavior vs. capability.** RAG changes *what it knows*.
> Fine-tuning changes *how it behaves*. Tools change *what it can do*. Pick the lever
> that matches your actual problem; most "we need to fine-tune" instincts are really
> a knowledge problem (RAG) or a phrasing problem (a better prompt).

---

## A decision walkthrough

Answer these in order; stop at the first "yes."

**1. Is the output just poorly phrased, formatted, or inconsistent?**
→ Fix the **prompt**. Be specific, assign a role, show the exact output format, state
how to handle missing info. → [Prompt Engineering](prompt-engineering-deep-dive/)

**2. Does it get the *shape* wrong, or fumble a few edge cases?**
→ Add **few-shot examples** (2–5) that demonstrate the format and the tricky cases.
→ [Prompt Engineering](prompt-engineering-deep-dive/) (few-shot, classification)

**3. Does it need to *do* something: math, an API call, a database query?**
→ Give it **tools**. You describe functions; the model asks to call them; you run
them. → [Agents](agents-deep-dive/) (tools), the API dives
([OpenAI](openai-api-deep-dive/), [Claude](claude-api-deep-dive/)) (function calling)

**4. Does it need facts it doesn't have: your docs, recent data, private knowledge?**
→ **RAG.** Retrieve the right text and put it in the context, with citations. Don't
bake changing facts into a model. → [RAG](rag-deep-dive/)

**5. Does it need to behave a *fixed* way every time (format/tone/narrow skill), or do
you want a cheaper/faster model on a high-volume task?**
-> **Fine-tune**, but only after a prompt and RAG fall short, and only if you can
*measure* that it beat your baseline. → [Fine-tuning](fine-tuning-deep-dive/)

**6. Is the task open-ended and multi-step, where you can't script the path?**
→ Build an **agent** (model-driven loop). If you *can* draw the flowchart, build a
**workflow** instead (cheaper, predictable). → [Agents](agents-deep-dive/) (workflows vs. agents)

> **"But everyone uses agents."** Usually that means everyone *uses* an agent
> someone else built and hardened (Cursor, Claude Code, a framework's prebuilt loop).
> The complexity that puts this rung last is paid once by the tool's author, then
> hidden, so the hardest rung *feels* like the cheapest. Building an agent into
> *your own* product is the decision this ladder is about, and there it's rarely the
> cheapest thing that works. Prove the lower rungs fail first.

---

## Branches for specific needs

These aren't higher rungs; they're side doors for particular requirements.

| You need… | Go to |
|-----------|-------|
| To build *on* an agent loop (hooks, permission policies, sandboxing, subagents, headless runs) | [**Agent Harnesses**](agent-harness-deep-dive/) |
| A long conversation (or agent) to remember without blowing the context window | [**Context Engineering**](context-engineering-deep-dive/) |
| Images or audio in/out (batch) | [**Multimodal**](multimodal-deep-dive/) |
| Real-time, spoken conversation (low latency, interruption) | [**Realtime Voice**](realtime-voice-deep-dive/) |
| Privacy, offline, or zero per-token cost | [**Local Models**](local-models-deep-dive/) |
| To share tools/data with an LLM across apps | [**MCP**](mcp-deep-dive/) |
| To know if any change actually helped | [**Evals**](evals-deep-dive/), the meta-skill for *every* rung |
| To stop it being jailbroken or leaking | [**Prompt Injection & Guardrails**](prompt-injection-deep-dive/) |
| To run any of it for real users | [**Production**](ai-in-production-deep-dive/) |
| To know it's *still* working weeks later: drift, silent regressions, alerting | [**Observability**](observability-deep-dive/) |
| To decide whether a framework beats what you hand-rolled: measured, not assumed | [**Professional Tools**](professional-tools-deep-dive/) |

---

## Three rules that apply at every rung

1. **Measure, don't guess.** "It seems better" ships regressions. Put a number on
   quality and rerun it. → [Evals](evals-deep-dive/)
2. **Start cheap.** Use the small model (`gpt-4o-mini` / `claude-haiku-4-5`) and the
   simplest technique; climb only when an eval forces you to. → [MODELS.md](MODELS.md)
3. **They combine.** Real systems stack rungs: a fine-tuned model *for behavior* +
   RAG *for facts*, inside an agent, behind guardrails, measured by evals, operated
   with the production stack. The ladder tells you what to *try first*, not what to
   use *only*.
