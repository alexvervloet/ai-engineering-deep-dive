# Authoring Lessons: writing teaching examples that don't lie

A runnable teaching example makes a promise: *"run this and you'll see X."* When the
output doesn't actually show X (or worse, shows the opposite) the reader either
gets quietly misled or loses trust. These are the principles we've learned for
keeping that promise, each one paid for by a real example that broke it.

The through-line: **the example is the argument.** Prose can claim anything; the
output is what the reader believes. So the output has to carry the lesson on its
own, honestly, every run.

---

## The principles

### 1. Make the example prove its own claim
If the headline says a technique helps, the *output* must visibly show it helping.
Re-read the takeaway, then look at what actually printed. If the run doesn't
demonstrate the claim, the example is broken, even if the code is "correct."

- **Hybrid retrieval (ex07)** claimed "hybrid is strictly better." On a paraphrase
  query a 50/50 blend ranked the right chunk *8th*, worse than vector-only's 1st.
- **Query transformation (ex10)** claimed HyDE "pulls the right chunk up the
  ranking." The default query already retrieved the answer at rank 1, so there was
  nothing to pull up.
- **Contextual retrieval (ex11)** claimed a big win, but plain and contextual chunks
  returned the *identical* top-3.

Three examples, same failure: a true-sounding sentence the output didn't back.

### 2. Verify the narrative against a real run, every sentence
Write the prose *after* you've run it, and make each concrete claim match the actual
numbers. "Watch it climb from direct to HyDE" is a lie if, on some runs, it doesn't
climb. Cite numbers you've actually seen.

### 3. Anchor on the reliable signal, not the wobbly one
Anything touching an LLM call is non-deterministic; rankings on a small corpus wobble
run to run. Build the lesson on what's *stable*.

- **ex10:** HyDE reliably ~doubled the answer's similarity score (~0.38 → ~0.78)
  every run, but its *rank* moved (3→2 one run, 3→1 the next). The takeaway was
  rewritten around the score lift, with an explicit note that ranks wobble.

### 4. Show the tradeoff, not "X is strictly better"
Real techniques have failure modes. Teaching the nuance ("a tool to tune, not a free
lunch") beats a tidy heuristic that falls apart the first time a learner hits the
exception. And when the concept *is* a tradeoff, don't just describe it: make the
dial runnable, so the reader moves it and watches each failure mode happen.

- **ex07** became an honest mini-tour of fusion: a 50/50 blend that *demotes* the
  answer, RRF that helps but can't fully undo a bad keyword rank, and a
  vector-weighted blend that recovers #1, with the weight labeled as tuned-to-
  illustrate, not universal.
- **Alerting (observability ex05):** the false-alarm↔detection-lag tradeoff is a
  knob the reader turns: `persistence=1` catches a one-day spike, `persistence=3`
  rides over it; EXERCISES has them drop `z_threshold` to 1.5 and watch alerts
  appear on a *healthy* history. Reading "there's a tradeoff" convinces no one;
  getting paged on noise because you tightened the dial does.

### 5. Build a corpus that isolates the phenomenon
If a technique's benefit won't reproduce on your general corpus, don't force it or
overclaim: build a small, inline corpus that isolates exactly the effect. Modern
embeddings are strong enough that many "technique X helps" demos simply won't show a
difference on well-written docs.

- **ex11:** contextual retrieval only visibly wins on *disambiguation*: several
  near-identical chunks differing only by an entity the text never names (Anthropic's
  "which company's revenue?" case). We gave ex11 its own three-plan mini-corpus where
  each "the cap is X" fact names neither its plan nor "storage." Plain retrieval
  returns the *wrong* plan's cap at #1; contextual fixes it. On the self-contained
  main corpus, plain retrieval already nailed everything and the lesson vanished.

### 6. Presentation can lie too
A misleading *display* fails the reader as surely as a wrong result. Two we hit:

- **Relative vs absolute scores.** Min-max normalizing to make scores comparable
  forces the top result to `1.000` *by construction*. Printed bare, `1.000` reads as
  "perfect match" when it only means "best of this list." Fix: label it `rel` and
  print the raw score beside it (`rel 1.000 (cos 0.32)` makes the weak match obvious).
- **Previews that show the wrong words.** Printing a chunk's first N characters
  advertises whatever the chunk happens to start with, often the wrong topic (a
  fixed-size chunk that answers "how do I export?" opened on an unrelated import-error
  code). Fix: center the preview on where the query actually matched
  (`rag.snippet`, in [rag/preview.py](rag-deep-dive/rag/preview.py)); fall back to the
  start only when nothing matches.

### 7. Match the tool to the structure of the data
A blind fixed-size word window cuts wherever the count runs out, gluing the tail of
one topic onto the head of the next. Structured docs (Markdown, HTML, PDFs with
headings) chunk far better on their *own* boundaries: one topic per chunk, a heading
to cite, no accidental topic-mixing.

- **ex07/ex13:** a 120-word window merged a doc's "Importing" and "Exporting"
  sections into one chunk, so retrieval returned a chunk whose first sentence was
  off-topic and whose keyword profile was muddied.
  `rag.chunk_markdown_sections` splits on headings instead.

### 8. When the wobble *is* the lesson, keep it and name it: don't engineer it away
Principle 3 says anchor away from the wobbly signal. But sometimes the unreliable
result is a genuine property of the technique the example is teaching; hiding it
would itself be a lie. When an apparent "the output didn't prove the claim" is
actually the technique's real failure mode, keep the case and call it out in the
output, turning the surprise into a second lesson.

- **Faithfulness judge (evals ex13):** the "Does the Pro plan include SSO?" row
  gives the *loose* prompt a 5/5 faithfulness score even though the context never
  mentions SSO, superficially contradicting the "loose invents ungrounded answers"
  headline. It's not a scorer bug: the cheap judge (Haiku, verified deterministic at
  temp=0) treats "No, it doesn't include SSO" (an inference from *silence*) as
  faithful, disagreeing with the rubric's intent that silence ≠ evidence of absence.
  The other three cases ask for a specific fact, so a loose answer either invents a
  concrete detail (clearly ungrounded) or hedges (clearly grounded): unambiguous.
  Only the yes/no question produces the hard negation-from-omission call. We kept the
  row and added a printed callout tying it to the judge-unreliability theme (ex08):
  the judge applies its own read of the rubric, so calibrate against human labels
  before trusting its numbers.

### 9. When you compare two systems with a judge, hold the judge constant
An LLM judge is *measurement infrastructure*, not part of the system under test. Swap
the answerer **and** the judge between two runs and a correctness delta could be
either one moving; the comparison means nothing. Pin the judge to one fixed model
across both runs; vary only the thing you're actually measuring.

- **Capstone local-vs-cloud (ext-local):** the local run answers with a local Qwen,
  but the eval's `JUDGE_PROVIDER` override keeps the *same* gpt-4o-mini judge the
  cloud baseline used. That's what lets the +0.072 correctness read as "the local
  answerer is better here," not "a more generous grader showed up." Without the pin,
  `PROVIDER=local` would have had Qwen grading its own answers: circular.

### 10. Before you report a metric delta, find out what moved the number
A dropped metric invites a tidy conclusion ("the small model can't cite"). Open the
failing cases *first*; the real cause is usually narrower, and more honest, than the
headline the number suggests. Reporting the raw delta without the diagnosis can libel
the system.

- **Capstone local-vs-cloud:** local citation-resolve fell 0.95 → 0.78, which reads
  as "ungrounded answers." But of the 14 answers that failed the strict `(path:line)`
  parse, **11 cited real sources**, just grouped as `(a.md:4, b.md:51)` instead of
  one-per-paren; only 3 were truly ungrounded. The gap is citation *format
  compliance*, not grounding. The honest writeup says so; the raw number alone would
  have lied about the model.

### 11. A generality claim needs more than one confirming run: vary the instance
"Works with *any* X" is a far stronger promise than "works with the X I tried." One
passing example verifies the specific case, not the generality; a reader will plug in
an X different enough to break it. Before you claim breadth, run the cases most likely
to *falsify* it (the awkward, the adversarially different) not a second variation of
the one that already worked.

- **Capstone ext-local ("any OpenAI-compatible runner"):** the local backend was
  verified on Ollama + qwen3:8b, which answered cleanly; the "any runner" claim
  looked safe. It would have been a lie for a reader on a *thinking* model: qwen3.6 on
  LM Studio (another machine) spent the entire token budget *reasoning* and returned a
  blank answer, a code gap the first setup couldn't surface. Testing a deliberately
  different second instance (thinking model, non-Ollama runner, remote box) is what
  turned an assumed generality into a real one, with a `LOCAL_MAX_TOKENS` fix and a
  documented caveat instead of a false universal.

### 12. In a multi-stage system, let the metric that moved name the stage that broke, and measure your own predictions
A pipeline has more than one place a regression can come from (retrieve → answer). Don't
pin the blame on the component you happened to be thinking about; read *which metric*
moved. Correctness and retrieval-hit are separate instruments: a fall in one and not
the other localizes the cause. And when an earlier writeup floats a prediction, actually
run it: a refuted prediction, reported, teaches more than a tidy confirmation, and a
confirming run you never did is just a guess in a table.

- **Capstone local (35B on a remote box):** an earlier note predicted "a bigger local
  model would close the citation gap; measure it, don't assume it." So we did, on
  qwen3.6-35b (vs the 8b), same constant judge. It **didn't**: judged correctness only
  *tied* cloud (0.786, within judge noise), not the win its size implied. And retrieval
  hit@k was the *only* metric that fell (0.886 -> 0.829): the one thing changed on the
  retrieval side was the 0.6B embedder. So the weak link was the **embedder, not the
  bigger answerer**: on a local RAG stack, spend the upgrade on the embedding model
  before the generator. The size prediction was published as refuted, not quietly
  dropped: the surprise *is* the lesson.

### 13. When the lesson is *detection*, keep the ground truth out of the data
Principles 1–12 assume the example computes one thing you then check. But when the
skill is *inferring* something from indirect signals (drift, a quality regression,
an anomaly) the synthetic data you generate must contain only what a real system
would observe, never the answer. Leak the label into the record and the learner's
detector *reads* it instead of *inferring* it; the example proves nothing. Keep the
truth as a **private answer key**, separate from the data, and use it only to grade
the detector: exactly the thing production never hands you.

- **Observability simulator:** `generate()` returns realistic logs (question,
  latency, cost, whether it refused, but no "was this answer good?" field) *and*,
  separately, the ground-truth incident schedule. Every metric and detector reads
  only the logs; the schedule exists solely so the capstone can score "you flagged
  drift on day 16; it actually started on day 14, a 2-day lag." A `quality=0.6` field
  in the log would have made the whole repo trivial and fake.

### 14. In generated data, make the signal a real consequence, not a stamped-in value
The synthetic-data form of "prove its own claim" (§1): whatever the detector picks up
must fall out of a *genuine change in the simulated behavior*, not a number you wrote
in to move the chart. Inject an incident by changing what the system **does** (worse
answers, more refusals, slower calls, bigger prompts) and let the metric move because
reality moved. A detector that only "works" because you fed it the answer teaches
nothing, and it breaks the moment the reader swaps the mock for the real thing.

- **Quality regression:** rather than marking some days "bad," the simulator makes
  answers genuinely terser and more evasive during the window, so the sampled judge
  scores them lower *because they are worse*. Swap the mock rule-based judge for a
  real LLM-as-judge and the same dip appears: the degradation lives in the text, not
  in a hidden flag. Same for cost creep (real extra prompt tokens) and the cohort
  outage (real added latency), so every alert fires off a real cause.

### 15. If the honest demonstration won't reproduce, change the instance: don't rig the detector
A concept can be real while the specific instance you picked to show it doesn't
actually exhibit it. The fix is to find the instance that genuinely does, verified by
measurement, across seeds, not to tune thresholds until the wrong instance appears to
work. A detector loosened until a staged effect shows up is a lie that happens to
compile, and it collapses the first time a reader points it at their own data.

- **Segmentation ("the aggregate hides it"):** the first draft hid a cohort
  *error-rate* spike inside the global average, but measured, it didn't hide. Error
  rate has near-zero baseline variance, so even a small global bump is many sigma and
  the global detector fires anyway. Instead of loosening the global threshold to
  *force* "it hides," the incident was switched to a cohort *latency* regression,
  which genuinely disappears into the noisy global p95 (z≈1.8, no alert) while the
  affected cohort's own p95 triples and screams. The lesson survives because the
  phenomenon is real, not staged, and the switch was driven by a measurement, not a
  guess.

### 16. A guardrail demo can fire correctly and still teach the wrong thing
Showing a filter *trigger* is not the same as showing what it's *for*. An output guard
that visibly redacts something has "worked" on screen; but if it scrubbed a value that
belonged in the answer, the reader learns the wrong lesson about the feature. Make the
example remove what genuinely doesn't belong, and keep what does.

- **ai-in-production ex08 (output PII guard):** the capstone claimed "an answer with PII
  → redacted," but the fourth question produced no PII, so the guard ran and did nothing
  the one layer that turn existed to show never fired (a §1/§2 miss). The first fix
  made it fire, but on the app's *own* `support@acme.example`: redacting the help-desk
  address the answer was trying to hand the customer, the exact "scrubbing your own
  support email is worse than useless" anti-pattern the guard's allowlist exists to
  prevent. It demonstrated the mechanism while inverting the point. The honest fix leaks
  a *third-party* customer's email (`sam.rivera@gmail.com`): PII with no business in the
  answer, so redaction removes the leak and the rest survives. And the tradeoff is real,
  not hypothetical: told to "remove PII," both gpt-4o-mini and claude-haiku stripped the
  *wanted* `support@acme.example` too (same over-redaction as a blunt regex), so any
  redactor, LLM or rules, needs an allowlist / keep-rules, never "just ask the model."

### 17. A rounded metric ties, and the tie-break will quietly name a winner
When a decision takes a max or a top-1 over values that have been rounded, bucketed, or
truncated, ties are the common case, not the edge case. Something still has to return
one answer, so the sort order picks one, and the example reports it as *the* result. The
reader has no way to see that three other candidates were level with it, or that the
winner was the weakest of them. Return everything that reached the top; if you still
want one name, rank it by the *unrounded* value.

- **Inference platform ex12 / capstone:** fleet size is the max of prefill, decode,
  concurrency, and a replica floor, each rounded up to whole replicas. In the capstone
  all four landed on 2, and the alphabetical tie-break reported "request concurrency",
  which had the *most* slack of the four (1.08 raw against decode's 1.77). The capstone's
  headline line, the one naming what binds the fleet, was an artifact of sorting. Two
  fixes, and both were needed: the planner now returns every binding dimension and ranks
  by raw demand, *and* the fixture was changed so one dimension genuinely binds. The
  first alone would have produced an honest report that nothing binds except the floor,
  which is true but is not the lesson chapter 12 is there to teach.

### 18. Check that the capstone obeys the rule its own chapters teach
An integrated capstone reimplements, in glue code, decisions the chapters made carefully
in isolation. That glue is where a rule quietly gets dropped: a value restated instead of
passed through, a stage handed a number that skips a term the previous stage computed.
Nothing fails, because the fixture has slack, and the flagship artifact ends up
demonstrating the mistake the course exists to prevent. Derive every downstream input
from the upstream decision object, and add a counterfactual sized to sit *between* the
right number and the wrong one.

- **Inference platform capstone:** chapter 22.2 exists to say that weight fit is not
  service fit, because the KV cache grows with live tokens. The capstone described the
  model twice, once for the memory check and once inline for the layout planner, and then
  reserved GPUs using weights plus a runtime constant, dropping the KV reservation it had
  computed one line earlier. Every test passed: the GPUs had 40 GiB and the true
  requirement was 34.75. The tell was two different runtime-overhead constants for one
  physical quantity. The fix that makes it stay fixed is not the corrected number, it is
  the counterfactual: inventory sized between weights-and-runtime and the full footprint,
  which fails loudly if anyone drops the term again.

---

## Case studies

Each is a symptom the reader would notice, its real diagnosis, and the fix.

| Example | Symptom | Diagnosis | Fix |
|---------|---------|-----------|-----|
| **07: hybrid** | 50/50 hybrid ranked the answer worse than vector-only | Keyword search was *confidently wrong* on a paraphrase (answer says "export," query doesn't); naive blending inherited the mistake | Rewrote as an honest fusion tour (50/50 → RRF → vector-weighted); reframed "strictly better" as a tradeoff |
| **10: query transformation** | No visible difference; nonsense preview | Default query already ranked the answer #1; answer buried mid-chunk so the preview showed the wrong sentence | Heading-aware chunks + an oblique query where direct genuinely fails; narrative anchored on the reliable score lift |
| **11: contextual retrieval** | Plain and contextual returned identical results | Main corpus is too self-contained to be under-specified; strong embeddings already nail it | Inline three-plan mini-corpus isolating the disambiguation case |
| **13: chunking** | (new lesson) fixed-size merges two topics | A word-window ignores document structure | `chunk_markdown_sections`; shown as the fix for the ex07 merge |
| **all previews** | preview text unrelated to the question | Showed the chunk's first N chars, not the match | `rag.snippet`: keyword-in-context, shared across examples |
| **evals 13: faithfulness** | loose prompt scores 5/5 on the SSO question despite no context support | Not a bug: the cheap judge deterministically treats negation-from-omission ("no SSO" inferred from silence) as faithful, against the rubric's intent | Kept the row; added a printed callout framing it as live judge unreliability (ties to ex08); calibrate against human labels |
| **capstone: local vs cloud** | local citation metrics dropped sharply | 11 of 14 "failures" cited real sources in a grouped format the strict parser rejects (only 3 ungrounded); and a swapped judge would have confounded the correctness delta | Pinned the judge constant across runs; reported the gap as format-compliance + latency, not accuracy |
| **capstone: ext-local generality** | "works with any OpenAI-compatible runner" held on Ollama/qwen3:8b | a thinking model (qwen3.6 on LM Studio, another machine) returned blank: reasoning consumed the whole token budget; invisible on the first setup | Tested a deliberately different second runner+model; added the `LOCAL_MAX_TOKENS` fix and bounded the claim with the caveat |
| **capstone: 35B remote eval** | a bigger local model was predicted to beat the 8b / close the gap | it only *tied* cloud on correctness; hit@k was the sole metric that fell (0.886→0.829), isolating the 0.6B embedder (not the strong answerer) as the weak link | Published the refuted prediction; lesson: on a local RAG stack, upgrade the embedder before the generator |
| **observability: simulator** | how do you teach *detecting* drift when logs have no "was this good?" label? | that's the real problem: a synthetic env that leaks the label makes the detector read the answer, not infer it | Emit realistic logs only; keep the incident schedule as a private answer key used to grade the detector (lag, catch/miss) |
| **observability: segmentation** | the intended "a cohort problem hides in the global average" didn't hide | error rate has ~zero baseline variance, so even a small global bump is many sigma, so the global detector fired | Measured, then switched the incident from cohort error rate to cohort *latency*, which genuinely vanishes into the noisy global p95; didn't loosen the threshold to fake it |
| **ai-in-production 08: output PII guard** | example "redacts PII" but the guard fired on nothing, then, once "fixed," on the app's own support email | the claimed layer never triggered (no PII on the path); the first fix redacted a *wanted* value, inverting what the guard is for | Leak a *third-party* email so redaction removes what doesn't belong; verified LLM redactors over-redact too (strip the wanted address); pair any redactor with an allowlist |

---

## A checklist for a new example

1. **Run it before writing the prose.** Read the actual output first.
2. **Does the output visibly prove the headline?** If not, fix the example, not the wording.
3. **Is every concrete claim true of the run you just did?** Numbers, ranks, "watch X happen."
4. **If it calls an LLM, is the lesson built on the stable signal?** Note what wobbles.
5. **Are you showing the honest tradeoff,** or a heuristic that breaks on the first exception?
6. **Is the display honest?** Relative scores labeled as such; previews centered on the match.
7. **If the effect won't reproduce,** isolate it in a tiny purpose-built corpus, or, if you measured that this instance genuinely doesn't show the effect, switch to one that does; don't rig a threshold to fake it.
8. **If you're teaching detection/inference,** is the ground-truth label *out* of the observable data, and does the signal come from a real simulated change rather than a stamped-in value?
9. **If you're demoing a guardrail/filter,** does it remove what genuinely doesn't belong, not a value that should stay? A filter firing on screen isn't proof it's doing its job.
10. **If a decision takes a max or top-1 over rounded values,** does the output show everything that tied, and is the named winner ranked by the unrounded number?
11. **If it's an integrated capstone,** does each stage take its inputs from the previous stage's output rather than restating them, and is there a counterfactual sized between the right number and the plausible wrong one?

---

*These lessons came out of hardening the RAG and evals deep dives' examples, building
the capstone that exercises all of them, building the observability dive on a
synthetic-log environment (which added the detection-specific principles 13–15),
hardening the ai-in-production dive's guardrail examples (principle 16), and auditing
the inference platform dive after it was finished, which is where the two
arithmetic-and-glue principles (17–18) came from. They generalize to any runnable
teaching material: the reader believes the output, so the output has to be worth
believing.*
