# Reference docs

The series-level docs, meaning everything that is not a dive. Each dive is
self-contained and links back here for the shared material, so nothing below assumes
you have finished any particular dive.

The series itself lives one level up, in [the main README](../README.md).

---

## Foundations

Read these before or alongside the first dive. They hold the shared vocabulary and
the decisions the dives assume you have already made.

- [HOW-LLMS-WORK.md](HOW-LLMS-WORK.md) is the mental model underneath the whole
  series. Next-token prediction, training, why models hallucinate, the context
  window. No math. Read it first if "what is an LLM?" is still fuzzy.
- [GLOSSARY.md](GLOSSARY.md) defines every term the series assumes (token, embedding,
  context window, temperature, RAG, agent, eval, guardrail, quantization, and the
  rest), each one cross-linked to the dive that teaches it.
- [CHOOSING.md](CHOOSING.md) is the decision guide. Prompt, few-shot, RAG, fine-tune,
  agent, and when to reach for multimodal, local, or MCP.
- [MODELS.md](MODELS.md) lists the models the series uses, their context windows and
  prices, and how to pick one. It is dated, and it tells you how to get current
  numbers.

## Practice

The working material. How to run the lessons, what to build, and what the work is
worth once you can do it.

- [SECRETS.md](SECRETS.md) says where your API keys actually go, which is your OS
  keychain, injected per command with `secrun`, and why `.env` is the wrong place.
  Moving from `.env` to the keychain is itself a lesson in the AI-agent threat model.
- [CAPSTONE.md](CAPSTONE.md) describes the whole-series capstone, a codebase Q&A tool
  called `askrepo` built step by step, one dive per tag, with its eval set pointed at
  this very repo. The build itself lives in
  [deep-dive-capstone](../deep-dive-capstone/), one tag per step from `v00-scaffold`
  to `v07-production`.
- [CAREERS.md](CAREERS.md) is the hirability map. Each dive translated into résumé
  lines, job-description phrases, and the industry tools it corresponds to
  (Braintrust, Langfuse, pgvector, vLLM, LiveKit, and others), so you can turn the
  work into interview answers.
- [AUTHORING-LESSONS.md](AUTHORING-LESSONS.md) is for anyone extending these dives.
  Principles for writing runnable teaching examples that actually prove their own
  claim, drawn from hardening the RAG examples. The reader believes the output, so
  the output has to be worth believing.

## Operating responsibly

The cross-cutting concerns. No single dive owns these, because every dive touches
them. What can go wrong, who decides, what you do at 2am, and what the person on the
other side of the screen experiences.

- [SAFETY.md](SAFETY.md) is the cross-cutting view. Injection, moderation, PII,
  hallucination, and unsafe actions, with what each one is and which dive covers it.
- [RESPONSIBILITY.md](RESPONSIBILITY.md) is the other half of safety. Honest
  capability claims, bias and fairness, sycophancy, disclosure, where your training
  data came from, what a fluent system does to the person using it, energy footprint,
  agent autonomy, the 2026 regulatory picture, and the question upstream of all of
  them, which is whether this should be an LLM at all. It ends with the arguments the
  field has not settled, left unsettled.
- [GOVERNANCE.md](GOVERNANCE.md) is the operational machinery between "we thought
  about it" and a record someone can read. Named roles, change classification, and
  copy-pasteable templates for a system register, a pre-deployment assessment, a risk
  register, a vendor assessment, and an appeal and redress path.
- [INCIDENTS.md](INCIDENTS.md) is what to do at 2am. A severity ladder, the first
  thirty minutes, the containment levers you have to build in advance, and runbooks
  for injection reaching a tool, PII in output, harmful output, silent quality
  regression, cost blowout, provider outage, and corpus poisoning. It ends with comms
  and postmortem templates.
- [AI-UX.md](AI-UX.md) treats the interface as part of the safety system. Designing
  for the wrong answer: disclosure, uncertainty that is actionable, citations that
  resolve, streaming versus guardrails, the four distinct failure states, feedback
  worth collecting, human handoff, and reversibility for systems that act.

---

## What stays at the repo root

Four docs live at the root rather than here, because each one mirrors a file that
every dive also has, and that pairing is the point.

| Root doc | What it is |
| --- | --- |
| [README.md](../README.md) | the series index, the same role each dive's README plays for its own lessons |
| [TEXTBOOK.md](../TEXTBOOK.md) | every dive's lecture chapter, in sequence, read as one book |
| [LESSONS.md](../LESSONS.md) | what went wrong building the series, the same record each dive keeps |
| [CHANGELOG.md](../CHANGELOG.md) | what changed across the series, and when |
