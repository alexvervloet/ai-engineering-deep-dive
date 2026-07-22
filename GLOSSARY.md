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

**max_tokens**: a hard cap on how many tokens the model may generate in one reply.

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

**STT→LLM→TTS pipeline vs speech-to-speech**: the two voice architectures: three
models in series (a text transcript in the middle you can log and moderate, more
control) vs one model hearing and speaking audio directly (fewer hops, lower latency,
more natural). *(Realtime Voice §3, §7)*

**Turn detection (VAD)**: deciding the user is done speaking, usually from a run of
silence; too eager clips them, too patient feels slow. *(Realtime Voice §2)*

**Open-weight / local model**: a model whose weights are public, run on your own
machine; speaks the OpenAI-compatible API. *(Local Models dive)*

**Quantization**: storing model weights in fewer bits (q4, q8) to shrink memory at a
small quality cost, and what lets a model fit on a laptop. *(Local Models)*

**KV cache**: memory holding the keys/values for tokens in context; grows with
context length and can rival the weights in size. *(Local Models)*

**Serving engine**: the program that loads and runs a local model (Ollama,
llama.cpp, vLLM). *(Local Models)*
