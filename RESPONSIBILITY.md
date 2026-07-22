# Responsibility: the cross-cutting view

[SAFETY.md](SAFETY.md) is about building a system that's safe *to operate*: one that
doesn't leak, get hijacked, or spew harmful content. This page is the other half:
whether you *should* build the thing, whether you're being honest about what it does,
and who's accountable when it's wrong. Those aren't features you can `pip install`.
they're decisions you make *around* the code. This is the map. Part of the
[AI Engineering Deep Dives](README.md).

> **Scope.** The rest of the series is hands-on: every concept is a script you run.
> This page is deliberately not: it's the judgment that the runnable parts can't
> encode. But it stays concrete: every concern below points to the dive whose tools
> *operationalize* it, because the responsible move is almost always to turn a worry
> into a **measurement** or a **limit**, not a good intention.

---

## The concerns, and where the tools live

| Concern | What it is | Operationalized in |
|---------|-----------|--------------------|
| **Honest capability claims** | Not selling "it understands" / "it's accurate" when it's a fluent next-token predictor that's right *most* of the time | [HOW-LLMS-WORK.md](HOW-LLMS-WORK.md), [Evals](evals-deep-dive/) (put a number on "how often right") |
| **Hallucination & grounding** | Confident claims that aren't true or aren't supported, and whether users can tell | [RAG](rag-deep-dive/) (cite sources), [Evals](evals-deep-dive/) (faithfulness) |
| **Bias & fairness** | The model treats groups differently, or your eval set only represents some users | [Evals](evals-deep-dive/) (slice your dataset; measure per-group) |
| **Disclosure** | Users have a right to know they're talking to an AI, and which answers are machine-generated | a product decision; nothing hidden in a system prompt should contradict it |
| **Data consent & governance** | What you may send upstream, retain, log, or train on, and whether the person whose data it is agreed | [Production](ai-in-production-deep-dive/) (PII touchpoints, retention), [SAFETY.md](SAFETY.md) |
| **Human oversight & contestability** | A person can review, override, and a user can appeal a consequential output | [Agents](agents-deep-dive/) (human-in-the-loop), [Production](ai-in-production-deep-dive/) (feedback) |
| **Accountability** | When it's wrong, a named human owns the outcome, not "the AI did it" | a process you define before launch, not after the incident |
| **Cost of being wrong** | Whether a mistake is a typo or a denied loan / wrong dosage; sets every bar above | informs your eval bar and whether to ship at all |

---

## Four principles that cut across all of them

**1. Match the stakes to the safeguards.** A draft-email helper and a system that
screens job applicants are not the same risk, even if the API call is identical. The
higher the cost of a wrong answer to the person on the receiving end, the higher the
eval bar, the more human oversight, and the more you should ask whether an LLM belongs
here *at all*. Calibrate the safeguards to the blast radius on a **human**, not on your
uptime.

**2. Honesty about limits is part of the product.** The model is right most of the
time and wrong fluently, with the same confident tone either way (see
[HOW-LLMS-WORK.md](HOW-LLMS-WORK.md)). Responsible design assumes the user can't tell
the two apart, so it shows its work: cite sources, surface uncertainty, say "I don't
know," and never let marketing copy promise an accuracy your [evals](evals-deep-dive/)
don't back.

**3. Measure fairness like any other quality: per group, not just on average.** An
aggregate pass rate can hide that a system works for one group and fails another. The
fix is the same discipline as the rest of the series: **slice the eval set** and report
the metric for each slice. You can't manage a number you never split.
→ [Evals](evals-deep-dive/)

**4. Keep a human accountable: naming the model is not an answer.** "The AI decided"
is not a thing a person harmed by a decision can appeal to. For any consequential
output, define *before* launch who reviews it, who can override it, and how a user
contests it. [Human-in-the-loop](agents-deep-dive/) and a
[feedback path](ai-in-production-deep-dive/) are the mechanics; the accountability is
the part you own.

---

## The question upstream of all the others: should this be an LLM?

The whole [CHOOSING.md](CHOOSING.md) ladder starts at "reach for the simplest thing
that works." Responsibility adds a rung *below* the bottom of that ladder: **maybe the
simplest thing is not an LLM, or not a feature at all.** Reach for a rule, a lookup,
or a human when:

- the cost of a confident wrong answer is paid by a person who didn't opt in (medical,
  legal, financial, hiring, housing, anything high-stakes), and you can't get the eval
  bar high enough to justify it;
- the task has a correct answer a deterministic system already nails; don't add
  hallucination risk to a solved problem;
- you couldn't explain or defend a given output if the person it affected asked you to.

"We *could* use a model here" is not "we *should*." Answering this honestly is itself
an engineering skill.

---

## A pre-launch checklist

Before a system reaches real users, you can answer these, and they're concrete:

1. **Claims**: does every public claim about accuracy match an [eval](evals-deep-dive/)
   number you can rerun? *(No → soften the copy or raise the bar.)*
2. **Disclosure**: does the user know they're interacting with AI, and which content
   is generated?
3. **Grounding**: for factual answers, are sources cited and
   [faithfulness](evals-deep-dive/) measured? *(→ [RAG](rag-deep-dive/))*
4. **Fairness**: have you sliced the eval set by the groups your app actually serves
   and checked the metric per slice?
5. **Data**: do you have consent for what you send upstream, and a defined retention
   policy for logs? *(→ [Production](ai-in-production-deep-dive/), [SAFETY.md](SAFETY.md))*
6. **Oversight**: for consequential outputs, who reviews, who overrides, how does a
   user contest? *(→ [Agents](agents-deep-dive/) human-in-the-loop)*
7. **Owner**: is there a named human accountable for outcomes?

None of these is a library call. All of them are answerable, and a "no" on a
high-stakes system is a reason to slow down.

---

## Where to start

- Shipping anything that affects a person's opportunities or wellbeing → start with the
  checklist above, then raise the [eval](evals-deep-dive/) bar to match the stakes.
- Worried about wrong or unsupported answers → [RAG](rag-deep-dive/) grounding +
  [Evals](evals-deep-dive/) faithfulness make honesty measurable.
- This page's sibling on *operational* safety (injection, leaks, moderation) →
  [SAFETY.md](SAFETY.md).
