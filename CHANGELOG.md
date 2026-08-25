# Changelog

Notable changes to the AI Engineering: Deep Dives series, newest first.

Each entry records what changed and, where it matters, why. Changes inside a
submodule are listed under that submodule's name; the submodule's own history
has the per-file detail.

Format loosely follows [Keep a Changelog](https://keepachangelog.com). This
series is not versioned, so entries are grouped by date instead of release.

---

## 2026-08-25: ML foundations becomes the 25th deep dive

The API courses showed what to send a model. Fine-tuning, local models, and inference
platforms assumed the reader could reason about what happened underneath. The new
course fills that gap without turning the series into an ML degree.

### Added

- **[ML Foundations for AI Engineers](ml-foundations-for-ai-engineers/).** Eleven
  offline NumPy and PyTorch lessons cover tensor shapes, stable softmax,
  cross-entropy, gradient checks and descent, causal attention, a transformer block,
  sampling, held-out calibration, quantization error, and named training and
  inference memory components.
- **A deterministic tiny-transformer capstone.** It trains on one cyclic rule, keeps
  train, calibration, and test identities separate, reconstructs weights through
  logical int8, measures held-out logit drift, and derives its verdict from four
  requirements declared apart from the observations.
- **Forty-five tests and a two-runtime CI matrix.** The suite runs on Python 3.12 and
  3.14 with NumPy 2.5.2 and CPU-only PyTorch 2.13.0. It also runs under optimized
  Python locally, executes every lesson with warnings as errors, compares two
  capstone reports, and runs CodeQL.
- **Chapter 24 and the parent routes.** The series map, textbook, decision guide,
  glossary, career map, responsibility guide, offline manifest, and social cards now
  point to the course.

### Fixed during review

- An alternating-pair capstone corpus made its first target unknowable and its quality
  requirements impossible. Held-out rotations of one deterministic cycle replaced it.
- A KV-memory mutation survived a pure doubling check because zero also doubles to
  zero. The test now anchors 40 fp16 elements to an independent 80-byte expectation.
- The original package floor claimed Python 3.11 while NumPy 2.5 had dropped it. The
  course and its minimum CI cell now start at Python 3.12.

## 2026-08-23: rag-deep-dive gains a real Postgres/pgvector path

The RAG dive taught retrieval with an in-memory store cached to a JSON file, which
is the right shape for learning the search and the wrong shape for everything
around it. A cache file has one verb, rebuild everything, so the dive never showed
what an index costs to keep, which is where the money and most of the bugs are.

### Added

- **A real vector store with a real lifecycle.** `rag/pgstore.py` runs the same
  pipeline against Postgres with pgvector: incremental sync by content hash,
  deletes that cascade to their vectors, one transaction per change, an HNSW index,
  and a recorded embedding-model id so a model switch is caught rather than obeyed.
  Retrieval is unchanged, since `1 - (embedding <=> query)` is the cosine
  similarity the from-scratch store computes by hand.
- **`examples/16_pgvector_lifecycle.py`**, which walks six lifecycle events and
  prints what each one costs. The second sync of an unchanged corpus embeds 0
  chunks; editing one document of four embeds 3 of 12.
- **`compose.yaml`** pinning pgvector 0.8.6 on Postgres 18, and
  `requirements-postgres.txt` for the optional driver. Everything else in the dive
  still runs with no Docker and no database.
- **`--store pg` on the capstone**, so `ask_docs.py` answers from the database with
  the same code that answers from the cache.
- Section 12 of the README, its exercises, a chapter section in `TEXTBOOK.md`, and
  the dive's first `LESSONS.md`.

### Changed

- The pipeline is typed against a `SupportsSearch` protocol rather than the
  concrete `VectorStore`. That puts the repo's central claim into the type system.
  Retrieval does not care where the vectors live.

### Fixed

A review of the above found four defects in one family: a sync that reported
success while leaving the index wrong, and stored hashes that then agreed there
was nothing left to do. All are closed, and `tests/test_pgstore.py` (14 tests,
no API calls, skipped without a database) now asserts each one; nine of them
fail against the code as first written.

- **A document emptied upstream keeps nothing.** The write loop skipped any
  document that produced no chunks, so emptying a page left its old chunks
  retrievable and its hash unadvanced, which made every later sync re-report the
  same edit and do nothing about it.
- **The table rebuild is inside the transaction it belongs to.** Its DDL was
  committed first, so a crash in between left an empty chunk table beside a full
  document table whose hashes all read "unchanged": a permanently empty index
  that no later sync would repair. Postgres does DDL transactionally.
- **A model narrowed under the same name is caught.** The dimension comparison
  was unreachable, because the caller built the object it compared against with
  the stored width copied in. OpenAI's `dimensions=` is exactly this case. A
  rebuild discovered after embedding now re-embeds the whole corpus rather than
  writing only the documents that happened to change, which had been dropping
  the rest of the index while reporting a successful rebuild.
- **`RAG_DATABASE_URL` in `.env` reaches the capstone.** It was read as an
  argparse default, which is evaluated before `load_dotenv()`, so the flag fell
  back to the compose service and a run against the wrong database looked fine.

---

## 2026-08-23: evals-deep-dive decision-statistics audit follow-ups

An audit of the decision-statistics work found one real coverage defect, one
docstring that its own tests contradicted, and a set of narration and
cross-reference gaps. All are closed.

### Fixed

- **A sequential look can no longer be smaller than its own approximation
  allows.** The guard required two pairs, but a nominal 95% normal interval covers
  about 70% at two pairs, 88% at five, and 94% at twenty. A module whose subject is
  spending a declared error budget could therefore overspend it sixfold while still
  printing the declared number. Looks now start at 30 pairs, and the README and
  chapter say why.
- **`classify_effect` documents the classification it performs.** The docstring
  promised that any interval inside the equivalence band supports equivalence, while
  the code reported the directional state first, and the test table (written from the
  code) had frozen the contradiction. The priority order, the reservation of
  `practically_equivalent` for intervals containing zero, and the deliberate
  strict-versus-inclusive boundary asymmetry are now stated and pinned by tests.
- **The lesson derives its release verdict instead of narrating it.** Example 14
  printed a fixed "HOLD" and a literal "+3.00 pp" beside a separately computed
  evidence state; the CI determinism check compares two runs to each other and so
  could never detect the two disagreeing.

### Changed

- Evidence states are named after their values (`STATISTICAL_IMPROVEMENT_ONLY`,
  `STATISTICAL_REGRESSION_ONLY`), so `EffectEvidence(value)` round-trips.
- Example 14 explains why its fixed-horizon section spends alpha/4 while the
  sequential campaign spends alpha/16, and notes that the paired interval is the
  narrower one despite being held to a stricter confidence level.
- Parent glossary entries for the decision vocabulary point at sections that exist;
  they had cited a chapter subsection number using the notation every neighbouring
  entry uses for README sections.
- Em-dashes and typographic quotes are out of the new files, matching the rest of
  the series.

---

## 2026-08-22: evals-deep-dive decision statistics

The Evals dive now carries a release decision from paired observations to an
explicit hold, ship, or harm signal without treating every detectable change as
useful.

### Added

- Paired bootstrap intervals that preserve shared case difficulty and reject
  unequal or invalid observations instead of silently truncating them.
- Prospective power and minimum-detectable-effect planning, practical-effect
  classification, family-wise error controls, and conservative planned sequential
  looks.
- A deterministic offline lesson, 16 regression tests including optimized-Python
  execution, and CI across the documented minimum and current Python versions.

### Changed

- Earlier fixed-horizon independent-sample comparisons now call themselves
  screening approximations rather than release evidence.
- Parent glossary, career guidance, responsibility checklist, and recursive offline
  verifier now teach and enforce the decision-statistics path.

---

## 2026-08-21: agents-deep-dive contract audit follow-ups

Successive audits of the tool-contract work found correctness gaps at adoption,
replay, configuration, approval, trace propagation, and protocol boundaries. All
are closed.

### Fixed

- **A settled idempotency key now binds to its payload.** Repeating a mutating
  call ID with different arguments returned the stored result and recorded the
  *first* call's digest against the second attempt, so the audit trail showed no
  sign it happened. That case is now denied as `idempotency_key_reuse`, and the
  honest retry still replays.
- **Discovered tool schemas can enter the loop again.** Requiring
  `additionalProperties: false` made every third-party MCP tool unusable:
  `ToolExecutor` raised before any model call, while the docs still promised such
  tools drop in unchanged. `seal_schema()` closes a copy at the point of adoption,
  the MCP client applies it to every descriptor, and the tradeoff (a sealed schema
  rejects calls an under-declaring server would accept) is stated rather than
  hidden.
- **A reusable executor cannot silently lose replay scope.** Passing `executor=`
  without its trusted `context=` now fails before any provider call. Tests cover
  the omitted, context-only, invalid executor-only, and fully paired modes.
- **Approval progress is no longer an overloaded Boolean.** Outcomes and steps
  distinguish `not_reached`, `not_required`, `required`, `approved`, `denied`, and
  approval-system `error`, so an early policy rejection cannot look like a human
  denial.
- **The teaching MCP client keeps its transport invariant under `python -O`.** A
  missing stdio stream raises explicitly, with a regression test for that branch.
- `--yes` in the capstone printed a bare tool line, because rich read
  `[auto-approved]` as markup.

### Changed

- The observability lesson is now deterministic and offline. A real dispatch plus
  replay visibly expose status, explicit approval state, replay state, and both
  argument and output digests while proving only one effect reached the sink.
- The MCP chapter teaches the contract in both directions: the client seals what
  it adopts, the server distrusts its clients. Neither end can verify the other
  checked.
- Stale claims corrected: the loop's "~20 lines", the toolbox docstring's account
  of approval and mutation, the offline example list in the setup check, and the
  going-further pattern count.

---

## 2026-08-21: agents-deep-dive tool contracts

The Agents dive previously explained that the model only requests a tool, but its
main and streaming loops dispatched those requests directly to Python. This update
makes the proposal-to-effect gap an executable contract rather than a warning.

### Added

- **A reusable local execution boundary** that rejects forged trusted context,
  validates Draft 2020-12 schemas, authorizes authenticated roles, fails closed on
  approval, injects tenant and subject data, bounds time and UTF-8 output bytes,
  and records structured outcomes with content digests.
- **Bounded replay protection for mutating calls.** Every post-dispatch outcome is
  retained within the process so a repeated timeout or after-commit error cannot
  duplicate an uncertain effect. The lesson explicitly names the production gap:
  durable, transactional sink idempotency and cross-worker coordination.
- **Offline example 18 and 14 tests** covering every declared schema constraint,
  trusted-context forgery, independent role and approval decisions, replay scope
  and eviction, after-commit failure, timeout, multibyte output bounds, audit
  provenance, malformed provider JSON, the main loop, and MCP dispatch.
- **Provider and delivery enforcement:** compatible OpenAI schemas advertise strict
  mode as defense in depth, every client-executed path uses the local executor, and
  a Python 3.10/3.14 CI matrix runs tests in normal and optimized mode plus all
  offline lessons.

### Notes

The migration found two older custom tools whose schemas were open to undeclared
properties and three teaching paths that bypassed the main loop. Those findings and
the thread-timeout, in-process replay, eviction, and concurrency simplifications are
now documented instead of left implicit.

---

## 2026-08-20: operational documentation

GenAI Security, Testing & Delivery, and RESPONSIBILITY.md each covered part of what
happens after a system is real. What was missing was the concrete layer: the forms
you fill in, the runbook you follow while tired, and the interface the person on the
other side actually sees.

### Added

- **[GOVERNANCE.md](docs/GOVERNANCE.md)**, the decision record. Named roles and who signs
  what, a change classification that keeps review from becoming noise, and
  copy-pasteable templates for a system register entry, a pre-deployment assessment,
  a risk register entry, a vendor and model assessment, and an appeal and redress
  record. Its one idea is that governance is a record of decisions, not a committee,
  and its most useful line is the reversal condition written before you have an
  incentive to argue.
- **[INCIDENTS.md](docs/INCIDENTS.md)**, the runbooks. A severity ladder with two rules
  that settle 2am arguments, the first thirty minutes in order, the containment
  levers that have to exist before you need them, and seven runbooks: injection
  reaching a tool, PII in output, harmful output, silent quality regression, cost
  blowout, provider outage, and corpus poisoning. Ends with comms templates and a
  postmortem template whose "what we are not doing" section stops the same debate
  recurring.
- **[AI-UX.md](docs/AI-UX.md)**, the interface as part of the safety system. Built on one
  test: can the user tell a good answer from a bad one without already knowing the
  answer? Covers disclosure, uncertainty that is behavioral rather than a number,
  citations that resolve and support the claim, why an output guard on a stream
  detects everything and prevents nothing, four distinct failure states that are
  usually collapsed into one, feedback worth collecting, human handoff, and
  reversibility for systems that act.
- **Cross-references** in the series map, textbook intro, decision guide, and both
  SAFETY.md and RESPONSIBILITY.md, which now point onward to the operational layer.

### Notes

The three pages are deliberately template-heavy. A governance process nobody finishes
governs nothing, so every template is short enough to complete in an afternoon. Where
a page makes a claim, it names the dive that proves it rather than asserting it.

---

## 2026-08-20: testing-and-delivery-deep-dive, chapter 23

Evals answer whether the application is good enough. Production answers what the
runtime around a model call must do. This chapter answers the question that sits
between them and is usually settled by vibes. Does this exact build qualify for
promotion, and can you take it back if it does not?

### Added

- **`testing-and-delivery-deep-dive/`**, offline start to finish: 12 decision modules,
  12 predict-then-run lessons, EXERCISES, Chapter 23 of the textbook, 87 tests, and a
  release-evidence capstone that emits deterministic JSON. Standard library only. No
  API key, cloud account, deployment target, or network after installation.
- **Test mechanics:** evidence portfolios chosen by failure mode, SDK contracts kept
  separate from recorded fixtures, seeded property tests with bounded shrinking that
  admits when it did not finish, deterministic doubles with explicit state bounds, and
  load evidence derived in named units from request events.
- **Delivery mechanics:** after-commit faults and idempotency under repeated lost
  responses, the artifact tuple as the unit of compatibility, PEP 751 `pylock.toml`
  auditing, a CI matrix that executes the support promise rather than declaring it,
  security findings judged by an independent severity policy, staged shadow and canary
  rollout with verified rollback, and evidence bound to a candidate digest and revision.
- **A non-vacuous release contract.** Policy, candidate artifacts, and stimuli are
  three separate inputs everywhere. Eight adversarial capstone scenarios remove a CI
  cell, delete a fixture field, change the index schema, drop idempotency, break the
  clamp property, inject an advisory, regress the canary, and age the evidence out.
  Each flips the final decision without rewriting the requirement.
- **Cross-references** in the series map, textbook, decision guide, careers map,
  glossary, and responsible-engineering ownership view.

### Notes

A post-build audit ran the suite, every example, the capstone twice for byte equality,
and fifteen seeded mutations against the modules. Thirteen mutations were caught; the
two survivors were behaviors the textbook asserts but no test pinned, and both now have
tests. The audit also found the load lesson printing "same measurements" above two
visibly different floats, and a scripted after-commit fault that the idempotent
deduplication path consumed without raising. Both are fixed, and all four findings are
recorded in the dive's
[LESSONS.md](testing-and-delivery-deep-dive/LESSONS.md).

---

## 2026-08-19: inference-platform-deep-dive, chapter 22

The Local Models dive ends at running open weights. This chapter starts where that
leaves off: turning model execution into a fleet whose latency, throughput, overload,
rollout, and cost behavior follows explicit evidence rather than a GPU count.

### Added

- **`inference-platform-deep-dive/`**, offline start to finish: 12 substantive decision
  modules, 12 isolated runnable lessons, EXERCISES, Chapter 22 of the textbook, 58
  tests, and an integrated fleet planner that emits deterministic JSON. It requires no
  GPU, model, API key, or network after installation.
- **Memory and execution mechanics:** weight/KV/runtime fit, TTFT/TPOT/E2E and token
  throughput, continuous batching, exact scoped prefix caching, measured quantization,
  and speculative decoding whose real acceptance must repay verification.
- **Fleet mechanics:** tensor/pipeline/data/expert parallel planning, pre-allocation
  admission and bounded shedding, capability/topology/residency-aware GPU placement,
  queued-token autoscaling with warmup semantics, independent canary gates, and
  burst/headroom/cost capacity planning.
- **A non-vacuous release contract.** Workload/control requirements are declared
  separately from stimuli and decisions. Counterfactual tests delete a required
  workload, shrink inventory, regress canary TPOT, and bypass shedding; each removes
  evidence without rewriting the requirement. Benign work traverses real admission and
  placement paths, and every primary decision reports the exact reason that decided it.
- **Cross-references** in the series map, textbook, decision guide, careers map,
  glossary, and responsible-engineering footprint view.

### Notes

The build's [LESSONS.md](inference-platform-deep-dive/LESSONS.md) records four concrete
authoring failures caught during verification: two fixtures that never reached their
intended capacity boundary, a tuple-vs-substring assertion that obscured decision
evidence, and the difference between source-tree verification and installing into a
bare Python 3.13 virtual environment without its declared build backend.

## 2026-08-18: genai-security-deep-dive, chapter 20

The [Prompt Injection](prompt-injection-deep-dive/) dive covers one attack on one
place, the text the model reads. Everything else a production system is made of,
identities, tools, build artifacts, retrieval indexes, interpreters, networks, and
budgets, can fail without a single crafted prompt. This dive is that larger system.

### Added

- **`genai-security-deep-dive/`**, offline start to finish: 13 modules under
  `genai_security/`, 12 narrated lessons, EXERCISES, chapter 20 of the TEXTBOOK, and
  a capstone (`hands_on/security_review.py`) that attacks a naive and a hardened
  build of the same boundary and writes deterministic release evidence. No API key,
  no network call, standard library only. It is the third repo in the series that
  runs entirely for $0, after Production and AI Data Engineering.
- **One big idea: treat the model as an untrusted principal, not a security
  boundary.** The model proposes; trusted code decides. Identity, policy, provenance,
  isolation, and budgets are enforced where a compromised model cannot argue with
  them.
- **The complete OWASP LLM Top 10 2025 surface**, plus SSRF and generated-code
  isolation, each wired to an executable control rather than a checklist row. The
  first lesson exists to make the distinction: a taxonomy is a review aid, not your
  threat model.
- **Cross-references**: the bonus table and diagram in [README.md](README.md),
  chapter 20 in [TEXTBOOK.md](TEXTBOOK.md), a GenAI security section in
  [GLOSSARY.md](docs/GLOSSARY.md), a senior-role entry in [CAREERS.md](docs/CAREERS.md), ten
  new concern rows and a fifth cross-cutting principle in [SAFETY.md](docs/SAFETY.md),
  and a row in [CHOOSING.md](docs/CHOOSING.md).

### Notes

An audit after the initial build found three defects, all in the capstone rather
than the controls, and all now fixed with tests. They are written up in the repo's
[LESSONS.md](genai-security-deep-dive/LESSONS.md) because the shape they share is
worth carrying into any release gate:

- The gate derived its required risk categories from the probe suite it was
  grading, so deleting a probe deleted its own requirement. Coverage could not fail.
- The cloud-metadata SSRF probe used an `http://` URL and was rejected by the scheme
  allowlist, so the resolved-address policy it was named for never ran. The report
  recorded a pass either way.
- The benign-utility probe returned a hardcoded `ALLOW`, so the measurement that
  catches an over-blocking regression was a constant.

Every one of them was a check that took its expected answer from its own input.
Probe outcomes now carry the control that decided them into
`security-report.json`, which is what makes that class of defect visible.

---

## 2026-08-12: typescript-ai-deep-dive, a companion outside the sequence

The series teaches in Python and will keep doing so. But the most common question
it gets is from people whose AI work has to ship inside a TypeScript codebase,
and the honest answer needed measuring rather than asserting: which differences
are real, which are folklore, and which one is dangerous.

This is deliberately **not** a dive in the sequence. It is not in the core or
bonus tables, its textbook chapter is unnumbered, and nothing in the series
depends on it.

### Added

- **`typescript-ai-deep-dive/`**, a standalone repo in the house style: 13
  runnable examples, a `tsai/` from-scratch library, `check_setup.ts`, EXERCISES,
  an unnumbered TEXTBOOK, and a capstone (`hands_on/ask.ts`, a typed streaming
  agent CLI). Twelve of the thirteen examples need no API key; the whole repo
  runs on an offline mock provider by default, with the same loud fallback the
  sibling dives use.
- **One big idea, and it is not the one people expect.** TypeScript's types are
  erased at runtime, so the place a Pydantic user expects the most help (parsing
  what the model said) is the one place annotations do nothing. The repo builds
  everything around that: Zod at the boundary, `unknown` for tool arguments, and
  a `ParseResult` union where skipping the check does not compile.
- **Three measurements with no Python equivalent to point at.** The standard
  library gap, counted rather than complained about (13 lines of statistics, one
  genuine hole in binary formats, and `node:test` as a row where Node wins). The
  single event loop, measured from a second process. And a live PyPI-versus-npm
  ecosystem comparison that re-fetches on every run instead of going stale.
- **An aside in [README.md](README.md) and [TEXTBOOK.md](TEXTBOOK.md)** pointing
  at it, phrased as a companion rather than a step.

### Notes

Four findings changed what the repo teaches, and are written up in its
[LESSONS.md](typescript-ai-deep-dive/LESSONS.md):

- The unchecked cast does **not** produce `NaN`. `"12.40" * 0.21` is the correct
  VAT, which is why the bug survives review.
- Forced to fill a required field it could not know, neither default model
  hallucinated: `gpt-5.4-nano` returned `""` and `claude-haiku-4-5` returned
  `"<UNKNOWN>"`. The real problem is that each invents its own undocumented
  encoding for "absent" and `z.string()` accepts all of them.
- Aborting a stream throws on two of three stacks and never the same way, so
  matching on `error.name` is wrong on two of them.
- A blocked event loop is invisible from inside the blocked process. The first
  version of that example measured a healthy 2ms and printed it under the word
  "stalled."

---

## 2026-08-11: mcp-deep-dive, sessions and stateless HTTP

Section 9 taught stdio versus HTTP and stopped there, so the dive never
mentioned the one thing the network transport adds: a session. That left the
series' oldest thread (the API is stateless, so any server can take your next
call) with a hole exactly where it repeats one layer down.

### Added

- **The session, made visible.** `servers/calculator_http.py` takes
  `--stateless`, which passes `stateless_http=True` to `run()`, and
  `examples/08_http_transport.py` drops to raw HTTP after the SDK part to print
  whether the server issued an `Mcp-Session-Id` (then ends the session with a
  `DELETE`). The tool call is identical in both modes; only the header moves.
  Raw HTTP via stdlib `urllib`, deliberately: `mcp` 2.x depends on `httpx2`, so
  an `import httpx` would only work because the provider SDKs happen to pull the
  old one in, and Sections 2 to 9 are supposed to run without them.
- **README section 9 and TEXTBOOK 14.5** carry the tradeoff, stated precisely
  rather than as "stateless loses features": notifications during a call still
  work (they ride the open request's stream), while resumable streams and
  server-to-client requests like sampling do not, because the client's reply
  has nowhere to land. Verified against the SDK, which sets
  `can_send_request=False` on the stateless path and raises `NoBackChannelError`
  instead of hanging.
- **An exercise** in section 9: predict what disappears, then move the mode to
  an environment variable and defend stateless as the default.

### Fixed

- **`MCPServer` constructor kwargs.** `calculator_http.py` said host and port
  could be set on the constructor. True in SDK 1.x; in 2.x `host`, `port`,
  `streamable_http_path`, `json_response` and `stateless_http` are all `run()`
  arguments and the constructor raises `TypeError`. Added as a troubleshooting
  row, since anyone porting 1.x code hits it.

### Worth recording

The 2026-08-08 port to SDK 2.x was verified in a fresh environment, so nobody
noticed that the dive's own `.venv` still had `mcp` 1.28.0 in it. The repo was
correct and green for a new reader while failing at `initialize()` for the
person who wrote it. Rebuilding from `requirements.txt` fixed it. Verifying a
dependency change in a clean venv is right, but it is not a substitute for
re-running in the venv that is actually sitting on disk.

---

## 2026-08-11: RESPONSIBILITY.md deepened

The page was thin relative to how much of the current argument about AI is
actually live. It went from 113 lines to ~390, keeping its shape (a map that
turns a worry into a measurement or a limit and points at the dive that
operationalizes it) rather than becoming an essay.

### Added

- **The person on the other side.** Anthropomorphism as a design choice rather
  than a user error, sycophancy as a thing with a clean eval, engagement as the
  wrong objective, a handoff path for users in distress, and the fact that a
  single disclosure at the top of a session decays.
- **Where your data came from.** Provenance notes per source, consent, the
  difference between deleting a row from a RAG index and retraining a fine-tune,
  output copyright, and annotation labor.
- **The footprint.** Published per-query numbers disagree by orders of magnitude
  because they measure different things. The lever you actually have (smaller
  model, caching, shorter contexts, fewer agent steps) is the same lever as cost.
- **Autonomy changes the calculus.** Sort actions by reversibility, not
  difficulty.
- **The rules stopped being hypothetical.** Dated August 2026 and sourced.
- **Where reasonable people disagree.** Six open questions left open, because a
  page that presented ethics as settled would break the series' own rule about
  showing the real tradeoff instead of a clean-but-false claim.

### Changed

- Concerns table split into four groups: what the system says, the person on the
  other side, what it's built on, who owns it.
- Four cross-cutting principles became six.
- Pre-launch checklist grew from 7 items to 13.
- `SAFETY.md` and `README.md` pointers updated to match the wider scope.

### Ground truth used for the regulation section

Verified against live sources on 2026-08-11, not from memory. Worth re-checking
before relying on it, in the same spirit as MODELS.md and prices:

| Fact | Status |
|------|--------|
| EU AI Act high-risk obligations | Deferred by the Digital Omnibus (in force 27 July 2026): Annex III to 2 Dec 2027, Annex I to 2 Aug 2028 |
| EU AI Act Article 50 transparency duties | Most still applied from 2 August 2026 |
| US state companion-chatbot laws | 12 states enacted in the first half of 2026 |
| Colorado | HB 26-1263 signed 1 Jul 2026, effective 1 Jan 2027; SB 26-189 repealed and re-enacted the Colorado AI Act, duties from 1 Jan 2027 |

The disclosure and crisis-handling behavior this page argued for on its own merits
turns out to be the behavior the statutes are converging on.

---

## 2026-08-08: currency audit

A full pass over every submodule (except `architecture-deep-dive`) checking that
the code runs and the prose describes current practice as of August 2026.

### Ground truth used for this pass

Verified against live sources on 2026-08-08, not from memory:

| Fact | Source |
|------|--------|
| OpenAI model IDs and availability | `GET /v1/models` on a real key, plus the pricing and deprecations pages |
| Anthropic model IDs, pricing, thinking API | `claude-api` skill reference, cached 2026-06-24 |
| Python package versions | PyPI JSON API |
| MCP SDK 2.0 breaking changes | `py.sdk.modelcontextprotocol.io/migration/`, confirmed by installing it |

Two things worth recording because they contradict what a search will tell you:

- **`o4-mini` and `o3` are still live in the API.** The February and August 2026
  retirements that show up in search results were ChatGPT retirements, not API
  ones. Both still appear in `GET /v1/models`.
- **`gpt-4o-mini` is not deprecated.** It still works. It was replaced in the
  examples because it is a 2024 model and no longer represents current practice,
  not because it broke.

### Fixed

- **mcp-deep-dive: the repo did not run.** `requirements.txt` asked for
  `mcp[cli]>=1.2.0` while its own comment said "pin to a 1.x release". MCP Python
  SDK 2.0.0 shipped 2026-07-28, so a fresh install resolved to 2.0.0 and every
  server and client example failed at import: `mcp.server.fastmcp` no longer
  exists (`FastMCP` is now `MCPServer` in `mcp.server.mcpserver`). Eight files
  were affected.

- **openai-api-deep-dive: two request bodies would have 400'd.** `hands_on/ask.py`
  and the batch example build their request as a dict, so the `max_tokens` rename
  below missed them on the first pass.

- **The `stop` parameter is gone from the entire GPT-5 line**, which broke the
  stop-sequences lesson, the `--stop` flag on `ask.py`, and the OpenAI branch of
  the prompt-engineering provider. Only the legacy gpt-4o line still accepts it.

### Changed

- **OpenAI examples moved off `gpt-4o-mini` to `gpt-5.4-nano`.** Not because
  gpt-4o-mini broke (it still works) but because it is a 2024 model.

  The first choice here was `gpt-5.6-luna`, the newest cheap tier. Probing it
  against what the dives actually do killed that idea: the 5.6 tiers reject
  `temperature` and `top_p`, and refuse function calling on
  `/v1/chat/completions` unless you set `reasoning_effort: "none"` or move to the
  Responses API. `prompt-engineering-deep-dive` alone has 25 files touching
  `temperature`. `gpt-5.4-nano` costs the same ($0.20/$1.25 vs $0.20/$1.20),
  is current generation, and defaults `reasoning.effort` to `none`, so every
  existing lesson survives.

- **`max_tokens` is now `max_completion_tokens` on OpenAI calls only.** The
  GPT-5 line rejects the old name. Anthropic still uses `max_tokens`, so the
  Claude branch of every dual-provider `providers.py` is untouched, as is
  local-models-deep-dive, whose local servers still expect the old name.

- **Stop sequences became a lesson about retirement.** Rather than delete the
  example, it now shows the 400 on a current model, the old behaviour on
  gpt-4o-mini, and the structured-output schema that replaces it.

- **fine-tuning-deep-dive tells the truth about the OpenAI path.** OpenAI is
  winding down self-serve fine-tuning (2026-05-07, 2026-07-02, 2027-01-06 by
  cohort), so the README's promise that one env var runs a real paid fine-tune
  is no longer true. The mock lifecycle is unchanged and is now the main path.

- MODELS.md rebuilt around the GPT-5 line, with the three parameter changes that
  break GPT-4 era code, and Claude's Opus 5 / Sonnet 5 added.

### Deliberately not changed

Stored results are records, not configuration, so the model names in them stay
as they were when the run happened:

- `deep-dive-capstone/evals/*` (a run from 2026-07-04)
- `professional-tools-deep-dive/*/VERDICT.md`, its `LESSONS.md`, and the exercise
  citing a judge model
- `AUTHORING-LESSONS.md`, which records observed model behaviour

Re-running those comparisons on `gpt-5.4-nano` is follow-up work. A find and
replace would have made them claim something that never ran.

- **deep-dive-capstone had the same MCP breakage**, found later via the pin
  audit: `askrepo/mcp_server.py` imports `mcp.server.fastmcp` and its
  requirements allowed 2.x. Ported and pinned the same way.

- **Dependency pins now carry an upper bound.** `context-engineering` and
  `prompt-engineering` asked for `anthropic>=0.40.0` while every sibling asked
  for `>=0.111.0`, and 0.40 predates `messages.parse`. Nothing anywhere had an
  upper bound, which is exactly how the MCP breakage happened, so provider SDKs
  are now ranged (`anthropic>=0.111.0,<1`, `openai>=2.0,<3`).

### Added

Five new modules, each covering something the series did not mention at all.
Every one was verified against the live API before being written up.

- **openai-api-deep-dive, example 26: the Responses API.** The dive taught Chat
  Completions and never mentioned the other endpoint, which matters now the
  Assistants API shuts down on 2026-08-26. Covers server-side conversation state
  and hosted tools, and is explicit that the cost is portability, since
  `/v1/chat/completions` is the dialect Ollama, LM Studio, vLLM and LiteLLM all
  speak and example 17 depends on that.

- **context-engineering-deep-dive, section 11: server-side compaction and
  context editing.** The dive built compaction by hand and never said the API
  now does it. Covers compaction (summarizes, needs Sonnet/Opus 4.6+) versus
  context editing (clears, runs on Haiku 4.5), and the trap where keeping only
  `.text` silently drops the compaction block, which stays invisible until the
  first real compaction near 150K tokens.

- **agent-harness-deep-dive, section 15: Managed Agents.** Referenced in six
  places, never demonstrated. Framed as the far end of the axis the dive walks,
  with a table mapping each section's problem to its hosted answer. Opt-in via
  `--real` because it provisions billable infrastructure; it cleans up after
  itself.

- **agent-harness-deep-dive, section 16: Agent Skills.** Progressive-disclosure
  instructions. Placed in the harness dive because which skills to attach is
  harness configuration, and because a skill can ship scripts that execute.

- **agents-deep-dive, examples 16 and 17: tool search, programmatic tool
  calling, and the memory tool.** The first two share a cause: the dive assumed
  a small tool surface and a small number of calls, and both assumptions fail in
  the context window. The memory tool is the counterpart to section 9, which
  dies with the process. The example implements the storage backend including
  the path-traversal guard, since memory paths are model-generated.

### Known follow-ups

- The seven `professional-tools-deep-dive` verdicts were measured on
  `gpt-4o-mini` and now carry a dated note saying so. Re-running them on
  `gpt-5.4-nano` is a deliberate exercise, not a find and replace.
- `realtime-voice-deep-dive` remains simulation-only and was not otherwise
  touched by this pass.
