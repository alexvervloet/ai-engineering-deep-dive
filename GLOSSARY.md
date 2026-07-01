# Glossary

Plain-English definitions of the terms the [deep dives](README.md) use. Each points
to the dive that covers it in depth. Skim it once; come back when a word snags.

---

## The model & the call

**Token** — the unit a model reads and writes; roughly ¾ of an English word (~4
characters). You're billed per token, and counts decide cost and context limits.
*(API dives)*

**Context window** — the maximum number of tokens a model can consider at once
(input + output). Everything the model "knows" for a request must fit here. *(API
dives; the core idea behind RAG)*

**Prompt** — the text you send. Usually a list of **messages** with **roles**.

**Role** — the label on each message: **system** (durable instructions/persona),
**user** (the human's input), **assistant** (the model's replies). *(API dives, §3)*

**System prompt** — the standing instructions that set the model's behavior, rules,
and output format for the whole conversation. *(API dives; Prompt Engineering)*

**Content block** — Claude returns a *list* of typed pieces (text, tool-use,
thinking) rather than a plain string. *(Claude API dive)*

**max_tokens** — a hard cap on how many tokens the model may generate in one reply.

**Stateless** — the API remembers nothing between calls. "Memory" is just you
re-sending the growing message list each turn. *(API dives; Agents §9)*

---

## Sampling & decoding

**Temperature** — how random the word choice is. 0 = deterministic/most-likely
(good for facts, extraction); higher = more varied/creative. *(API dives, §4)*

**top_p (nucleus sampling)** — an alternative randomness knob: only consider the
most-likely tokens whose probabilities sum to *p*. Use temperature *or* top_p, not
both. *(API dives, §4)*

**Stop sequence** — a string that, when generated, halts the response. *(API dives)*

**Logits / log-probabilities (logprobs)** — the model's confidence per token. Turn a
logprob into a probability to score how sure the model was. *(OpenAI dive, logprobs)*

**Seed / determinism** — `temperature=0` plus a fixed `seed` makes output (mostly)
reproducible — for tests and caching. Best-effort, not guaranteed. *(OpenAI dive)*

**Nondeterminism** — the same prompt can give different answers run to run, so one
result (or one eval score) is a sample, not the truth. *(Evals §10)*

---

## Prompting techniques

**Zero-shot / few-shot** — asking with no examples vs. showing 2–5 examples to teach
format and conventions. *(Prompt Engineering)*

**Chain-of-thought (CoT)** — asking the model to reason step by step before
answering; boosts accuracy on multi-step problems. *(Prompt Engineering §3)*

**Self-consistency** — sample several CoT answers and majority-vote. *(Prompt Eng §9)*

**ReAct** — interleave **Reason** and **Act**: Thought → Action (tool) → Observation,
looping. The pattern under most agents. *(Prompt Engineering; Agents)*

**Reflexion** — attempt → run a real check → reflect on the failure → retry. Stronger
than self-critique because the feedback is grounded. *(Prompt Engineering; Agents)*

**Meta-prompting** — using the model to rewrite/improve a prompt. *(Prompt Eng)*

**Reasoning model** — a model that generates a hidden chain of thought before
answering (OpenAI o-series, Claude extended thinking). Prompt them with the *goal*,
not "think step by step." *(Prompt Engineering; API dives)*

**Structured output** — forcing the reply into valid JSON or a schema, so code can
consume it. *(API dives; Prompt Engineering)*

**Prompt injection** — untrusted text (a user message or a retrieved document) that
hijacks the model's instructions. *(Prompt Injection & Guardrails)*

---

## Retrieval (RAG)

**RAG (Retrieval-Augmented Generation)** — find the right text and put it in the
context window so the model answers from *your* documents. *(RAG dive)*

**Embedding** — a vector (list of numbers) capturing a text's *meaning*; similar
meanings sit close together. The engine of semantic search. *(API dives; RAG §2)*

**Cosine similarity** — the standard measure of how close two vectors (meanings) are;
1 = identical direction, 0 = unrelated. *(RAG)*

**Vector store** — a collection of (text, embedding) pairs with nearest-neighbor
search to find the closest chunks to a query. *(RAG §4)*

**Chunking** — splitting documents into retrievable pieces before embedding. *(RAG §3)*

**Hybrid search** — combining keyword and semantic search to get each one's
strengths. *(RAG §7)*

**Reranking** — over-retrieve, then reorder the candidates with a stronger model.
*(RAG §8)*

**Grounding / citations** — instructing the model to answer *only* from the retrieved
context and cite which chunk it used — the basis of checkable answers. *(RAG)*

**HyDE / multi-query** — query transformations: embed a hypothetical *answer* (HyDE),
or fan out into paraphrases, to retrieve better. *(RAG, query transformation)*

**Contextual retrieval** — prepend a short situating sentence to each chunk *before
embedding* so isolated chunks stay findable. *(RAG)*

---

## Evaluation

**Eval** — a repeatable measurement of quality: **dataset → task → scorer → report**.
*(Evals dive)*

**Scorer** — the function that grades an output: code-based (exact match, regex,
JSON-valid) or an **LLM-as-judge**. *(Evals §3, §7)*

**LLM-as-judge** — using a model to grade outputs against a rubric, for things code
can't check. Watch for **position/verbosity bias**. *(Evals §7–9)*

**Pass rate / accuracy / precision / recall / F1** — standard metrics turning per-item
scores into one decision number. *(Evals §5)*

**pass@k** — fraction of tasks solved within *k* attempts. *(Evals §5)*

**Confidence interval / significance** — the honest way to tell a real improvement
from noise; a difference must clear its margin of error. *(Evals §10)*

**Inter-annotator agreement / Cohen's kappa** — how much human labelers agree
(corrected for chance); low agreement means noisy "ground truth." *(Evals)*

**Eval gate** — a CI check that fails the build when quality drops. *(Evals; Production)*

---

## Agents & tools

**Agent** — a loop where the model picks a **tool**, you run it, and you feed the
result back, until it produces a final answer. *(Agents dive)*

**Tool / function calling** — the model emits a request to call a function (name +
arguments); *you* run it and return the result. The model never runs your code.
*(API dives; Agents)*

**Workflow vs. agent** — a workflow is fixed steps *you* orchestrate in code; an agent
lets the *model* drive. Prefer the workflow when you can draw the flowchart. *(Agents)*

**Trajectory** — the full sequence of an agent's steps; you evaluate the process, not
just the final answer. *(Evals; Agents)*

**Human-in-the-loop** — requiring human approval before a risky (side-effecting) tool
runs. *(Agents §7)*

**MCP (Model Context Protocol)** — a standard for serving tools, data (**resources**),
and **prompts** to an LLM from a separate process. *(MCP dive)*

---

## Context & memory

**Context engineering** — deciding what goes into the context window, in what order,
and what to drop when it won't all fit. The complement to prompt engineering: *how
you ask* vs. *what the model can see when you ask*. *(Context Engineering dive)*

**Compaction / summary memory** — when a conversation outgrows its budget, replace
the oldest turns with a running **summary** and keep the recent turns verbatim — so
the *facts* survive even though the exact words don't. *(Context Engineering)*

**Sliding window** — keep the system prompt plus the most recent turns that fit a
token budget; the oldest scroll off (and are forgotten). Bounded but lossy. *(Context
Engineering §3)*

**Long-term memory** — durable facts stored *outside* any single conversation's
window and retrieved back in when a later turn (or session) needs them — RAG pointed
at the conversation. *(Context Engineering §5)*

**Lost in the middle** — a model's tendency to use information at the **start** and
**end** of a long context more reliably than what's buried in the **middle**; a
reason to order context by importance. *(Context Engineering §6)*

**Context rot** — quality degrading as a window fills with irrelevant "just in case"
context, even under the token limit; relevance beats volume. *(Context Engineering §8)*

---

## Production & safety

**Observability** — structured traces of what each request did (inputs, tokens, cost,
tools, latency). *(Production §3)*

**Prompt caching** — caching a long, repeated prefix so it bills at ~0.1× on reuse.
*(API dives; Production)*

**Semantic caching** — serving a cached answer when a new query is close *in meaning*
(not just identical text). *(Production)*

**Retry / backoff** — automatically re-trying a transient failure with growing delays.
*(Production §5)*

**Fallback / failover** — switching to a backup model when the primary fails. *(Production)*

**Circuit breaker** — stop calling a failing dependency for a cooldown, then test it
again. *(Production §5)*

**Rate limiting / token bucket** — capping request rate per user/tenant to protect a
shared backend (and your bill). *(Production)*

**Guardrail** — a check on what comes *in* (injection/abuse detection) or goes *out*
(secret/PII leak, harmful content). *(Prompt Injection; Production §7)*

**Moderation** — classifying content as harmful (hate/violence/sexual/self-harm) — a
separate concern from injection defense. *(Prompt Injection)*

**Data exfiltration** — leaking data through a channel like a markdown image URL the
client auto-loads. *(Prompt Injection)*

**Feedback flywheel** — capturing 👍/👎 on real answers to build eval and training
data. *(Production)*

---

## Model customization & deployment

**Fine-tuning** — training a model on your examples to change how it *behaves* (not
what it knows). *(Fine-tuning dive)*

**Distillation** — fine-tuning a small/cheap model on a strong model's outputs.
*(Fine-tuning)*

**LoRA / PEFT** — efficient fine-tuning that trains a small set of added weights
instead of all of them. *(Fine-tuning; Local Models)*

**Batch API** — submitting many requests for asynchronous processing at ~50% off.
*(API dives)*

**Multimodal** — accepting more than text (images, audio). *(Multimodal dive)*

**Open-weight / local model** — a model whose weights are public, run on your own
machine; speaks the OpenAI-compatible API. *(Local Models dive)*

**Quantization** — storing model weights in fewer bits (q4, q8) to shrink memory at a
small quality cost — what lets a model fit on a laptop. *(Local Models)*

**KV cache** — memory holding the keys/values for tokens in context; grows with
context length and can rival the weights in size. *(Local Models)*

**Serving engine** — the program that loads and runs a local model (Ollama,
llama.cpp, vLLM). *(Local Models)*
