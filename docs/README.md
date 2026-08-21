# Reference docs

The series-level docs: everything that isn't a dive. Each dive is self-contained
and links back here for the shared material, so nothing below assumes you have
finished any particular dive.

The series itself lives one level up, in [the main README](../README.md).

---

## Foundations

Read these before or alongside the first dive. They are the shared vocabulary and
the decisions the dives assume you have already made.

- [**HOW-LLMS-WORK.md**](HOW-LLMS-WORK.md): the mental model underneath the whole
  series: next-token prediction, training, why models hallucinate, the context
  window. No math. Read it first if "what *is* an LLM?" is still fuzzy.
- [**GLOSSARY.md**](GLOSSARY.md): every term the series assumes (token, embedding,
  context window, temperature, RAG, agent, eval, guardrail, quantization, …),
  cross-linked to the dive that teaches it.
- [**CHOOSING.md**](CHOOSING.md): a decision guide: prompt → few-shot → RAG →
  fine-tune → agent, and when to reach for multimodal, local, or MCP.
- [**MODELS.md**](MODELS.md): the models the series uses, their context windows and
  prices, and how to pick one. Dated; tells you how to get current numbers.

## Practice

The working material: how to run the lessons, what to build, and what the work is
worth once you can do it.

- [**SECRETS.md**](SECRETS.md): where your API keys actually go (your OS keychain,
  injected per-command with `secrun`) and why not `.env`. The `.env` → keychain
  progression is itself a lesson in the AI-agent threat model.
- [**CAPSTONE.md**](CAPSTONE.md): the whole-series capstone: a codebase Q&A tool
  (`askrepo`) built step by step, one dive per tag, with its eval set pointed at
  this very repo. The build itself lives in
  [**deep-dive-capstone**](../deep-dive-capstone/), one tag per step from
  `v00-scaffold` to `v07-production`.
- [**CAREERS.md**](CAREERS.md): the hirability map: each dive translated into the
  résumé lines, job-description phrases, and industry tools (Braintrust, Langfuse,
  pgvector, vLLM, LiveKit, …) it corresponds to, so you can turn the work into
  interview answers.
- [**AUTHORING-LESSONS.md**](AUTHORING-LESSONS.md): for anyone extending these dives:
  principles for writing runnable teaching examples that actually prove their own
  claim, drawn from hardening the RAG examples. The reader believes the output, so
  the output has to be worth believing.

## Operating responsibly

The cross-cutting concerns. No single dive owns these, because every dive touches
them: what can go wrong, who decides, what you do at 2am, and what the person on
the other side of the screen experiences.

- [**SAFETY.md**](SAFETY.md): the cross-cutting view: injection, moderation, PII,
  hallucination, and unsafe actions: what each is and which dive covers it.
- [**RESPONSIBILITY.md**](RESPONSIBILITY.md): the other half of safety: honest
  capability claims, bias & fairness, sycophancy, disclosure, where your training data
  came from, what a fluent system does to the person using it, energy footprint,
  agent autonomy, the 2026 regulatory picture, and the question upstream of all of
  them: *should* this be an LLM? Ends with the arguments the field hasn't settled,
  left unsettled.
- [**GOVERNANCE.md**](GOVERNANCE.md): the operational machinery between "we thought
  about it" and a record someone can read: named roles, change classification, and
  copy-pasteable templates for a system register, a pre-deployment assessment, a risk
  register, a vendor assessment, and an appeal and redress path.
- [**INCIDENTS.md**](INCIDENTS.md): what to do at 2am. A severity ladder, the first
  thirty minutes, the containment levers you have to build in advance, and runbooks
  for injection reaching a tool, PII in output, harmful output, silent quality
  regression, cost blowout, provider outage, and corpus poisoning. Ends with comms
  and postmortem templates.
- [**AI-UX.md**](AI-UX.md): the interface is part of the safety system. Designing for
  the wrong answer: disclosure, uncertainty that is actionable, citations that
  resolve, streaming versus guardrails, the four distinct failure states, feedback
  worth collecting, human handoff, and reversibility for systems that act.

---

## What stays at the repo root

Four docs live at the root rather than here, because each one mirrors a file that
every dive also has, and the pairing is the point:

| Root doc | What it is |
| --- | --- |
| [README.md](../README.md) | the series index, the same role each dive's README plays for its own lessons |
| [TEXTBOOK.md](../TEXTBOOK.md) | every dive's lecture chapter, in sequence, read as one book |
| [LESSONS.md](../LESSONS.md) | what went wrong building the series, the same record each dive keeps |
| [CHANGELOG.md](../CHANGELOG.md) | what changed across the series, and when |
