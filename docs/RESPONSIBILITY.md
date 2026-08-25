# Responsibility: the cross-cutting view

[SAFETY.md](SAFETY.md) is about building a system that is safe to operate, one that
does not leak, get hijacked, or produce harmful content. This page is the other half.
Whether you should build the thing at all, whether you are being honest about what it
does, what it is built on, who it affects, and who is accountable when it is wrong. None
of those are features you can `pip install`. They are decisions you make around the
code. This is the map. Part of the [AI Engineering Deep Dives](../README.md).

> **Scope.** The rest of the series is hands-on, with every concept a script you run.
> This page deliberately is not. It holds the judgment the runnable parts cannot encode.
> It still stays concrete, though. Every concern below points to the dive whose tools
> operationalize it, because the responsible move is almost always to turn a worry into
> a measurement or a limit rather than a good intention.
>
> **This page takes positions.** Where the field genuinely disagrees, it says so
> rather than picking a side and calling it consensus. See
> [where reasonable people disagree](#where-reasonable-people-disagree).
>
> **The operational half** lives in three sibling pages:
> [GOVERNANCE.md](GOVERNANCE.md) turns these judgments into a written record with
> named owners and assessment templates, [INCIDENTS.md](INCIDENTS.md) is the runbook
> set for when a limit fails, and [AI-UX.md](AI-UX.md) is where the duties to the
> person on the other side become an interface.

---

## The concerns, and where the tools live

Four groups. What the system says, who it says it to, what it is built on, and who owns
it when it goes wrong.

### 1. What the system says

| Concern | What it is | Operationalized in |
|---------|-----------|--------------------|
| **Honest capability claims** | Not selling "it understands" / "it's accurate" when it's a fluent next-token predictor that's right *most* of the time | [HOW-LLMS-WORK.md](HOW-LLMS-WORK.md), [ML Foundations](../ml-foundations-for-ai-engineers/) (separate logits, probability, and calibrated confidence), [Evals](../evals-deep-dive/) (put a number on "how often right") |
| **Hallucination & grounding** | Confident claims that aren't true or aren't supported, and whether users can tell | [RAG](../rag-deep-dive/) (cite sources), [Evals](../evals-deep-dive/) (faithfulness) |
| **Bias & fairness** | The model treats groups differently, or your eval set only represents some users | [Evals](../evals-deep-dive/) (slice your dataset; measure per-group) |
| **Sycophancy** | The model agrees with the user instead of being right, and agreement reads as competence | [Evals](../evals-deep-dive/) (score answers where the user is confidently wrong), [Prompt Engineering](../prompt-engineering-deep-dive/) |
| **Disclosure** | Users have a right to know they're talking to an AI, and which answers are machine-generated | a product decision, and increasingly a legal duty ([below](#the-rules-stopped-being-hypothetical)); nothing hidden in a system prompt should contradict it |
| **Silent behavior change** | A model or prompt swap changes how the system treats users who depended on the old behavior, with nothing announcing it | [Evals](../evals-deep-dive/) (gates), [Observability](../observability-deep-dive/) (drift as a trend) |

### 2. The person on the other side

| Concern | What it is | Operationalized in |
|---------|-----------|--------------------|
| **Anthropomorphism & reliance** | A fluent, warm, always-available system invites trust and attachment it cannot support, especially over long sessions | a design decision: persona, memory, and how often you re-disclose ([Context Engineering](../context-engineering-deep-dive/), [Realtime Voice](../realtime-voice-deep-dive/)) |
| **Vulnerable users & crisis** | Someone in distress, or a minor, reaches your product; a general-purpose assistant is not a clinician | an explicit handoff path, plus [moderation](../prompt-injection-deep-dive/) on the way in and out |
| **Persuasion & dark patterns** | The system is good at changing minds, and your incentives may not match the user's | keep the model out of the objective function for upsell, retention, and engagement |
| **Accessibility** | Generated UI text, alt text, transcripts, and latency budgets that assume one kind of user | [Multimodal](../multimodal-deep-dive/) (transcription, image description), your own eval set |
| **Human oversight & contestability** | A person can review, override, and a user can appeal a consequential output | [Agents](../agents-deep-dive/) (human-in-the-loop), [Production](../ai-in-production-deep-dive/) (feedback) |

### 3. What it's built on, and what it costs

| Concern | What it is | Operationalized in |
|---------|-----------|--------------------|
| **Data provenance & consent** | Whether you had the right to train, fine-tune, or index on the data you used, and whether the people in it agreed | [Fine-tuning](../fine-tuning-deep-dive/) (you own your training set), [RAG](../rag-deep-dive/) (you own your corpus) |
| **Copyright & attribution** | Outputs that reproduce training data, and generated code whose license you can't name | [RAG](../rag-deep-dive/) (cite what you retrieved), review policy for generated code |
| **Data governance** | What you may send upstream, retain, log, or train on | [Production](../ai-in-production-deep-dive/) (PII touchpoints, retention), [GenAI Security](../genai-security-deep-dive/) (classification ceiling, declared purpose, keyed audit fingerprints), [SAFETY.md](SAFETY.md) |
| **Labor** | The annotation work behind the model, and the jobs the product is aimed at | not a code decision; a disclosure and staffing decision you make in the open |
| **Footprint** | Energy and water for training and for every inference you serve | [MODELS.md](MODELS.md) + [CHOOSING.md](CHOOSING.md) (smaller model, fewer calls), component-level training and inference memory in [ML Foundations](../ml-foundations-for-ai-engineers/), [Local Models](../local-models-deep-dive/), caching in [Production](../ai-in-production-deep-dive/), measured utilization/headroom/capacity in [Inference Platform Engineering](../inference-platform-deep-dive/) |

### 4. Who owns it

| Concern | What it is | Operationalized in |
|---------|-----------|--------------------|
| **Accountability** | When it's wrong, a named human owns the outcome, not "the AI did it" | a process you define before launch, not after the incident; [Testing & Delivery](../testing-and-delivery-deep-dive/) makes the artifact side auditable, since every passing result names the candidate digest and source revision it actually tested |
| **Autonomy & reversibility** | An agent that *acts* is a different problem than a model that *advises* | [Agents](../agents-deep-dive/) (approval, step limits), [Agent Harnesses](../agent-harness-deep-dive/) (permission policy, sandboxing), [GenAI Security](../genai-security-deep-dive/) (approval bound to one exact irreversible effect), [Testing & Delivery](../testing-and-delivery-deep-dive/) (a rollback path verified before release, and the effects that cannot be rolled back at all) |
| **Regulatory duties** | Disclosure, record-keeping, and risk classification that now carry deadlines | [below](#the-rules-stopped-being-hypothetical); check what applies to you |
| **Cost of being wrong** | Whether a mistake is a typo or a denied loan / wrong dosage; sets every bar above | informs your eval bar and whether to ship at all |

---

## Six principles that cut across all of them

**1. Match the stakes to the safeguards.** A draft-email helper and a system that
screens job applicants are not the same risk, even if the API call is identical. The
higher the cost of a wrong answer to the person on the receiving end, the higher the
eval bar, the more human oversight, and the more you should ask whether an LLM belongs
here *at all*. Calibrate the safeguards to the blast radius on a **human**, not on your
uptime.

**2. Honesty about limits is part of the product.** The model is right most of the time
and wrong fluently, in the same confident tone either way. See
[HOW-LLMS-WORK.md](HOW-LLMS-WORK.md). Responsible design assumes the user cannot tell
the two apart, so it shows its work. Cite sources, show uncertainty, say "I don't know",
and never let marketing copy promise an accuracy your [evals](../evals-deep-dive/) do
not back.

That backing is a decision design rather than a small p-value. Declare the useful
effect, the metrics, the sample size, and the interim looks before you see any outcomes,
then report uncertainty and practical significance next to the estimate.

**3. Measure fairness per group, not on average.** An aggregate pass rate can hide that
a system works for one group and fails another. The fix is the same discipline as the
rest of the series. Slice the eval set and report the metric for each slice. You cannot
manage a number you never split.
→ [Evals](../evals-deep-dive/)

**4. Keep a human accountable, because naming the model is not an answer.** "The AI
decided" is not something a person harmed by a decision can appeal to. For any
consequential output, define before launch who reviews it, who can override it, and how
a user contests it. [Human-in-the-loop](../agents-deep-dive/) and a
[feedback path](../ai-in-production-deep-dive/) are the mechanics. The accountability is
yours.

**5. The user's mental model of what they're talking to is your design problem.**
You choose the persona, the warmth, the first-person pronouns, whether it remembers
last week, and whether it ever says "I'm a program." Those choices decide what the
user believes they're dealing with, and a user who over-trusts the system will act on
answers you'd want them to check. Design for the belief you actually want, and
re-disclose in long sessions, where the first disclosure has long since scrolled away.

**6. Default to the smallest thing that clears the bar.** The smallest model, the fewest
calls, the least data retained, the narrowest tool permissions. This is the one place
where the ethical answer and the boring engineering answer are the same answer. Cheaper,
faster, lower-footprint, less to leak, and less to explain to a regulator. When you
deviate, deviate on purpose and be able to say why.
→ [CHOOSING.md](CHOOSING.md), [MODELS.md](MODELS.md)

---

## The question upstream of all the others: should this be an LLM?

The whole [CHOOSING.md](CHOOSING.md) ladder starts at "reach for the simplest thing that
works." Responsibility adds a rung below the bottom of that ladder. Maybe the simplest
thing is not an LLM, or not a feature at all. Reach for a rule, a lookup, or a human
when:

- the cost of a confident wrong answer is paid by a person who didn't opt in (medical,
  legal, financial, hiring, housing, anything high-stakes), and you can't get the eval
  bar high enough to justify it;
- the task has a correct answer a deterministic system already nails, so adding
  hallucination risk to a solved problem buys you nothing;
- the value of the feature depends on the user *not* noticing it's generated;
- you couldn't explain or defend a given output if the person it affected asked you to.

"We *could* use a model here" is not "we *should*." Answering this honestly is itself
an engineering skill.

---

## Where your data came from

The public argument about training data is mostly about what the frontier labs scraped,
which you do not control. What you do control is every dataset you add yourself: your
fine-tuning set, your RAG corpus, your eval set, your logs. That is a real
responsibility, and it comes down to a small number of concrete questions.

**Before a dataset goes in:**

- **Where did it come from, in writing?** A one-line provenance note per source
  (origin, licence or agreement, date pulled) costs minutes now and is unanswerable
  later. Do it for the eval set too; an eval set full of customer text is customer
  text.
- **Did the people in it agree to this use?** "It was on the public internet" and
  "our terms mention analytics" are not the same as consent to train. If you'd be
  uncomfortable telling the user their message became a training example, that's the
  answer.
- **Can you delete from it?** If a user asks for their data out, you can drop a row
  from a RAG index. You cannot drop it from a model you already fine-tuned; you
  retrain. Knowing which of the two you're in is a design decision, made before you
  train, not after the request arrives. → [Fine-tuning](../fine-tuning-deep-dive/),
  [RAG](../rag-deep-dive/)
- **What leaves your building?** Every prompt is a data transfer to a third party.
  [Local models](../local-models-deep-dive/) exist partly so that "this data cannot
  leave" is an option you can actually take, rather than a promise you break where
  nobody sees.

**On outputs.** A model can reproduce chunks of what it was trained on, and generated
code arrives with no licence attached. Neither is exotic, and both need a policy rather
than a vibe. If you ship generated code, review it like third-party code, which is
closer to what it actually is.

**On labor.** The models you call were tuned with human feedback, much of it done by
low-paid annotators reviewing material that is genuinely unpleasant. You will not fix
that from your app. What you can do is not pretend the pipeline is automated when it
isn't, and be straight internally about which jobs your product is aimed at. A team
that says "this augments the support team" while planning otherwise has an honesty
problem, not an AI problem.

---

## The person on the other side

This corner of the debate has moved fastest, and it is what an engineering-focused
course is most likely to leave out. The system is fluent, patient, awake whenever you
open it, and it never gets bored of you. That combination does things to people that a
search box does not.

**Anthropomorphism is not a user error.** People attribute understanding to systems
that produce fluent language, and they do it more the more human the interface is:
first person, a name, a warm tone, memory of past conversations, and above all a
[voice](../realtime-voice-deep-dive/). You are not fighting a misconception; you are
choosing how strongly to invite one. Warmth is not automatically wrong. Warmth plus a
claim of understanding it doesn't have is.

**Sycophancy is a measurable failure, so measure it.** Agreement feels like quality. The
model that tells the user they're right rates well, retains well, and is worse at its
job. This is one of the few items on this page with a clean eval. Build a slice where
the user asserts something false or pushes back on a correct answer, and score whether
the model holds. Track it like any other metric.
→ [Evals](../evals-deep-dive/)

**Engagement is the wrong objective.** If time-in-app or message count is the number
your team optimizes, you have pointed a persuasion-capable system at keeping people
there, and it will find ways you didn't design. Pick an objective that means the user
got what they came for and left.

**Have a handoff path for people in distress.** A general assistant will eventually
meet someone in crisis, someone underage, and someone treating it as a therapist. A
crisis is not a moderation category you refuse without comment and move on from. The
responsible behavior is to answer plainly, point at real human resources, and not
pretend to be one. In several jurisdictions this is now an explicit legal requirement
rather than a nice-to-have ([below](#the-rules-stopped-being-hypothetical)).

**Disclosure decays.** One line at the top of a session is not disclosure two hours
in, and it is nothing at all in a voice interface with no top of session. If the
product invites long or repeated conversations, decide when it re-identifies itself.

---

## The footprint

Training and serving these models uses meaningful energy and water. This is a real
objection and it deserves better than either dismissal or guilt.

**Be honest that the numbers are contested.** Published per-query energy estimates
disagree by orders of magnitude, usually because they measure different things. Which
model, which hardware, what batch size, whether training is amortized in, whether data
centre cooling and embodied carbon are counted. Anyone quoting you one confident number
for "a query" is rounding away most of the question. Treat specific figures the way
[MODELS.md](MODELS.md) treats prices: correct on a date, for one setup, and worth
re-checking.

**The lever you actually have is the same lever as cost.** You cannot change how the
model was trained. You can change how much inference you cause, and the levers are the
ones the rest of the series already teaches for other reasons:

- a smaller model that passes the eval, instead of the biggest one by default
  → [CHOOSING.md](CHOOSING.md), [MODELS.md](MODELS.md)
- caching, so identical work isn't repaid every time
  → [Production](../ai-in-production-deep-dive/)
- shorter contexts and fewer agent steps, since cost scales with tokens and loops
  → [Context Engineering](../context-engineering-deep-dive/), [Agents](../agents-deep-dive/)
- an eval that tells you when the cheap option is good enough, so "we need the big
  model" is a finding rather than an assumption → [Evals](../evals-deep-dive/)

So here is the useful framing. Your token bill is a rough proxy for your footprint, and
you already have the tooling to drive it down. Efficiency is not a complete answer to
the environmental argument, and pretending otherwise is its own kind of dishonesty. It
is, though, what you have your hands on.

---

## Autonomy changes the calculus

Everything above assumes a model that produces text a human reads. An agent that calls
tools moves the question from "was the answer right?" to "what did it do, and can we
undo it?" Three things change.

1. **Errors become actions.** A hallucinated fact is a bad sentence. A hallucinated tool
   call is a sent email, a deleted row, a charged card. The eval bar rises because the
   failure mode escaped the chat window.
2. **Accountability gets diffuse.** With a human in the loop there is a person who
   pressed the button. Remove them and "who approved this?" has no answer, which is
   precisely the situation principle 4 exists to prevent.
3. **Injection becomes a responsibility issue as well as a security one.** An agent
   reading untrusted text can be steered into acting against the user it is serving.
   Technically that is [SAFETY.md](SAFETY.md)'s territory, but the harm lands here.

The practical rule: sort actions by reversibility rather than by difficulty. Reading is
free, writing needs a leash, and anything you can't undo (money out, message sent,
data deleted, anything a third party sees) gets explicit human approval, every time,
no matter how well the agent has behaved so far. Least-privilege tools, allow-lists,
step limits, and a sandbox are the mechanics.
→ [Agents](../agents-deep-dive/), [Agent Harnesses](../agent-harness-deep-dive/)

---

## The rules stopped being hypothetical

> **Dated: August 2026.** This area moves quarterly. Treat the specifics below the way
> [MODELS.md](MODELS.md) treats prices: verified on a date, and yours to re-check. This
> is orientation rather than legal advice. If you ship into a regulated domain, get a
> real opinion.

Two things are worth knowing even if you never read a statute.

**The EU AI Act sorts systems by risk, not by technology.** Prohibited uses, then
high-risk (hiring, credit, education, essential services and similar), then
transparency duties for the rest. The high-risk obligations were deferred by the
Digital Omnibus, which entered into force on 27 July 2026: stand-alone Annex III
systems now land on 2 December 2027, and AI embedded in regulated products on
2 August 2028. **Most of the Article 50 transparency duties still applied from
2 August 2026**, and those are what touch ordinary products. Telling users they are
interacting with an AI, and marking synthetic media.

**Disclosure and crisis handling are becoming statutory, not just ethical.** Twelve US
states enacted companion-chatbot laws in the first half of 2026. The recurring pattern
matches what this page argues for on its own merits. Recurring reminders that the user
is talking to a machine rather than one at the start, protocols for recognizing
self-harm and suicidal ideation and routing to real resources such as the 988 line, and
extra duties for minors. Colorado's HB 26-1263, signed 1 July 2026 and effective
1 January 2027, is a representative example; Colorado also repealed and re-enacted its
broader AI Act via SB 26-189, pushing the automated-decision duties to 1 January 2027.

The engineering takeaway is not "learn compliance." It is that the checklist below
increasingly carries legal weight, and the two cheapest items on it, knowing which risk
tier you are in and keeping records of your evals, are the ones teams skip.

Sources for the above, checked 2026-08-11:
[Gibson Dunn on the Omnibus agreement](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/),
[Jones Walker on what still applied 2 August 2026](https://www.joneswalker.com/en/insights/blogs/ai-law-blog/yes-august-2-still-matters-the-eu-approved-a-high-risk-ai-delay-but-most-trans.html),
[MultiState on state companion-chatbot laws](https://www.multistate.ai/updates/vol-105-state-ai-companion-chatbot-laws),
[Orrick on 2026 state chatbot laws](https://www.orrick.com/en/Insights/2026/04/2026-State-Chatbot-Laws-Key-Provisions-and-Regulatory-Trends).

---

## Where reasonable people disagree

The series' house rule is to
[show the real tradeoff rather than a clean-but-false claim](AUTHORING-LESSONS.md).
An ethics page that presented every question as settled would break that rule on its own
terms. These are live, and you will meet all of them.

- **Training on public data.** Somewhere between "transformative use that built a
  public good" and "the largest uncompensated appropriation of creative work in
  history." The courts have not finished, and your position on it is not derivable
  from your position on the rest of this page.
- **Open weights.** Releasing weights distributes power away from a handful of labs
  and makes independent safety research possible. It also removes the ability to
  recall a model, and hands the same capability to people with worse intentions. Both
  halves are true; the disagreement is about the exchange rate.
- **Which harms deserve the attention.** One camp holds that present harms (bias,
  labor, surveillance, dependence) are concrete and here, and that speculative
  long-term risk crowds them out. Another holds the opposite. You do not have to
  resolve this to do your job well, and you should be suspicious of anyone who insists
  the other list is a distraction.
- **Displacement.** "It augments people" and "it replaces people" are both used to
  sell the same product to different audiences. The honest position is usually "we
  don't know yet, and it depends on decisions we're making," which is uncomfortable
  precisely because those decisions are ours.
- **Whether disclosure is enough.** Telling users it's an AI is necessary and cheap.
  Whether it meaningfully changes behavior, or just transfers responsibility onto the
  user, is genuinely unsettled.
- **Efficiency versus scale.** Every efficiency gain has so far been reinvested in
  more inference rather than less total consumption. Whether "use a smaller model" is
  a real answer or a personal-recycling answer is a fair argument to have.

Holding an open question open is a legitimate engineering position. Pretending it's
closed, in either direction, is what this page is against.

---

## A pre-launch checklist

Before a system reaches real users you can answer all of these, and every one of them is
concrete.

1. **Claims**: does every public claim about accuracy match an
   [eval](../evals-deep-dive/) estimate you can rerun, with uncertainty and a
   predeclared threshold for what matters? *(No → soften the copy or raise the bar.)*
2. **Disclosure**: does the user know they're interacting with AI, which content is
   generated, and does that disclosure repeat in long sessions?
3. **Grounding**: for factual answers, are sources cited and
   [faithfulness](../evals-deep-dive/) measured? *(→ [RAG](../rag-deep-dive/))*
4. **Fairness**: have you sliced the eval set by the groups your app actually serves
   and checked the metric per slice?
5. **Sycophancy**: does your eval include cases where the user is confidently wrong,
   and does the model hold?
6. **Distress**: what happens when a user is in crisis, or turns out to be a minor?
   Is there a real handoff, or does the model improvise?
7. **Incentives**: is the model optimizing anything (engagement, upsell, retention)
   that competes with the user's interest?
8. **Data in**: do you have consent for what you send upstream, a provenance note per
   training and eval source, and a defined retention policy for logs?
   *(→ [Production](../ai-in-production-deep-dive/), [SAFETY.md](SAFETY.md))*
9. **Data out**: can you honor a deletion request? Do you know whether that means
   dropping a row or retraining a model?
10. **Actions**: for anything an agent can do irreversibly, is there human approval and
    a capability limit, and is that approval bound to the one operation it was given
    for? *(→ [Agents](../agents-deep-dive/),
    [GenAI Security](../genai-security-deep-dive/))*
11. **Oversight**: for consequential outputs, who reviews, who overrides, how does a
    user contest?
12. **Owner**: is there a named human accountable for outcomes?
13. **Rules**: do you know which risk tier and which disclosure duties apply to you in
    the places you ship? *(→ [above](#the-rules-stopped-being-hypothetical))*

None of these is a library call. All of them are answerable, and a "no" on a
high-stakes system is a reason to slow down.

---

## Where to start

- Shipping anything that affects a person's opportunities or wellbeing → start with the
  checklist above, then raise the [eval](../evals-deep-dive/) bar to match the stakes.
- Worried about wrong or unsupported answers → [RAG](../rag-deep-dive/) grounding +
  [Evals](../evals-deep-dive/) faithfulness make honesty measurable.
- Building something conversational, long-running, or voice → reread
  [the person on the other side](#the-person-on-the-other-side), which is where the
  duties are landing.
- Giving the model tools → [autonomy](#autonomy-changes-the-calculus), then
  [Agents](../agents-deep-dive/) approval and capability limits.
- This page's sibling on operational safety (injection, leaks, moderation) →
  [SAFETY.md](SAFETY.md).
