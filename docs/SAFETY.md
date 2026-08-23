# Safety: the cross-cutting view

Safety in an LLM app is several distinct concerns rather than one feature, and the
series teaches each one in the dive where it bites. This page is the map. What the
concerns are, which dive covers each one hands-on, and the handful of principles that
tie them together. Part of the [AI Engineering Deep Dives](../README.md).

> **Scope.** This page is about building systems that are safe to operate, meaning
> they do not leak, get hijacked, produce harmful content, or mislead without anyone
> noticing. The [Prompt Injection & Guardrails](../prompt-injection-deep-dive/) and
> [GenAI Security](../genai-security-deep-dive/) dives are strictly defensive, and
> every attack in them targets its own toy system. Use these techniques only on
> systems you own or are authorized to test. The other half of the subject lives in
> [RESPONSIBILITY.md](RESPONSIBILITY.md): honest claims, bias and fairness,
> disclosure, consent, what the training data is built on, the effect on the person
> on the other side, and human accountability. Three more pages sit on top of both.
> [GOVERNANCE.md](GOVERNANCE.md) holds the decision record and assessment templates,
> [INCIDENTS.md](INCIDENTS.md) covers what to do when a control fails, and
> [AI-UX.md](AI-UX.md) covers the interface that makes a wrong answer visible.

---

## The concerns, and where they're covered

| Concern | What it is | Hands-on in |
|---------|-----------|-------------|
| **Prompt injection** | Untrusted text (a user message, a retrieved doc, a tool result) overrides your instructions | [Prompt Injection & Guardrails](../prompt-injection-deep-dive/) |
| **Jailbreaks** | Coaxing the model past its own safety training | [Prompt Injection & Guardrails](../prompt-injection-deep-dive/) |
| **Harmful content (moderation)** | Hate, violence, sexual, self-harm, in *or* out | [Prompt Injection](../prompt-injection-deep-dive/) (content moderation), [OpenAI API](../openai-api-deep-dive/) (free moderation endpoint) |
| **Data exfiltration** | Leaking data through a side channel (e.g. a markdown image URL the client auto-loads) | [Prompt Injection](../prompt-injection-deep-dive/) |
| **PII / data privacy** | Personal data sent upstream, returned to the wrong user, or sitting in logs | [Prompt Injection](../prompt-injection-deep-dive/) + [Production](../ai-in-production-deep-dive/) (the three touchpoints) |
| **Hallucination** | Confident, fluent claims that aren't true or aren't supported | [RAG](../rag-deep-dive/) (grounding), [Evals](../evals-deep-dive/) (faithfulness), [HOW-LLMS-WORK.md](HOW-LLMS-WORK.md) (why) |
| **Unsafe actions** | An agent taking a destructive or costly action on its own | [Agents](../agents-deep-dive/) (approval, step limits), [Prompt Injection](../prompt-injection-deep-dive/) (capability limits) |
| **Untrusted tools/servers** | An MCP server's tool descriptions and results flowing into your model | [MCP](../mcp-deep-dive/) (security section) |
| **Silent quality regressions** | A prompt or model change that makes things worse without tripping anything | [Evals](../evals-deep-dive/) (eval gates), [Production](../ai-in-production-deep-dive/) |
| **Excessive agency** | A tool call carrying authority the user never had, because the model chose the tenant, the role, or the object | [GenAI Security](../genai-security-deep-dive/) (capability broker, bound approval) |
| **Supply chain** | A model, adapter, prompt, or dataset that changed behavior without changing your code | [GenAI Security](../genai-security-deep-dive/) (digests, signatures, approved sources) |
| **Data & model poisoning** | Bad records reaching a corpus or training set whose outer artifact verifies perfectly | [GenAI Security](../genai-security-deep-dive/) (record and population gates), [AI Data Engineering](../ai-data-engineering-deep-dive/) (lineage) |
| **Cross-tenant retrieval** | One tenant's chunk ranking into another tenant's answer, cache, or trace | [GenAI Security](../genai-security-deep-dive/) (prefilter before ranking), [AI Data Engineering](../ai-data-engineering-deep-dive/) (ACLs travel with the chunk) |
| **SSRF & egress** | A model-chosen URL reaching cloud metadata, loopback, or a private control plane | [GenAI Security](../genai-security-deep-dive/) (resolved-address policy) |
| **Generated-code execution** | Running what the model wrote, in a process that can reach your filesystem and credentials | [GenAI Security](../genai-security-deep-dive/) (runner contract), [Agent Harnesses](../agent-harness-deep-dive/) (sandboxing) |
| **Denial of wallet** | One accepted request that recurses, fans out, and spends the budget | [GenAI Security](../genai-security-deep-dive/) (pre-call reservations), [Production](../ai-in-production-deep-dive/) (per-request budgets) |
| **Incident response** | What you actually do when it breaks, and whether recovery is tested or hoped for | [GenAI Security](../genai-security-deep-dive/) (lifecycle, evidence, tested recovery) |

---

## Five principles that cut across all of them

**1. Everything the model reads and writes is untrusted.**
The model cannot reliably tell your instructions from an attacker's. To it, all of it
is just text. Untrusted input (user text, retrieved docs, tool results, another
server's output) can carry instructions, and untrusted output can carry a leak or a
harmful response. Check both sides. This is the spine of the
[Prompt Injection](../prompt-injection-deep-dive/) dive.

**2. Contain the blast radius rather than trusting the model to behave.**
You cannot make a model un-trickable, so make being tricked survivable. The defense
that does not depend on the model guessing right is limiting what it can cause:
least-privilege tools, allow-listed actions, human approval for anything with a side
effect, and the dual-LLM pattern that quarantines untrusted text from the model that
holds authority. Capability limits beat detection.

**3. Defense in depth, because every single layer is necessary and none is sufficient.**
A delimiter, an input filter, an output check, a moderation pass, capability limits.
Each one leaks. Stack them. The [Production](../ai-in-production-deep-dive/) dive is
where they stop being separate demos and sit on one request path together: input guard,
model, output guard, with every decision traced.

**4. Measure safety like any other quality, as a number you can rerun.**
"It seems safer" ships regressions. Turn your attack catalog into an **eval** whose
metric is attack-success-rate, gate it in CI, and watch it over time. See
[Evals](../evals-deep-dive/) and the red-team eval in
[Prompt Injection](../prompt-injection-deep-dive/). Hallucination works the same way. A
faithfulness eval makes "did it stay grounded?" a tracked number instead of a vibe.

Watch benign traffic in the same gate. A system that blocks everything scores a perfect
attack-success rate, and a suite that cannot fail its own coverage check is not
measuring anything either ([GenAI Security](../genai-security-deep-dive/), lesson 11).

**5. The model is a principal, not a boundary.**
The first four all live around the model. This one says where the line actually falls.
The model may propose an action, but nothing it says grants authority. Identity,
policy, provenance, isolation, and budgets get enforced in ordinary code that a
compromised model cannot argue with. That is the difference between asking a system to
behave and building one where misbehaving does not help.
([GenAI Security](../genai-security-deep-dive/) is the whole dive on this.)

---

## Three things people conflate, and shouldn't

- **Injection defense is not moderation.** Injection defense stops the model being
  hijacked. Moderation stops harmful content coming in or going out. They are
  independent layers, so run both. A bot nobody has jailbroken can still be asked to
  write something hateful.
- **Hallucination is not a safety bug you can patch.** It is inherent to how the model
  works, as [HOW-LLMS-WORK.md](HOW-LLMS-WORK.md) explains. You do not fix it. You
  manage it: ground answers in retrieved facts, cite sources, and measure faithfulness.
- **Injection defense is not securing the system.** Injection is one attack in one
  place, the text the model reads. A production system also has identities, tools,
  build artifacts, retrieval indexes, interpreters, networks, and budgets, and every
  one of them can fail without a single crafted prompt. Do
  [Prompt Injection](../prompt-injection-deep-dive/) for the attack. Do
  [GenAI Security](../genai-security-deep-dive/) for the rest of the system, which has
  to hold when the model is wrong, tricked, or replaced.

---

## The PII three-touchpoint checklist

Personal data is the concern most likely to slip through, because it has three
separate touchpoints and missing any one of them is a leak.

1. **In.** Decide what you may send upstream to the provider at all, and under what
   retention. Reuse the input-inspection pattern from injection defense.
2. **Out.** Redact PII on the way back to the user with an output guard, while letting
   your own published addresses through.
3. **Logs.** Scrub structured fields before they hit your log store, which usually has
   looser access and longer retention than your database.

All three are built and wired together in the
[Production](../ai-in-production-deep-dive/) dive.

---

## Where to start

- Building anything user-facing → do the
  [Prompt Injection & Guardrails](../prompt-injection-deep-dive/) dive. It is the one
  that changes how you think.
- Putting it in front of real users → [Production](../ai-in-production-deep-dive/) puts
  the guards on a live request path.
- Worried about wrong answers rather than attacks → [RAG](../rag-deep-dive/) grounding
  and [Evals](../evals-deep-dive/) faithfulness.
- Giving the model tools → [Agents](../agents-deep-dive/) approval and capability limits.
- Multi-tenant, handling regulated data, or shipping agents that act →
  [GenAI Security](../genai-security-deep-dive/), the whole control plane, offline,
  ending in a release gate that fails the naive build and passes the hardened one.
