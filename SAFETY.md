# Safety: the cross-cutting view

Safety in an LLM app isn't one feature; it's a set of distinct concerns that the
series teaches *in context*, in the dives where they bite. This page is the map:
what the concerns are, which dive covers each hands-on, and the few principles that
tie them together. Part of the [AI Engineering Deep Dives](README.md).

> **Scope.** This is about building systems that are safe *to operate*: they don't
> leak, get hijacked, spew harmful content, or quietly mislead. The
> [Prompt Injection & Guardrails](prompt-injection-deep-dive/) and
> [GenAI Security](genai-security-deep-dive/) dives are strictly defensive (every
> attack targets its own toy system); use these techniques only on systems you own or
> are authorized to test. For the *other* half (honest claims,
> bias & fairness, disclosure, consent, what the training data is built on, the
> effect on the person on the other side, and human accountability) see its sibling
> [RESPONSIBILITY.md](RESPONSIBILITY.md).

---

## The concerns, and where they're covered

| Concern | What it is | Hands-on in |
|---------|-----------|-------------|
| **Prompt injection** | Untrusted text (a user message, a retrieved doc, a tool result) overrides your instructions | [Prompt Injection & Guardrails](prompt-injection-deep-dive/) |
| **Jailbreaks** | Coaxing the model past its own safety training | [Prompt Injection & Guardrails](prompt-injection-deep-dive/) |
| **Harmful content (moderation)** | Hate, violence, sexual, self-harm, in *or* out | [Prompt Injection](prompt-injection-deep-dive/) (content moderation), [OpenAI API](openai-api-deep-dive/) (free moderation endpoint) |
| **Data exfiltration** | Leaking data through a side channel (e.g. a markdown image URL the client auto-loads) | [Prompt Injection](prompt-injection-deep-dive/) |
| **PII / data privacy** | Personal data sent upstream, returned to the wrong user, or sitting in logs | [Prompt Injection](prompt-injection-deep-dive/) + [Production](ai-in-production-deep-dive/) (the three touchpoints) |
| **Hallucination** | Confident, fluent claims that aren't true or aren't supported | [RAG](rag-deep-dive/) (grounding), [Evals](evals-deep-dive/) (faithfulness), [HOW-LLMS-WORK.md](HOW-LLMS-WORK.md) (why) |
| **Unsafe actions** | An agent taking a destructive or costly action on its own | [Agents](agents-deep-dive/) (approval, step limits), [Prompt Injection](prompt-injection-deep-dive/) (capability limits) |
| **Untrusted tools/servers** | An MCP server's tool descriptions and results flowing into your model | [MCP](mcp-deep-dive/) (security section) |
| **Silent quality regressions** | A prompt/model change that quietly makes things worse | [Evals](evals-deep-dive/) (eval gates), [Production](ai-in-production-deep-dive/) |
| **Excessive agency** | A tool call carrying authority the *user* never had: the model chose the tenant, the role, or the object | [GenAI Security](genai-security-deep-dive/) (capability broker, bound approval) |
| **Supply chain** | A model, adapter, prompt, or dataset that changed behavior without changing your code | [GenAI Security](genai-security-deep-dive/) (digests, signatures, approved sources) |
| **Data & model poisoning** | Bad records reaching a corpus or training set whose outer artifact verifies perfectly | [GenAI Security](genai-security-deep-dive/) (record and population gates), [AI Data Engineering](ai-data-engineering-deep-dive/) (lineage) |
| **Cross-tenant retrieval** | One tenant's chunk ranking into another tenant's answer, cache, or trace | [GenAI Security](genai-security-deep-dive/) (prefilter before ranking), [AI Data Engineering](ai-data-engineering-deep-dive/) (ACLs travel with the chunk) |
| **SSRF & egress** | A model-chosen URL reaching cloud metadata, loopback, or a private control plane | [GenAI Security](genai-security-deep-dive/) (resolved-address policy) |
| **Generated-code execution** | Running what the model wrote, in a process that can reach your filesystem and credentials | [GenAI Security](genai-security-deep-dive/) (runner contract), [Agent Harnesses](agent-harness-deep-dive/) (sandboxing) |
| **Denial of wallet** | One accepted request that recurses, fans out, and spends the budget | [GenAI Security](genai-security-deep-dive/) (pre-call reservations), [Production](ai-in-production-deep-dive/) (per-request budgets) |
| **Incident response** | What you actually do at 3am, and whether recovery is tested or hoped for | [GenAI Security](genai-security-deep-dive/) (lifecycle, evidence, tested recovery) |

---

## Four principles that cut across all of them

**1. Treat everything the model reads and writes as untrusted.**
The model can't reliably tell your instructions from an attacker's; to it, it's all
just text. So untrusted *input* (user text, retrieved docs, tool results, another
server's output) can carry instructions, and untrusted *output* can carry a leak or a
harmful response. Check both sides. This is the spine of the
[Prompt Injection](prompt-injection-deep-dive/) dive.

**2. Contain the blast radius: don't rely on the model behaving.**
You can't make a model un-trickable, so make being tricked *survivable*. The defense
that doesn't depend on the model guessing right is limiting what it can *cause*:
least-privilege tools, allow-listed actions, human approval for anything
side-effecting, and the dual-LLM pattern (quarantine untrusted text from the model
that holds authority). Capability limits beat detection.

**3. Defense in depth: every single layer is "necessary, not sufficient."**
A delimiter, an input filter, an output check, a moderation pass, capability limits:
each one leaks. Stack them. The [Production](ai-in-production-deep-dive/) dive is where
they stop being separate demos and sit on one request path together: input guard →
model → output guard, each decision traced.

**4. Measure safety like any other quality: as a number you can rerun.**
"It seems safer" ships regressions. Turn your attack catalog into an **eval** whose
metric is *attack-success-rate*, gate it in CI, and watch it over time
([Evals](evals-deep-dive/) + the red-team eval in
[Prompt Injection](prompt-injection-deep-dive/)). Same for hallucination: a
faithfulness eval makes "did it stay grounded?" a tracked number, not a vibe.

Watch benign traffic in the same gate. A system that blocks everything scores a perfect
attack-success rate, and a suite that can't fail its own coverage check isn't measuring
anything either ([GenAI Security](genai-security-deep-dive/), lesson 11).

**5. The model is a principal, not a boundary.**
The first four all live around the model. This one says where the line actually is:
the model may *propose* an action, but nothing it says grants authority. Identity,
policy, provenance, isolation, and budgets are enforced in ordinary code that a
compromised model cannot argue with. It's the difference between asking a system to
behave and building one where misbehaving doesn't help.
([GenAI Security](genai-security-deep-dive/) is the whole dive on this.)

---

## Two things people conflate (and shouldn't)

- **Injection defense ≠ moderation.** Injection defense stops the model being
  *hijacked*; moderation stops *harmful content* coming in or going out. They're
  independent layers; run both. (A perfectly un-jailbroken bot can still be asked to
  write something hateful.)
- **Hallucination ≠ a safety bug you can patch.** It's inherent to how the model works
  ([HOW-LLMS-WORK.md](HOW-LLMS-WORK.md)). You don't fix it; you *manage* it: ground
  answers in retrieved facts, cite sources, and measure faithfulness.
- **Injection defense ≠ securing the system.** Injection is one attack, on one
  surface: the text the model reads. A production system also has identities, tools,
  build artifacts, retrieval indexes, interpreters, networks, and budgets, and every
  one of them can fail without a single crafted prompt. Do
  [Prompt Injection](prompt-injection-deep-dive/) for the attack;
  [GenAI Security](genai-security-deep-dive/) for the rest of the system that has to
  hold when the model is wrong, tricked, or replaced.

---

## The PII three-touchpoint checklist

Personal data is the concern most likely to slip through, because it has three
separate touchpoints; miss any one and you've leaked:

1. **In**: decide what you may send *upstream* to the provider at all (and under
   what retention). Reuse the input-inspection pattern from injection defense.
2. **Out**: redact PII on the way back to the user (output guard), but allow your
   own published addresses through.
3. **Logs**: scrub structured fields before they hit your log store, which usually
   has looser access and longer retention than your database.

All three are built and wired together in the
[Production](ai-in-production-deep-dive/) dive.

---

## Where to start

- Building anything user-facing → do the [Prompt Injection & Guardrails](prompt-injection-deep-dive/)
  dive; it's the one that changes how you think.
- Putting it in front of real users → [Production](ai-in-production-deep-dive/) puts the
  guards on a live request path.
- Worried about wrong answers, not attacks → [RAG](rag-deep-dive/) grounding +
  [Evals](evals-deep-dive/) faithfulness.
- Giving the model tools → [Agents](agents-deep-dive/) approval + capability limits.
- Multi-tenant, handling regulated data, or shipping agents that act →
  [GenAI Security](genai-security-deep-dive/): the whole control plane, offline, ending
  in a release gate that fails the naive build and passes the hardened one.
