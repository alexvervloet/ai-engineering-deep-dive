# Governance: who decides, and on what record

[SAFETY.md](SAFETY.md) is about building a system that is safe to operate.
[RESPONSIBILITY.md](RESPONSIBILITY.md) is about whether you should build it at all
and who is accountable when it is wrong. This page is the machinery in between: the
named roles, the written record, and the templates that turn "we thought about it"
into something a reviewer, an auditor, or your future self can actually read. Part
of the [AI Engineering Deep Dives](../README.md).

> **Scope.** Everything here is a form you fill in. The templates are deliberately
> short enough to complete in an afternoon, because a governance process nobody
> finishes governs nothing. Copy them into your own repo and delete what does not
> apply.
>
> **This is not legal advice.** It is engineering practice that makes a legal or
> compliance conversation possible. Where a duty is legally specific, the template
> tells you to go and find out what applies to you.

---

## 0. The one big idea

> **Governance is a record of decisions, not a committee.**

The failure mode is not "we had no meeting." It is that six months later nobody can
say who approved the thing, what they knew, what they assumed, or what would have
changed their mind. A governance record answers four questions for any system in
production:

1. What is this, and who owns it?
2. What did we decide, and on what evidence?
3. What would make us reverse the decision?
4. Who does the person harmed by it talk to?

If your process produces documents that cannot answer those four, it is producing
paperwork rather than governance.

---

## 1. Roles: who signs what

You do not need a large organization. You need named humans. One person can hold
several of these, but a role with nobody's name on it is unowned.

| Role | Owns | Signs |
|---|---|---|
| **System owner** | The product decision. Whether this ships and stays shipped. | Release sign-off, appeal outcomes |
| **Technical owner** | The build, the evals, the rollback path. | Assessment evidence sections |
| **Data owner** | Provenance, retention, deletion, tenant boundaries. | The data section of the assessment |
| **Reviewer** | Independent read of the assessment. Not the author. | The review line |
| **Incident commander** | Named per incident, not standing. | Postmortem ([INCIDENTS.md](INCIDENTS.md)) |

The reviewer must not be the author. That is the whole point of the role, and it is
the first thing dropped when a team is busy. If the same person writes and approves,
say so on the record rather than pretending otherwise.

---

## 2. Change classification: what actually needs review

Reviewing everything is the same as reviewing nothing. Classify first.

| Class | Examples | What it needs |
|---|---|---|
| **Routine** | Prompt wording, retrieval `k`, UI copy | Eval gate green, normal code review |
| **Material** | Model swap, new tool, new data source, new user group, retention change | Full assessment update, reviewer sign-off, staged rollout |
| **Novel** | New decision the system did not make before, new population affected, first irreversible action | Everything above, plus an explicit "should this be an LLM?" answer |

The trap is that a model swap looks routine because it is one line of config. It is
not. A different model is a different artifact tuple, and everything you measured
was measured on the old one. See
[Testing & Delivery](../testing-and-delivery-deep-dive/) on why the candidate is the
tuple and not the model name.

---

## 3. Template: system register entry

One per system in production. Keep them in one directory in the repo. This is the
index everything else hangs off.

```markdown
# System register: <name>

- **Purpose:** one sentence on what decision or task this supports.
- **Status:** proposed | piloting | production | deprecated
- **System owner:** <name>
- **Technical owner:** <name>
- **Data owner:** <name>
- **First shipped:** <date>          **Last reviewed:** <date>
- **Next scheduled review:** <date>

## What it does
Inputs, outputs, and the action it can take without a human. Name the tools it
can call and which of them have external side effects.

## Who it affects
The population that experiences the output, including people who never chose to
use it. Note any group for which performance is untested.

## Artifact tuple
Prompt version, model and features, index revision and embedding dimensions,
SDK contract version, dependency lock digest.

## Autonomy
- Acts without review: <list, or none>
- Requires human approval: <list>
- Cannot do at all: <list>

## Evidence
Link the eval run, the release evidence bundle, and the last incident review.

## Reversal conditions
What measurement, complaint rate, or external change would take this out of
production. Write it now, while you have no incentive to argue.
```

---

## 4. Template: pre-deployment assessment

Complete before the first material release, and update on every material change.
This is the document a reviewer reads.

```markdown
# Pre-deployment assessment: <system> <version>

**Author:** <name>   **Reviewer:** <different name>   **Date:** <date>
**Change class:** routine | material | novel

## 1. Should this be an LLM?
What breaks if you use a rule, a lookup, or a smaller classifier instead? If the
answer is "nothing, but the LLM is faster to build," record that honestly.

## 2. What could go wrong
Three columns: failure, who it lands on, and what it costs them. Include the
failure where the system is confidently wrong rather than visibly broken.

| Failure | Who it lands on | Cost to them |
|---|---|---|

## 3. Evidence we have
- Quality: eval set, size, score, and the baseline it beat.
- Safety: injection and jailbreak results, guardrail coverage.
- Operational: latency, cost per request, error rate under load.
- Supply chain: dependency lock, scanner results, source revision.
Link each to the run that produced it. A number with no run behind it is a claim,
not evidence.

## 4. Evidence we do not have
The honest list. Populations untested, failure modes unmeasured, conditions the
eval set does not represent. This section being empty is a red flag, not a pass.

## 5. Limits we are imposing
Rate limits, spend caps, blast radius, which actions require approval, what the
system is not allowed to answer at all.

## 6. The person on the other side
How they know it is AI, how they contest the output, and what happens when they do.
Cross-reference the appeal path in section 8 of this page.

## 7. Rollback
The tested path back, who can trigger it, and the effects that cannot be undone.

## 8. Decision
Approved | approved with conditions | not approved. Conditions are dated and owned.

**Reviewer note:** what the reviewer checked independently, not just that they read it.
```

---

## 5. Template: risk register entry

One per accepted risk. An accepted risk with no owner and no review date is an
ignored risk wearing a hat.

```markdown
| ID | Risk | Likelihood | Impact | Treatment | Owner | Review by |
|----|------|-----------|--------|-----------|-------|-----------|
| R-01 | <what goes wrong, in one line> | low/med/high | low/med/high | mitigate / accept / avoid / transfer | <name> | <date> |
```

For anything marked **accept**, add a sentence: what we would have to see to stop
accepting it. That sentence is the difference between a decision and a shrug.

---

## 6. Template: vendor and model assessment

Run this before depending on a hosted model, an embedding provider, or a tool API.

```markdown
# Vendor assessment: <provider> / <model or service>

- **What we send it:** categories of data, including anything derived from user content.
- **Retention:** how long they keep it, and how we know.
- **Training use:** whether our data trains their models, and how that is switched off.
- **Region:** where it is processed.
- **Deprecation:** notice period for model retirement, and our exit path.
- **Availability:** their stated SLA and our behavior when they miss it.
- **Subprocessors:** who else touches the data.
- **Our fallback:** the second provider or the degraded mode, and whether it is tested.
```

The last line is the one people skip. A fallback that has never been exercised is
an assumption. [Architecture](../architecture-deep-dive/) measures what fallbacks
actually cost you, and the answer is usually "correctness."

---

## 7. Review cadence

Systems drift even when the code does not. The world moves, the corpus ages, the
model gets deprecated.

| Trigger | Action |
|---|---|
| Scheduled, at least annually | Full assessment refresh, or a written decision to deprecate |
| Material change | Assessment update plus reviewer sign-off |
| Any Sev-1 or Sev-2 incident | Assessment update within the postmortem |
| Model deprecation notice | Change class is material by default |
| A new population starts using it | Reassess section 2, since your evidence may not cover them |

---

## 8. Appeal and redress

If your system affects people, some of them will be affected wrongly. An appeal path
is the difference between a system that makes mistakes and a system that traps people
in them.

**The policy, in five lines:**

1. Every consequential output carries a visible way to contest it.
2. A human, not the model, decides the appeal.
3. The reviewer can see the inputs, the retrieved context, and the output.
4. There is a stated response time, and it is met or communicated.
5. Outcomes are counted, and a rising appeal rate is a product signal, not noise.

```markdown
# Appeal record: <id>

- **Received:** <date>          **Decided:** <date>
- **Output contested:** link to the request trace and the exact output.
- **Grounds:** in the person's own words.
- **Reviewer:** <name, human>
- **What the reviewer saw:** inputs, retrieved context, tool calls, output.
- **Outcome:** upheld | overturned | partially overturned
- **Remedy applied:** <what actually changed for this person>
- **Systemic?** Does this indicate a class of failures rather than one case?
  If yes, open a risk register entry and link it.
```

Track two numbers: **appeal rate** and **overturn rate**. A high overturn rate means
the system is wrong often and the appeal path is working. A near-zero appeal rate on
a consequential system usually means people cannot find the path, not that they are
happy. The user-facing half of this lives in [AI-UX.md](AI-UX.md).

---

## 9. Where the evidence comes from

Governance documents make claims. The dives are where the claims get proven.

| The claim | Proven in |
|---|---|
| "It meets a quality bar" | [Evals](../evals-deep-dive/) |
| "This exact build was tested and can be rolled back" | [Testing & Delivery](../testing-and-delivery-deep-dive/) |
| "It resists injection and the blast radius is bounded" | [Prompt Injection](../prompt-injection-deep-dive/), [GenAI Security](../genai-security-deep-dive/) |
| "We know what it costs and how it behaves under load" | [Production](../ai-in-production-deep-dive/), [Inference Platform](../inference-platform-deep-dive/) |
| "It is still working weeks later" | [Observability](../observability-deep-dive/) |
| "We know where the corpus came from and can delete from it" | [AI Data Engineering](../ai-data-engineering-deep-dive/) |
| "The boundaries between components are where we say they are" | [Architecture](../architecture-deep-dive/) |

If a governance document asserts something no dive can demonstrate, that assertion
is the weakest part of the record. Mark it as an assumption rather than letting it
read like a finding.

---

## 10. Anti-patterns

- **The assessment written after launch.** It documents what you did rather than
  informing what you do. Date it honestly if this happens.
- **The reviewer who is the author.** Record it rather than disguising it.
- **Risk accepted with no reversal condition.** That is not acceptance, it is
  deferral with extra steps.
- **A model card copied from the vendor.** Their card describes their model. Yours
  has to describe your system, on your data, for your users.
- **Governance that only runs at launch.** Most harm shows up in month four, when
  the corpus has drifted and nobody is looking.
- **An appeal path that routes to the model.** If the thing that made the decision
  also reviews it, there is no appeal.

---

## Where to start

If you have nothing today, do these three in order, and stop there until they are
real:

1. **A system register entry** for the one system already in production. An hour.
2. **The reversal conditions line.** What would take it out. Ten minutes, and it is
   the single most useful sentence in the whole record.
3. **An appeal path** with a named human on the other end.

The rest of this page is what you grow into. A short record that is true beats a
thorough one that is aspirational.
