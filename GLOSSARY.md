# Glossary

Plain-English definitions of the terms the [deep dives](README.md) use. Each points
to the dive that covers it in depth. Skim it once; come back when a word snags.

---

## The model & the call

**Token**: the unit a model reads and writes; roughly ¾ of an English word (~4
characters). You're billed per token, and counts decide cost and context limits.
*(API dives)*

**Context window**: the maximum number of tokens a model can consider at once
(input + output). Everything the model "knows" for a request must fit here. *(API
dives; the core idea behind RAG)*

**Prompt**: the text you send. Usually a list of **messages** with **roles**.

**Role**: the label on each message: **system** (durable instructions/persona),
**user** (the human's input), **assistant** (the model's replies). *(API dives, §3)*

**System prompt**: the standing instructions that set the model's behavior, rules,
and output format for the whole conversation. *(API dives; Prompt Engineering)*

**Content block**: Claude returns a *list* of typed pieces (text, tool-use,
thinking) rather than a plain string. *(Claude API dive)*

**max_tokens / max_completion_tokens**: a hard cap on how many tokens the model
may generate in one reply. The two names are the same idea on different
providers: Anthropic still calls it `max_tokens`, while OpenAI's GPT-5 line
rejects that name and requires `max_completion_tokens`. The rename is
meaningful, not cosmetic: on a reasoning model the cap also covers reasoning
tokens you never see, so a generous-looking cap can return an *empty* answer
with a finish reason of "length". *(API dives)*

**stop sequence**: a string that, if the model is about to generate it, ends the
reply there. A text-completion era idea, and a retreating one: OpenAI's GPT-5
line dropped `stop` entirely (Anthropic keeps `stop_sequences`). Where you would
once chop output at a marker, you now ask for a shape with structured outputs.
*(OpenAI dive §06)*

**Stateless**: the API remembers nothing between calls. "Memory" is just you
re-sending the growing message list each turn. *(API dives; Agents §9)*

---

## Sampling & decoding

**Temperature**: how random the word choice is. 0 = deterministic/most-likely
(good for facts, extraction); higher = more varied/creative. *(API dives, §4)*

**top_p (nucleus sampling)**: an alternative randomness knob: only consider the
most-likely tokens whose probabilities sum to *p*. Use temperature *or* top_p, not
both. *(API dives, §4)*

**Stop sequence**: a string that, when generated, halts the response. *(API dives)*

**Logits / log-probabilities (logprobs)**: the model's confidence per token. Turn a
logprob into a probability to score how sure the model was. *(OpenAI dive, logprobs)*

**Seed / determinism**: `temperature=0` plus a fixed `seed` makes output (mostly)
reproducible, for tests and caching. Best-effort, not guaranteed. *(OpenAI dive)*

**Nondeterminism**: the same prompt can give different answers run to run, so one
result (or one eval score) is a sample, not the truth. *(Evals §10)*

---

## Prompting techniques

**Zero-shot / few-shot**: asking with no examples vs. showing 2–5 examples to teach
format and conventions. *(Prompt Engineering)*

**Chain-of-thought (CoT)**: asking the model to reason step by step before
answering; boosts accuracy on multi-step problems. *(Prompt Engineering §3)*

**Self-consistency**: sample several CoT answers and majority-vote. *(Prompt Eng §9)*

**ReAct**: interleave **Reason** and **Act**: Thought → Action (tool) → Observation,
looping. The pattern under most agents. *(Prompt Engineering; Agents)*

**Reflexion**: attempt → run a real check → reflect on the failure → retry. Stronger
than self-critique because the feedback is grounded. *(Prompt Engineering; Agents)*

**Meta-prompting**: using the model to rewrite/improve a prompt. *(Prompt Eng)*

**Reasoning model**: a model that generates a hidden chain of thought before
answering (OpenAI o-series, Claude extended thinking). Prompt them with the *goal*,
not "think step by step." *(Prompt Engineering; API dives)*

**Structured output**: forcing the reply into valid JSON or a schema, so code can
consume it. *(API dives; Prompt Engineering)*

**Prompt injection**: untrusted text (a user message or a retrieved document) that
hijacks the model's instructions. *(Prompt Injection & Guardrails)*

---

## Retrieval (RAG)

**RAG (Retrieval-Augmented Generation)**: find the right text and put it in the
context window so the model answers from *your* documents. *(RAG dive)*

**Embedding**: a vector (list of numbers) capturing a text's *meaning*; similar
meanings sit close together. The engine of semantic search. *(API dives; RAG §2)*

**Cosine similarity**: the standard measure of how close two vectors (meanings) are;
1 = identical direction, 0 = unrelated. *(RAG)*

**Vector store**: a collection of (text, embedding) pairs with nearest-neighbor
search to find the closest chunks to a query. *(RAG §4)*

**Chunking**: splitting documents into retrievable pieces before embedding. *(RAG §3)*

**Hybrid search**: combining keyword and semantic search to get each one's
strengths. *(RAG §7)*

**Reranking**: over-retrieve, then reorder the candidates with a stronger model.
*(RAG §8)*

**Grounding / citations**: instructing the model to answer *only* from the retrieved
context and cite which chunk it used: the basis of checkable answers. *(RAG)*

**HyDE / multi-query**: query transformations: embed a hypothetical *answer* (HyDE),
or fan out into paraphrases, to retrieve better. *(RAG, query transformation)*

**Approximate nearest neighbor (ANN) / IVF / HNSW**: an index that finds *most* of
the closest vectors without scanning all of them, trading a little **recall** for a
large speedup. Brute force is exact but O(n); ANN (FAISS, hnswlib, pgvector's IVFFlat/
HNSW) is what you switch to at millions of vectors. *(RAG §15)*

**Contextual retrieval**: prepend a short situating sentence to each chunk *before
embedding* so isolated chunks stay findable. *(RAG)*

---

## The corpus behind the retrieval

*The vocabulary of keeping an index current, separated, and provable. Retrieval
assumes this work is done; these are its terms. (AI Data Engineering dive)*

**Data contract**: the rules a connector payload must satisfy, checked at runtime
rather than described in a document: known fields only, timestamps with offsets, a
non-empty ACL, a supported MIME type. A schema nobody enforces is a note, not a
contract. *(AI Data Engineering §1)*

**Connector**: the code that gets documents out of the system that owns them (a wiki,
a drive, a ticket tracker) and into your pipeline, with its rate limits, pagination,
and outages attached. *(AI Data Engineering §2)*

**Snapshot and high-watermark**: a full read of source state, plus the exact position
in the source's change history that the read corresponds to. Capturing them together
is what lets the incremental feed start with no gap and no loss. *(§2)*

**CDC (change data capture)**: consuming a source's stream of creates, updates, and
deletes instead of re-crawling it. The idea predates AI by decades; it comes from
database replication. *(§2, §6)*

**Cursor / checkpoint**: your saved position in the change stream. The rule that
makes crashes survivable: apply the change first, persist the cursor second. Reversed,
a crash skips events permanently and reports nothing. *(§2, §6)*

**Idempotency**: an effect that can be applied twice without changing the result.
Since delivery is at-least-once in practice, idempotent writes plus version comparison
are the workable substitute for exactly-once processing. *(§6)*

**Source version**: the monotonic number the source assigns a document, and the only
trustworthy way to decide whether an arriving event is news or an echo. Arrival order
is not, because retries and partitions reorder it. *(§6)*

**Tombstone**: a durable record that a document was deleted, at the version it was
deleted at. Without one, a late retry of an older event finds nothing in the index,
concludes the document is new, and resurrects it. *(§8)*

**Backfill**: a deliberate rerun of current source state after the *code* changed
(new parser, chunker, or embedding model) rather than the data. The one mode allowed
to rewrite a document at its existing version, and still not allowed to lift a
tombstone. *(§7)*

**Reconciliation**: periodically comparing source truth against index state to find
what the event stream missed: missing, stale, orphaned, or ACL-drifted documents.
Repair needs a budget, because a half-degraded source snapshot looks exactly like a
source that deleted everything. *(§8)*

**Lineage / provenance**: the record of which source document produced which chunk,
through which transform, at which version. What turns "why did it say that?" into a
query rather than an afternoon. *(§9)*

**Content addressing**: identifying work by the hash of its bytes so identical content
is parsed or embedded once. An optimization on compute only: identity, ACLs, and
lineage stay keyed to the document, or one tenant's cache becomes another's leak.
*(§4)*

**ACL propagation**: copying the source document's access control list onto every
chunk derived from it, so retrieval can filter before it ranks. Filtering after
ranking both leaks and silently under-returns. *(§5)*

**Tenant isolation**: keeping one customer's data unreachable from another's, in the
IDs, the query predicates, and the database itself. *(§5)*

**Row-level security (RLS)**: a database policy that filters rows per session, used
here as a second layer behind the application's own predicates. Note the trap:
Postgres exempts a table's *owner* from its policies unless the table is declared
`FORCE ROW LEVEL SECURITY`, so an app connecting as its migration role gets a policy
that enforces nothing. *(AI Data Engineering, capstone)*

**Data quality gate**: checks on the corpus itself (coverage, drift, empty chunks,
ACL parity, lineage coverage) that run before answer-quality evals. A stale corpus
scores perfectly against a stale eval set. *(§9)*

**RPO / RTO**: recovery point objective, how much source and change history you can
afford to lose; recovery time objective, how long a full rebuild actually takes. Both
are measured by rebuilding once, not estimated. *(§10)*

---

## Evaluation

**Eval**: a repeatable measurement of quality: **dataset → task → scorer → report**.
*(Evals dive)*

**Scorer**: the function that grades an output: code-based (exact match, regex,
JSON-valid) or an **LLM-as-judge**. *(Evals §3, §7)*

**LLM-as-judge**: using a model to grade outputs against a rubric, for things code
can't check. Watch for **position/verbosity bias**. *(Evals §7–9)*

**Pass rate / accuracy / precision / recall / F1**: standard metrics turning per-item
scores into one decision number. *(Evals §5)*

**pass@k**: fraction of tasks solved within *k* attempts. *(Evals §5)*

**Confidence interval / significance**: the honest way to tell a real improvement
from noise; a difference must clear its margin of error. *(Evals §10)*

**Inter-annotator agreement / Cohen's kappa**: how much human labelers agree
(corrected for chance); low agreement means noisy "ground truth." *(Evals)*

**Eval gate**: a CI check that fails the build when quality drops. *(Evals; Production)*

---

## Agents & tools

**Agent**: a loop where the model picks a **tool**, you run it, and you feed the
result back, until it produces a final answer. *(Agents dive)*

**Tool / function calling**: the model emits a request to call a function (name +
arguments); *you* run it and return the result. The model never runs your code.
*(API dives; Agents)*

**Workflow vs. agent**: a workflow is fixed steps *you* orchestrate in code; an agent
lets the *model* drive. Prefer the workflow when you can draw the flowchart. *(Agents)*

**Trajectory**: the full sequence of an agent's steps; you evaluate the process, not
just the final answer. *(Evals; Agents)*

**Human-in-the-loop**: requiring human approval before a risky (side-effecting) tool
runs. *(Agents §7)*

**MCP (Model Context Protocol)**: a standard for serving tools, data (**resources**),
and **prompts** to an LLM from a separate process. *(MCP dive)*

**Agent harness**: the layer that runs the agent loop for you and adds the things a
bare loop lacks: an event stream, hooks, a permission policy, a sandbox, and
subagents. Building *on* a harness (Claude Agent SDK, OpenAI Agents SDK, Managed
Agents) is most agent work in 2026. *(Agent Harnesses dive)*

**Hook**: a function the harness calls at a fixed point in a tool cycle: *pre-tool*
(block a call or substitute a result) and *post-tool* (transform a result, e.g.
redact a secret), where guardrails live without editing the loop. *(Agent Harnesses §4)*

**Permission policy**: a declarative allow / ask / deny verdict per tool, lifted out
of the loop so you can read, version, and swap it per environment. The productionized
form of human-in-the-loop approval. *(Agent Harnesses §5)*

**Sandbox**: the boundary tools execute inside (a path jail, a command allowlist, or
a hosted container): the model proposes, the sandbox disposes. *(Agent Harnesses §6)*

**Subagent**: a delegate the harness spawns as a nested run with its own context
window and toolset; only its final answer returns, keeping the parent's context
focused (context isolation). *(Agent Harnesses §7)*

**Server-side / hosted tool**: a tool the *provider* runs inside the turn (web
search, code execution) rather than your loop; you declare it and get a grounded
answer back, with no tool-result round-trip, trading control for zero plumbing.
*(Agents §hosted tools)*

**Computer use**: the agent loop pointed at a screen: the tools are screenshot /
click / type and the observation is an image. Reach for it only when the task lives
in a GUI with no API. *(Agent Harnesses §9)*

**Checkpoint / durable execution**: persisting a run's state (its transcript / step)
after each step so a crashed or redeployed process can **resume** where it stopped,
redoing nothing. The transcript *is* the checkpoint. *(Agent Harnesses §10)*

**Run record / task state**: the durable status of a run (`queued` → `running` →
`done` / `failed`), queryable after the fact: the difference between an agent you
*hope* finished and one you can *prove* did. *(Agent Harnesses §11)*

**Fan-out / join (map-reduce over agents)**: run many *independent* subagents
concurrently (each with its own context), then aggregate their results; the batch
costs the slowest worker, not the sum. *(Agent Harnesses §12)*

**Steering**: acting on a run *while it's in flight*: **inject** a message that
changes the next step, **queue** follow-ups, or **interrupt** (stop at a safe
boundary, not mid-tool). Distinct from the permission gate, which acts *before* a
tool. *(Agent Harnesses §13)*

**Orchestration graph**: driving control flow with *code* instead of the model: a
graph of nodes wired by conditional edges, giving branching and cycles (route →
handle → review → loop). Build one when you can draw the flowchart; use the agent
loop when you can't. The model behind LangGraph. *(Agent Harnesses §14)*

---

## Context & memory

**Context engineering**: deciding what goes into the context window, in what order,
and what to drop when it won't all fit. The complement to prompt engineering: *how
you ask* vs. *what the model can see when you ask*. *(Context Engineering dive)*

**Compaction / summary memory**: when a conversation outgrows its budget, replace
the oldest turns with a running **summary** and keep the recent turns verbatim, so
the *facts* survive even though the exact words don't. *(Context Engineering)*

**Sliding window**: keep the system prompt plus the most recent turns that fit a
token budget; the oldest scroll off (and are forgotten). Bounded but lossy. *(Context
Engineering §3)*

**Long-term memory**: durable facts stored *outside* any single conversation's
window and retrieved back in when a later turn (or session) needs them: RAG pointed
at the conversation. *(Context Engineering §5)*

**Lost in the middle**: a model's tendency to use information at the **start** and
**end** of a long context more reliably than what's buried in the **middle**; a
reason to order context by importance. *(Context Engineering §6)*

**Context rot**: quality degrading as a window fills with irrelevant "just in case"
context, even under the token limit; relevance beats volume. *(Context Engineering §8)*

**Prompt caching**: providers cache the prompt *prefix* so repeated context is
cheap (a cache *read*, ~0.1×) instead of reprocessed (a *write*, ~1.25×). Any change
to the prefix invalidates everything after it, so compaction and pruning, which
rewrite the prefix, can *raise* your bill even as they shrink the window. *(Context
Engineering §10; Claude API)*

---

## GenAI security

**Untrusted principal**: the security model for an LLM: it may *propose* data and
actions, but trusted code derives identity and decides what is authorized. A model's
intent is never authority. *(GenAI Security)*

**Threat model / trust boundary**: the system-specific map of assets, owners, entry
points, data flows, attacker capabilities, and consequences; a trust boundary is where
data or authority moves between differently trusted components. A top-ten list helps
review the map but cannot replace it. *(GenAI Security §1)*

**Capability broker / reference monitor**: trusted code between a model proposal and
an effect. It combines authenticated subject, tenant, roles, object policy, approval,
idempotency, and limits, then denies or creates the effective tool arguments. *(§6)*

**Least privilege**: giving a principal only the smallest capability, scope, and
duration required. For an agent that means narrow tools, tenant-scoped objects,
bounded output and time, and separately approved irreversible actions. *(§6)*

**Artifact provenance / attestation**: evidence binding exact model, prompt, dataset,
dependency, or image bytes to an immutable version, source, builder, and approval. A
checksum detects changed bytes; provenance answers who produced and approved them.
*(§3; SLSA)*

**Data or model poisoning**: changing training, fine-tuning, evaluation, or retrieval
data so future behavior is manipulated. Record-level triggers, conflicting labels,
untrusted sources, duplicates, and population shifts are quarantined with evidence.
*(§4)*

**Sink-specific output validation**: treating model output as untrusted input to the
next interpreter: an exact schema for structured actions, parameter binding for SQL,
and context-appropriate encoding for HTML. There is no universal sanitizer. *(§5)*

**Retrieval prefilter**: applying tenant, ACL, and source-approval policy before
similarity ranking, context construction, tracing, or caching. Filtering afterward is
both a disclosure risk and a relevance bug. *(§7; AI Data Engineering §5)*

**Egress policy / SSRF**: restricting a server-side fetch by scheme, exact host, port,
resolved public address, redirects, bytes, and time. A model-selected URL is
attacker-controlled even when its hostname looks familiar. *(§8; CWE-918)*

**Denial-of-wallet / resource reservation**: exhausting money or capacity through
tokens, recursive steps, tools, retries, bytes, or time. Reserve the worst-case effect
against one shared request budget *before* starting work. *(§10)*

**Adversarial release gate**: a CI decision that combines attack success, benign
utility, required-risk coverage, and evaluator health. Block-all behavior, missing
categories, and harness exceptions all fail. *(§11)*

**Containment / eradication / recovery**: the incident sequence: stop the active blast
radius, remove the root cause and add its regression, then restore service only after
the release gate passes. Evidence preservation begins before destructive repair.
*(§12)*

---

## Production & safety

**Observability**: structured traces of what each request did (inputs, tokens, cost,
tools, latency). *(Production §3; Observability)*

**Data / input drift**: the distribution of what users send shifts over time (new
topics, new wording), so a model quietly answers things it was never good at: no
error, just worse answers. *(Observability §5)*

**Concept drift**: the input→output relationship changes. For LLM apps the usual
culprit is a **silent model swap** or a prompt edit that makes answers worse on the
same questions. *(Observability §6)*

**Embedding drift**: measuring input drift by *meaning*: how far today's requests
sit from a baseline's center of mass in embedding space. *(Observability §5)*

**PSI (Population Stability Index)**: the classic MLOps statistic for "how much did
this distribution move?" (`<0.1` stable, `>0.25` major shift). *(Observability §5, §9)*

**Baseline / z-score**: learn what "normal" looked like from a clean window, then
score each new day in standard deviations from it, so "weird" is relative, not a
hand-tuned constant. *(Observability §4)*

**Alert fatigue**: too many false alarms, so the team mutes the alert, and the
muted alert is the one that misses the real outage. The reason alerting trades
false alarms against detection lag. *(Observability §7)*

**Prompt caching**: caching a long, repeated prefix so it bills at ~0.1× on reuse.
*(API dives; Production)*

**Semantic caching**: serving a cached answer when a new query is close *in meaning*
(not just identical text). *(Production)*

**Retry / backoff**: automatically re-trying a transient failure with growing delays.
*(Production §5)*

**Fallback / failover**: switching to a backup model when the primary fails. *(Production)*

**Circuit breaker**: stop calling a failing dependency for a cooldown, then test it
again. *(Production §5)*

**Rate limiting / token bucket**: capping request rate per user/tenant to protect a
shared backend (and your bill). *(Production)*

**Guardrail**: a check on what comes *in* (injection/abuse detection) or goes *out*
(secret/PII leak, harmful content). *(Prompt Injection; Production §7)*

**Moderation**: classifying content as harmful (hate/violence/sexual/self-harm): a
separate concern from injection defense. *(Prompt Injection)*

**Data exfiltration**: leaking data through a channel like a markdown image URL the
client auto-loads. *(Prompt Injection)*

**Feedback flywheel**: capturing 👍/👎 on real answers to build eval and training
data. *(Production)*

---

## Model customization & deployment

**Fine-tuning**: training a model on your examples to change how it *behaves* (not
what it knows). *(Fine-tuning dive)*

**Distillation**: fine-tuning a small/cheap model on a strong model's outputs.
*(Fine-tuning)*

**SFT / preference tuning (DPO) / RFT**: the three ways to train behavior. **SFT**
learns from demonstrations (one right answer); **preference tuning / DPO** from
comparisons (A is better than B); **reinforcement fine-tuning (RFT)** from a
*grader* that scores each attempt, used when success is checkable but not easily
demonstrated (how reasoning models are trained). *(Fine-tuning §11–12)*

**LoRA / PEFT**: efficient fine-tuning that trains a small set of added weights
instead of all of them. *(Fine-tuning; Local Models)*

**Batch API**: submitting many requests for asynchronous processing at ~50% off.
*(API dives)*

**Multimodal**: accepting more than text (images, audio). *(Multimodal dive)*

**Native PDF input**: passing a PDF to the model as its own content block (real
text + page structure), the enterprise default, vs the workaround of screenshotting
a document and using vision. *(Multimodal §11)*

**Realtime voice**: a low-latency, full-duplex spoken loop: audio streams both ways,
turns are detected from silence, and the user can interrupt. *(Realtime Voice dive)*

**Barge-in**: the user interrupting the agent mid-response; a good voice agent stops
speaking instantly and listens. Needs full-duplex audio + fast cancellation. *(Realtime Voice §5)*

**Architecture Decision Record (ADR)**: a short document recording one structural
decision: the context, the options, the choice, the consequences, and the conditions
that would reverse it. Useful precisely because it names what would change your mind.
*(Architecture, all chapters)*

**Blast radius**: how much of a system a single failure takes with it. An in-process
model that is OOM-killed takes the health check and the cached responses with it; a
separate model tier does not. *(Architecture §4)*

**Circuit breaker**: stop calling a dependency that has stopped answering, so requests
fail fast instead of holding a worker for the full deadline. A capacity device, not a
latency-percentile one. *(Architecture §6)*

**Hold-back window**: streaming output while keeping the last N tokens unsent, so an
output guard sees them before the user does. Buys containment with first-token latency.
*(Architecture §5)*

**Load shedding**: refusing work immediately when the queue is too deep, rather than
accepting it and making the client wait for a deadline it will not meet.
*(Architecture §3)*

**Sticky routing**: sending every request in a session to the same worker, which makes
in-process state work until that worker restarts. *(Architecture §2)*

**Write-through indexing**: re-embedding a document when it changes, rather than
rebuilding the index on a timer or on every request. Work scales with the edit rate
instead of the query rate. *(Architecture §7)*

**STT→LLM→TTS pipeline vs speech-to-speech**: the two voice architectures: three
models in series (a text transcript in the middle you can log and moderate, more
control) vs one model hearing and speaking audio directly (fewer hops, lower latency,
more natural). *(Realtime Voice §3, §7)*

**Turn detection (VAD)**: deciding the user is done speaking, usually from a run of
silence; too eager clips them, too patient feels slow. *(Realtime Voice §2)*

**Open-weight / local model**: a model whose weights are public, run on your own
machine; speaks the OpenAI-compatible API. *(Local Models dive)*

**Quantization**: representing weights (and sometimes activations or KV state) at lower
precision to reduce memory and potentially change performance. Quality loss, kernel
support, and speed depend on format, model, workload, runtime, and hardware; bit width
alone is not a throughput result. *(Local Models; Inference Platform §22.6)*

**KV cache**: memory holding the keys/values for tokens in context; grows with
context length and can rival the weights in size. *(Local Models)*

**Serving engine**: the program that loads and runs a local model (Ollama,
llama.cpp, vLLM). *(Local Models)*

**TTFT / TPOT**: time to first token measures arrival through queueing and prefill to
the first streamed token; time per output token measures average decode spacing after
it. They diagnose different serving phases and must not collapse into one latency
average. *(Inference Platform §22.3)*

**Continuous batching**: revisiting batch membership between decode iterations so
finished sequences leave and newly arrived work can fill their lanes. It reduces
request-level head-of-line blocking but still has prefill/decode fairness trade-offs.
*(Inference Platform §22.4)*

**Prefix caching**: reusing prefill KV blocks for an exact token prefix under the same
model, tokenizer, adapter, and security scope. Visible text or a caller's cache label
is not sufficient identity. *(Inference Platform §22.5)*

**Speculative decoding**: a cheaper draft model proposes several tokens and the target
model verifies them in parallel, preserving the target distribution under the exact
algorithm. It helps only when acceptance repays drafting and verification overhead.
*(Inference Platform §22.7)*

**Tensor / pipeline / data / expert parallelism (TP / PP / DP / EP)**: four distinct
ways to distribute inference: split operations inside layers, split layer ranges into
stages, duplicate complete replicas, or distribute MoE experts. Fit, divisibility, and
physical link topology constrain which compositions are useful. *(Inference Platform
§22.8)*

**Admission control**: deciding and reserving worst-case request work before allocation;
when live capacity and the bounded queue are full, the platform sheds rather than
accepting work it predicts it cannot serve. *(Inference Platform §22.9)*

---

## Testing & delivery

**Evidence portfolio**: the set of check families a release requires, each catching a
different failure: unit, eval, SDK contract, property, integration, load, fault. The
required set is declared by the release owner, so the checks that happened to run
cannot decide which checks were needed. *(Testing & Delivery §23.2)*

**Vacuous gate**: a check that derives its expected answer from the same input it
judges, so it proves only that the input equals itself. Recording a broken response
and asserting the response matches the recording is the common shape.
*(Testing & Delivery §23.0, §23.3)*

**Fixture vs contract**: a fixture is a captured observation of real traffic; a
contract is a maintained requirement about shape. They change for different reasons
and belong in different files, or a bad recording silently becomes the spec.
*(Testing & Delivery §23.3)*

**Property test**: a test that states an invariant and lets a generator explore
inputs, rather than pairing one input with one expected output. A useful run reports
its generator, seed, first failure, and shrunk witness. *(Testing & Delivery §23.4)*

**Shrinking**: reducing a randomly found failure to the smallest input that still
fails, so the report explains the bug rather than merely proving one exists. A run
that exhausts its shrink budget must say the witness is not proven minimal.
*(Testing & Delivery §23.4)*

**Stub / mock / fake**: a stub returns canned data, a mock asserts an interaction
happened, and a fake implements simplified real behavior with state. A double must
model behavior, never carry the test's expected answer. *(Testing & Delivery §23.5)*

**Metamorphic test**: a test asserting a relation between two runs rather than one
absolute output, such as shifting every timestamp and requiring the derived durations
to survive. On floating-point values the relation holds within a stated tolerance,
not bit for bit. *(Testing & Delivery §23.6)*

**Nearest-rank percentile**: sort `n` values and take one-based rank
`ceil(percentile * n)`. The rank is not the value, and the one-based rank is not the
zero-based index; conflating them is the classic p95 bug. *(Testing & Delivery §23.6)*

**After-commit failure**: a fault that lands once the server has made its durable
change but before the client sees the response. The client cannot tell it from a
failure that changed nothing, which is what makes a blind retry duplicate the effect.
*(Testing & Delivery §23.7)*

**Artifact tuple**: the deployable candidate is not a model name but the combination
of source revision, prompt version, model and its features, index revision, schema
and embedding dimensions, SDK contract version, and dependency lock. Testing one
combination and shipping another is shipping something untested.
*(Testing & Delivery §23.8)*

**Lock file (`pylock.toml`)**: the PEP 751 standard record of an exact installation
result, as opposed to `pyproject.toml`, which records acceptable resolution inputs.
A lock makes inputs reviewable and repeatable; it does not make them safe.
*(Testing & Delivery §23.9)*

**Support promise vs support evidence**: `requires-python = ">=3.11"` is metadata. It
becomes evidence only once CI actually runs on 3.11; a green matrix of newer runtimes
cannot prove the lower bound. *(Testing & Delivery §23.10)*

**Shadow traffic**: a copy of real requests sent to the candidate with its response
discarded and external side effects blocked, so behavior can be compared before any
user is exposed. *(Testing & Delivery §23.12)*

**Canary**: routing a small real slice of traffic to the candidate, with allocation,
duration, and pass thresholds chosen before anyone looks at the results.
*(Testing & Delivery §23.12)*

**Evidence lineage**: binding each passing result to the candidate that produced it
via a subject digest, source revision, timestamp, and digest of the actual decision
payload, so a green result cannot be transferred to a different build.
*(Testing & Delivery §23.13)*
