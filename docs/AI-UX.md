# AI UX: the interface is part of the safety system

Every other page in this series is about what the system does. This one is about
what the person on the other side can see, understand, doubt, and undo. That is not
decoration on top of the engineering. A model that is right 85% of the time is a
useful product or a dangerous one depending almost entirely on whether the interface
makes the other 15% visible and recoverable. Part of the
[AI Engineering Deep Dives](../README.md).

> **Scope.** This is guidance and patterns, not a component library. It assumes you
> have read [RESPONSIBILITY.md](RESPONSIBILITY.md) on who is affected and
> [GOVERNANCE.md](GOVERNANCE.md) on appeal paths. This page is where those obligations
> become pixels.

---

## 0. The one big idea

> **Design for the wrong answer, because you are going to ship one.**

Most AI interfaces are designed around the demo, where the answer is right and arrives
fast. Production is all the other cases. The model is unsure, the retrieval missed, the
tool failed, the answer is confidently wrong, or the user asked something the system
should decline. Treat those states as an afterthought and the interface will present a
wrong answer in exactly the same confident typography as a right one, leaving the user
no way to tell them apart.

Here is the practical test for any AI feature. **Can the user tell a good answer from a
bad one without already knowing the answer?** If not, you have moved your accuracy
problem onto the user and called it a feature.

---

## 1. Say it is AI, once, clearly

People deserve to know what they are talking to, and in a growing number of
jurisdictions this is a duty rather than a courtesy. See the regulatory section in
[RESPONSIBILITY.md](RESPONSIBILITY.md).

- Disclose at the point of interaction, not only in a settings page or terms
  document.
- Once and clearly beats a badge on every message. Repetition becomes wallpaper.
- Say what it can do and what it cannot, in the user's terms rather than yours.
- Never imply a human is present when one is not. Fake typing indicators and human
  first names on a bot are the clearest version of this mistake.

**Anti-pattern:** the tiny grey "AI-generated" label under a paragraph of confident
prose. It is technically disclosure and practically invisible.

---

## 2. Show uncertainty where it is actionable

Showing uncertainty is not the same as showing a number. A confidence score of 0.73
means nothing to a user, and for most model setups it is not calibrated anyway. What
users can act on is a behavioral signal.

| Instead of | Show |
|---|---|
| A confidence percentage | "I could not find this in your documents" |
| A single answer, always | Two candidate answers when retrieval is split |
| Silent low confidence | A prompt to narrow the question |
| A hedged wall of text | The direct answer, plus what it depends on |

The strongest uncertainty signal is usually the absence of a source. If your system can
say "I found this in these three documents" when it is grounded, the grounded and
ungrounded cases already look different, and you never have to explain a score.

Do not fabricate certainty in the other direction either. A system that hedges
everything equally has told the user nothing, and they will learn to skip the hedge.

---

## 3. Citations that actually resolve

A citation is a promise the user can check. Three requirements, ordered by how often
they get broken.

1. **It resolves.** The link opens the thing. A citation to a document that does not
   exist is worse than no citation, because it manufactures trust.
2. **It points at the passage,** not the top of a 40-page PDF.
3. **It supports the specific claim.** The nastiest failure is a real document,
   correctly linked, that does not say what the answer says it says.

Measure this. Citation resolve rate and citation match rate are separate numbers, and
the second one catches confident nonsense. [Evals](../evals-deep-dive/) covers scoring
them, and the capstone reports both.

That has a design consequence. If you cannot cite, say so, rather than presenting an
uncited answer in the same visual style as a cited one.

---

## 4. Streaming, latency, and the feeling of speed

Streaming changes what users perceive and what your guardrails can do.

- **Stream for perceived latency.** First token is the number users feel. See
  [Inference Platform](../inference-platform-deep-dive/) on why TTFT and total time are
  different problems.
- **Do not stream text you might have to retract.** An output guard that runs after
  generation cannot unsay what the user already read.
  [Architecture](../architecture-deep-dive/) measures this directly: an output guard on
  a stream detected every violation and prevented none.
- **Show the stage, not a spinner.** "Searching your documents" then "Reading 4
  sources" then "Writing" sets expectations and makes a slow path feel deliberate.
- **Give long operations a way out.** A stop button, and a way to keep partial work.

Rules of thumb: under 300ms feels instant, under a second feels responsive, past
about ten seconds you need visible progress and an escape hatch.

---

## 5. Error, refusal, and empty states

These three get treated as one and should not be.

| State | What the user needs |
|---|---|
| **Error** (something broke) | That it is not their fault, and what to try |
| **Refusal** (the system will not) | Why, and what the boundary is |
| **Empty** (nothing found) | That the search worked and found nothing, plus how to widen |
| **Degraded** (fallback active) | That capability is reduced right now |

A refusal that reads like an error makes users retry the same thing. An empty result
that reads like a refusal makes them think they did something wrong. Silent degradation,
where the system answers worse because a provider is down and never mentions it, is the
one that costs you trust for good. Say it.

Write refusals as boundaries rather than accusations. "I cannot give medical advice.
Here is what I can help with" beats "Your request violates our policy."

---

## 6. Feedback that is worth collecting

Thumbs up and down are cheap to add and mostly useless on their own, because you get a
signal with nothing attached to it. Make feedback actionable.

- **Attach it to the trace,** not just the message id. You need the inputs, retrieved
  context, tool calls, and model version to do anything with it.
- **Ask one narrowing question** on negative feedback: wrong, incomplete, off-topic,
  or offensive. Four buttons beats a free-text box nobody fills in.
- **Close the loop visibly.** If feedback changes nothing the user can perceive, they
  stop giving it.
- **Watch the rate as a trend,** not the individual votes. A rising thumbs-down rate
  with no deploy is a quality incident. See
  [Observability](../observability-deep-dive/) and section 7 of
  [INCIDENTS.md](INCIDENTS.md).

Feedback is badly biased. People report offensive output far more than they report
subtly wrong output. The confidently wrong answers are the ones users never flag,
because they believed them.

---

## 7. Handoff to a human

For anything consequential, the exit to a human is a core feature.

- **Make it visible from the start,** not only after the user has failed three times.
- **Carry the context across.** Making someone re-explain to a human what they just
  explained to a bot is the single most reliable way to make the AI feature feel like
  an obstacle.
- **Be honest about wait times.** "A person will reply within a day" beats a queue that
  never moves and never says so.
- **Trigger it automatically** on repeated failure, detected distress, or any topic
  you have decided the system should not handle.

---

## 8. The appeal path, from the user's side

[GOVERNANCE.md](GOVERNANCE.md) defines the policy. This is what it has to look like
to the person affected.

- **On the decision, not buried in help.** If an output has consequences, the way to
  contest it belongs next to the output.
- **In plain words.** "Ask a person to review this" beats "Submit a reconsideration
  request."
- **Tell them what happens next,** including roughly when.
- **A human decides, and the interface should say so.** An appeal that visibly routes
  back to the same system is not an appeal.
- **Show the state.** Received, under review, decided. Silence reads as refusal.

If your appeal rate is near zero on a consequential system, treat it as a UX finding
before you treat it as good news.

---

## 9. Reversibility and consent for actions

The moment your system acts rather than answers, the interface carries new weight.
See [Agents](../agents-deep-dive/) and
[Agent Harnesses](../agent-harness-deep-dive/) for the mechanics behind these.

- **Preview before irreversible actions.** Show exactly what will happen, with the
  real values, not a summary of the intent.
- **Bind approval to one specific effect.** A blanket "allow this agent to send
  email" is not consent to the message it is about to send.
- **Prefer undo over confirm** where the action allows it. Confirmation dialogs are
  trained away within a week; undo survives.
- **Make the audit trail visible to the user,** not just to you. What did it do, when,
  on whose instruction.
- **Distinguish the drafted from the done.** The clearest AI action interfaces make
  "this is a draft you can edit" and "this has been sent" impossible to confuse.

---

## 10. A pre-launch UX checklist

Run this alongside the pre-deployment assessment in [GOVERNANCE.md](GOVERNANCE.md).

- [ ] The user can tell it is AI, at the point of use.
- [ ] A wrong answer looks different from a right one, without the user knowing the
      answer in advance.
- [ ] Citations resolve, point at passages, and support the claim. Both rates measured.
- [ ] "I do not know" is a designed state, not a failure of the happy path.
- [ ] Error, refusal, empty, and degraded are four distinct states with distinct copy.
- [ ] Nothing irreversible happens without a preview of the actual effect.
- [ ] There is an undo, or a documented reason there cannot be.
- [ ] A human handoff is visible before the user gets frustrated, and carries context.
- [ ] The appeal path sits next to any consequential output, in plain words.
- [ ] Negative feedback captures the trace and one narrowing question.
- [ ] Degraded mode is announced rather than silent.
- [ ] Someone who cannot see the interface can still use it, and screen readers are
      not defeated by streaming text that rewrites itself.

---

## 11. Anti-patterns

- **Confidence theatre.** A precise-looking score that is not calibrated. It buys trust
  the system cannot back up.
- **The infinite chat box.** A blank prompt with no affordances, shipped because it
  was easy, leaving users to guess the capability boundary.
- **Retracted streaming.** Text appears, then vanishes when a guard fires. The user
  read it.
- **Feedback into a void.** Collected, never surfaced, never acted on.
- **The dark-pattern default.** Data used for training unless the user finds a
  toggle. If consent matters, ask for it plainly.
- **Silent degradation.** Answering worse during an outage behind an interface that
  looks exactly as confident as usual.
- **Fake humanity.** Typing indicators, human names, and manufactured hesitation on a
  system that is not a person.

---

## Where to start

If you have shipped an AI feature and none of the above, do these three things.

1. **Design the "I do not know" state.** It is the highest-value hour of UX work in any
   AI product, and most teams have never done it.
2. **Check that your citations resolve.** Measure it rather than assuming it. The
   number is often worse than anyone expects.
3. **Put the human handoff where a frustrated person will find it,** which is earlier
   than you think.
