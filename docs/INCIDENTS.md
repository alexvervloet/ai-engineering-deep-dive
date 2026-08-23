# Incidents: what to do when it goes wrong at 2am

[SAFETY.md](SAFETY.md) is about the limits you build in advance.
[GOVERNANCE.md](GOVERNANCE.md) is about the record of what you decided. This page is
for the hour when a limit did not hold. It is a set of playbooks you can follow while
tired, plus the containment levers you have to build **before** you need them. Part
of the [AI Engineering Deep Dives](../README.md).

> **Scope.** These are runbooks, not theory. Each one assumes you are mid-incident
> and skims: what you are looking at, stop the bleeding, find the blast radius, then
> fix. Adapt the thresholds to your system; the shape holds.

---

## 0. The one big idea

> **Most AI incidents are not outages. They are the system working, confidently, and
> being wrong.**

A crashed service pages you. A retrieval index that went stale three weeks ago and told
nobody does not. This changes the job in two ways. Detection has to be something you
built on purpose, because failure is not self-announcing. And containment is usually
about narrowing what the system is allowed to do, not about restarting it, because
restarting a confidently wrong system gives you a confidently wrong system.

---

## 1. Severity: decide this first, in one minute

| Sev | Meaning | Examples | Response |
|---|---|---|---|
| **Sev-1** | Ongoing harm to people, or data out the door | PII in outputs to other users, an agent taking destructive real-world actions, tenant boundary crossed | Page now. Contain before you diagnose. |
| **Sev-2** | Wrong at scale, or a security control failed | Injection working in production, quality collapse on a main path, spend running away | Page during working hours, contain today |
| **Sev-3** | Degraded, bounded, no one harmed yet | One tool failing, latency doubled, a narrow class of bad answers | Ticket, fix this week |
| **Sev-4** | Cosmetic or theoretical | Ugly formatting, a jailbreak that reaches nothing | Backlog |

Two rules that save arguments at 2am:

- **Uncertainty rounds up.** If you cannot tell whether data left, it is a Sev-1
  until you can.
- **Blast radius beats severity of a single case.** One user seeing a bad answer is
  Sev-3. Every user seeing it is Sev-2, even if each instance is mild.

---

## 2. The first thirty minutes

Do these in order. Do not skip to diagnosis; that is the classic way to spend an hour
being clever while harm continues.

1. **Name an incident commander.** One person, said out loud. They coordinate and do
   not also debug.
2. **Start a timeline.** One channel, timestamps, decisions as you make them. You are
   writing the postmortem now, badly, so that later you can write it well.
3. **Contain.** Pull a lever from section 3. Containment before understanding is
   correct here; you can widen again once you know more.
4. **Bound the blast radius.** How many requests, which users, which tenants, over
   what window. Query the logs before they roll off.
5. **Preserve evidence.** Snapshot the traces, the index revision, the prompt
   version, the model id, the release evidence bundle. All of it becomes unavailable
   the moment someone redeploys.
6. **Decide on disclosure.** Not "do we tell anyone eventually" but "who has to know
   in the next hour," which may include users, a customer, or a regulator.

---

## 3. Containment levers, which you build in advance

An incident is the wrong time to discover you have no way to turn one thing off.
Build these before you need them, and test them the way you test a rollback.

| Lever | What it does | Build it in |
|---|---|---|
| **Kill switch** | Disables the AI path, falls back to the non-AI experience | [Production](../ai-in-production-deep-dive/) |
| **Model pin** | Forces one known-good model and prompt version | [Testing & Delivery](../testing-and-delivery-deep-dive/) |
| **Tool disable** | Turns off one tool without taking the system down | [Agents](../agents-deep-dive/), [Agent Harnesses](../agent-harness-deep-dive/) |
| **Spend cap** | Hard stop on tokens per minute and per tenant | [Production](../ai-in-production-deep-dive/) |
| **Read-only mode** | Model can answer, cannot act | [GenAI Security](../genai-security-deep-dive/) |
| **Tenant isolation switch** | Cuts one tenant off from shared paths | [Architecture](../architecture-deep-dive/) |
| **Index rollback** | Reverts to a previous corpus revision | [AI Data Engineering](../ai-data-engineering-deep-dive/) |

The test for each: can an on-call engineer who did not build it trigger it in under
five minutes, from a runbook, without a deploy? If not, it is a plan, not a lever.

---

## 4. Runbook: prompt injection reaching a tool

**Signs.** Tool calls that no user request explains. Outputs quoting instructions
from retrieved documents. An agent visiting a domain nobody configured.

1. **Contain:** read-only mode, or disable the specific tool. Do not start by
   rewriting the system prompt; that is a fix, not containment.
2. **Scope:** find every session that touched the poisoned source. Injection arrives
   through content, so the question is "which documents," not "which users."
3. **Quarantine the source.** Pull the document, page, or record out of the index.
   Record its revision before you delete it.
4. **Check what the tools actually did.** Every side effect, not every response.
   Money moved, mail sent, records changed, data read.
5. **Fix:** the durable fix is almost never a better prompt. It is narrowing what the
   tool can do and who can call it. See
   [Prompt Injection](../prompt-injection-deep-dive/) for why prompt-level defenses
   degrade, and [GenAI Security](../genai-security-deep-dive/) for authorizing effects
   in code.

---

## 5. Runbook: PII or secrets in output

**Signs.** A user reports seeing someone else's data. A secret scanner fires on
generated content. Support sees an answer containing an address nobody supplied.

1. **Contain immediately.** Sev-1 by default. Kill switch or read-only, not a patch.
2. **Determine direction.** Did data leak *out* to a user, or *up* to a provider in a
   prompt? They have different obligations and different fixes.
3. **Bound it.** Which records, which users saw them, over what window. If logs do
   not let you answer this, that gap is itself a finding for the postmortem.
4. **Check the three touchpoints:** what you send, what you log, what you retain.
   The [PII checklist in SAFETY.md](SAFETY.md) is the short version.
5. **Purge deliberately.** Prompts and completions live in your logs, your traces,
   your eval sets, and possibly the provider's retention window. Deleting the
   database row is the beginning of the job.
6. **Disclosure is likely mandatory.** Do not let this decision sit with the on-call
   engineer. Escalate to whoever owns that duty, today.

---

## 6. Runbook: harmful, defamatory, or dangerous output

**Signs.** A screenshot. Almost always a screenshot.

1. **Get the exact input and output.** Not a paraphrase. Reproduce it if you can, and
   record whether you could, since non-reproducible cases are still real.
2. **Contain by narrowing scope,** not by patching one string. Blocking the exact
   phrase teaches you nothing and stops nothing similar.
3. **Ask whether it is a class.** One offensive completion is a bug. A prompt pattern
   that reliably produces them is a Sev-2.
4. **Handle the person first.** Someone received this. The appeal and remedy path in
   [GOVERNANCE.md](GOVERNANCE.md) applies, and it applies faster than your fix.
5. **Add it to the eval set** before you fix it, so the fix is measured and the
   regression is caught next time. See [Evals](../evals-deep-dive/).

---

## 7. Runbook: silent quality regression

This is the most common serious AI incident and the least likely to page anyone.

**Signs.** Support volume up with no deploy. Thumbs-down rate drifting. Citation
resolve rate falling. A model version changed under you.

1. **Establish when.** Compare against your baseline eval run, not against memory.
   If you have no baseline, that is finding number one.
2. **Check the artifact tuple first.** Model version, prompt version, index revision,
   embedding model, SDK version. Regressions usually arrive as a change in one of
   these, and a hosted model can change without you deploying anything.
3. **Bisect by component.** Retrieval quality and generation quality fail
   differently. Measure hit rate separately from answer correctness.
4. **Contain by pinning** to the last known-good tuple while you diagnose.
5. **The durable fix is detection,** not the specific regression. If this ran for
   three weeks, the finding is that nothing watches quality as a trend. See
   [Observability](../observability-deep-dive/).

---

## 8. Runbook: cost blowout or runaway loop

**Signs.** Spend graph turns vertical. An agent iterating without converging.
Retries amplifying an upstream failure.

1. **Cap first, diagnose second.** Spend caps and rate limits exist for this minute.
2. **Look for the loop.** Agents that retry, tools that call the model, and retries
   with no budget are the usual causes. A retry storm during a partial outage is the
   classic version.
3. **Check for amplification.** One user request causing many model calls is normal
   for agents and pathological past a bound. Find the bound you never set.
4. **Check whether it is an attack.** Unbounded cost is a denial-of-wallet vector.
5. **Fix:** step limits, retry budgets, and per-tenant caps.
   [Agents](../agents-deep-dive/) covers step limits;
   [Testing & Delivery](../testing-and-delivery-deep-dive/) covers retry budgets that
   stop incident amplification.

---

## 9. Runbook: provider outage or deprecation

**Signs.** Elevated errors from one provider. A deprecation email with a date on it.

1. **Fail over if you have a tested fallback.** If it is untested, decide
   consciously whether an untested path is better than a clear error message. Often
   it is not.
2. **Watch correctness, not just availability.** A fallback model that answers
   everything wrong looks healthy on an uptime graph.
   [Architecture](../architecture-deep-dive/) measures exactly this trade.
3. **Degrade honestly.** Tell users the system is limited right now. A silent
   downgrade is how trust is lost permanently.
4. **For deprecation:** treat it as a material change in
   [GOVERNANCE.md](GOVERNANCE.md) terms. New model, new evidence, full eval run.

---

## 10. Runbook: corpus poisoning or contamination

**Signs.** Confident answers citing a document that should not exist. Content from
one tenant surfacing for another. An ingest job that ran with the wrong permissions.

1. **Freeze ingestion.** Stop making it worse.
2. **Identify the revision** where the bad content entered. This is why the corpus
   is versioned. If it is not versioned, that is finding number one.
3. **Roll the index back,** then re-ingest forward with the fix.
4. **Check permission propagation.** If ACLs did not travel with the chunk, the leak
   is structural rather than a one-off.
5. See [AI Data Engineering](../ai-data-engineering-deep-dive/) for versions, lineage,
   and deletes as first-class operations.

---

## 11. Communication templates

**Internal, at declaration:**

```markdown
**Incident <id>** declared Sev-<n> at <time UTC>.
Commander: <name>.
Symptom: <what is observed, not what we think causes it>.
Contained by: <lever pulled>, at <time>.
Blast radius so far: <requests / users / tenants / window>.
Next update: <time>.
```

**User-facing, during:**

```markdown
We have limited <feature> while we investigate an issue affecting <what>.
<What the user can do instead, if anything.>
We will update by <time>.
```

Say what is affected and what they can do. Do not explain the cause while you are
still guessing at it, and do not promise a resolution time you are inventing.

**User-facing, after, when someone was actually affected:**

```markdown
Between <start> and <end>, <specific thing that happened> affected <who>.
What we did: <containment and fix>.
What this means for you: <concrete, including any action they need to take>.
What we changed so it does not recur: <the durable fix>.
If this affected you and you want it reviewed: <the appeal path>.
```

---

## 12. Postmortem template

Blameless, written within a week, and worth reading a year later.

```markdown
# Postmortem: <title> (<id>, Sev-<n>)

**Date:** <date>   **Duration:** <detect to resolve>   **Commander:** <name>

## What happened
Two paragraphs a new engineer could follow.

## Impact
Users, tenants, requests, money, and any harm to a person. Numbers, not adjectives.
If you cannot measure part of it, say which part and why.

## Timeline
| Time (UTC) | Event |
|---|---|
Include when it started and when anyone *noticed*. The gap between those two is
usually the most useful number in the document.

## Detection
How did we find out? If the answer is "a user told us," that is the finding.

## Root causes
Plural. Stop at the first cause and you fix a symptom. Include the contributing
conditions, such as the missing alert or the untested fallback.

## What went well
Real entries only. A lever that worked is worth keeping.

## Actions
| Action | Type | Owner | Due |
|---|---|---|---|
Type is detect / prevent / mitigate / respond. If every action is "prevent," you
have not thought about the next unknown failure.

## What we are not doing
The fixes considered and rejected, with the reason. This is the section that stops
the same debate happening in six months.
```

---

## 13. What to measure afterwards

Four numbers tell you whether your incident practice is improving:

- **Time to detect.** The one that matters most for AI systems, and usually the worst.
- **Time to contain.** Tests whether your levers are real.
- **Percentage detected by monitoring rather than by users.** Start honest; it is
  often low.
- **Repeat rate.** Incidents recurring from the same root cause mean the postmortem
  produced tickets rather than change.

---

## 14. Anti-patterns

- **Diagnosing before containing.** Harm continues while you are being clever.
- **The fix that is a prompt edit.** Fine as mitigation. As the durable fix for a
  security incident, it is wishful.
- **Redeploying before snapshotting.** You have destroyed the evidence.
- **Severity negotiated down because it is inconvenient.** Write the real severity
  and the reason for the response you chose.
- **A postmortem with no "what we are not doing" section.** It will be rewritten
  from scratch next time.
- **No named commander.** Six people investigate, nobody contains, nobody talks to
  the affected user.

---

## Where to start

If you have nothing today:

1. **Build one kill switch** and test it. Everything else is easier once you can
   stop the system without a deploy.
2. **Write the severity ladder** and put it where on-call can find it. One page.
3. **Run one postmortem** on the last thing that went wrong, even a small one. The
   template teaches the practice better than reading about it.
