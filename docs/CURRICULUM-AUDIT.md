# Curriculum audit for senior AI engineering

Audited 2026-09-06 against parent commit `27590d0` and its 25 pinned submodules.
This report recommends work. It does not apply the curriculum fixes below.

## Assessment

This is a substantial curriculum for engineers building LLM applications. The
strongest material teaches the work around the model: evaluation, permissions,
data lifecycle, failure recovery, and operational tradeoffs. Adding another
general agents, RAG, security, or MLOps survey would mostly duplicate it.

I would not yet describe completing the eight core dives as preparation for
senior ownership. Several subjects that ownership requires are called bonus
material. Much of the strongest evidence of real deployment and training lives
in companions that the parent explicitly excludes from the course. The course
also needs more work on problem selection, learning from data, and enterprise
tasks beyond answering questions about documents.

The first investment should be correcting misleading teaching claims and making
a senior path through material that already exists. After that, the best new
repositories are AI product experimentation and enterprise SQL. Document
intelligence is the next specialist addition. Real post-training belongs in the
existing Fine-tuning dive, with the `local-lora` companion as a starting point.

## Scope and evidence

I inventoried every submodule, README and textbook outline, numbered examples,
shared reference documents, and relevant exercises. I read selected implementations
and workflows to distinguish an explanation from a runnable demonstration. Evals,
Architecture, and ML Foundations supplied the comparison for teaching depth and
verification. Suspected omissions were checked across code and prose rather than
inferred from repository names.

I also read the relevant README content of `local-lora`, `askrepo-live`,
`deskhand`, `knowledge-desk`, `model-swap`, `rag-at-scale`, and
`client-context-compiler` through GitHub. Their documented scope counts as
companion coverage. Their production behavior and test suites were not independently
validated in this audit.

The senior bar here means owning an LLM feature through problem definition,
measurement, implementation, deployment, incidents, and revision. It does not
mean training frontier models or mastering every ML specialty. For a broader
interpretation of AI engineering, classical predictive ML needs an explicit
prerequisite or additional track.

Evidence labels used below:

- **Covered** means there is substantive teaching material and a runnable path.
- **Partial** means there is a treatment, but the named senior task lacks a
  complete learning exercise.
- **Integration gap** means a companion already addresses much of the subject.
- **Missing** means I found no dedicated treatment in the inspected curriculum.

This is a curriculum and targeted correctness audit, not an exhaustive security
review or certification that every example works. No paid API calls, training
jobs, or deployments were run.

## Coverage map

| Senior capability | Existing home | Assessment |
| --- | --- | --- |
| Provider calls, streaming, structured output, reasoning controls | [OpenAI](../openai-api-deep-dive/README.md), [Claude](../claude-api-deep-dive/README.md), [TypeScript](../typescript-ai-deep-dive/README.md) | Covered. OpenAI already has a substantial Responses track. A third provider tutorial is lower priority. |
| Prompt design, context assembly, memory, tool selection | [Prompt Engineering](../prompt-engineering-deep-dive/README.md), [Context Engineering](../context-engineering-deep-dive/README.md), [Agents](../agents-deep-dive/README.md) | Covered. Automatic optimization and comparative inference-budget experiments remain partial. |
| Retrieval and index operations | [RAG](../rag-deep-dive/README.md), [AI Data Engineering](../ai-data-engineering-deep-dive/README.md) | Covered, including hybrid retrieval, reranking, ANN, pgvector, CDC, ACLs, deletes, and rebuilds. Domain adaptation and multilingual retrieval are thin. |
| Evaluation and experiment statistics | [Evals](../evals-deep-dive/TEXTBOOK.md), [model-swap](https://github.com/alexvervloet/model-swap) | Covered, including pairing, power, practical effects, multiple testing, and repeated looks. Product experiment instrumentation is a separate gap. |
| Agent contracts and security | [Agents contracts](../agents-deep-dive/agent/contracts.py), [Prompt Injection](../prompt-injection-deep-dive/README.md), [GenAI Security](../genai-security-deep-dive/README.md) | Covered. Remote delegated authentication and uncertain external effects need applied exercises. |
| Durable execution and human approval | [Agent Harnesses](../agent-harness-deep-dive/README.md), [deskhand](https://github.com/alexvervloet/deskhand) | Integration gap. Deskhand documents real database recovery and approval binding. Its effects deliberately share one database transaction. |
| Interoperability | [MCP](../mcp-deep-dive/README.md), [2026 protocol notes](../mcp-deep-dive/PROTOCOL_2026.md) | Covered and recently updated. OAuth remains a further-study item rather than a lab. |
| Production architecture, reliability, cost, telemetry | [Production](../ai-in-production-deep-dive/README.md), [Architecture](../architecture-deep-dive/README.md), [Observability](../observability-deep-dive/README.md) | Covered. Real OpenTelemetry already exists. Deployment and recovery practice should draw on companions. |
| Testing, provenance, promotion, rollback | [Testing & Delivery](../testing-and-delivery-deep-dive/README.md) | Covered in simulations. An actual service release should consume this evidence. |
| Model mechanics and serving | [ML Foundations](../ml-foundations-for-ai-engineers/README.md), [Local Models](../local-models-deep-dive/README.md), [Inference Platform](../inference-platform-deep-dive/README.md) | Covered at the conceptual level, with real CPU training and local inference. GPU fleet planning is simulated and says so. |
| Model adaptation and training data | [Fine-tuning](../fine-tuning-deep-dive/README.md), [local-lora](https://github.com/alexvervloet/local-lora) | Partial and an integration gap. Formal LoRA and preference lessons explain rather than train. Data selection needs a complete feedback cycle. |
| Images, audio, voice, PDFs | [Multimodal](../multimodal-deep-dive/README.md), [Realtime Voice](../realtime-voice-deep-dive/README.md) | Covered as introductions. Complex documents, media evaluation, and actual voice transport are partial. |
| Governance, responsibility, incidents, UX | [Governance](GOVERNANCE.md), [Responsibility](RESPONSIBILITY.md), [Incidents](INCIDENTS.md), [AI UX](AI-UX.md) | Substantive written coverage. Accessibility, reviewer capacity, and cross-system privacy need applied exercises. |
| Product value and non-LLM alternatives | [Choosing](CHOOSING.md), [Governance](GOVERNANCE.md), [online eval](../evals-deep-dive/examples/12_online_eval.py) | Partial. No complete exercise joins workflow outcomes, experiment integrity, human effort, and total cost. |
| Enterprise analytics and complex document extraction | [SQL prompt example](../prompt-engineering-deep-dive/examples/05_text_to_sql.py), [Multimodal](../multimodal-deep-dive/README.md) | Partial. These are substantial new-dive candidates. |

## Corrections to make first

Priority 1 means fix before treating the material as senior-level instruction.
Priority 2 means a bounded refresh or qualification. These are findings, not
claims that every surrounding lesson is defective.

### F1. A prompt is presented as SQL safety enforcement

Priority 1. In [the SQL example](../prompt-engineering-deep-dive/examples/05_text_to_sql.py),
the final explanation says providing a schema prevents invented identifiers and
that requesting read-only SQL is a safety guardrail. The program prints the
generated SQL. It does not parse, authorize, execute, or evaluate it.

Change the explanation to say these instructions encourage valid output. They
cannot enforce it. Add a link to server-side controls and a deliberately bad
query that a restricted database identity refuses. A SELECT-only text check also
does not establish acceptable runtime cost, allowed functions, or permitted data.
Keep this lesson about prompting; put the complete execution boundary in R4 below.

### F2. The prompt capstone's scorer rewards contradictory labels

Priority 1. [The capstone's `score`](../prompt-engineering-deep-dive/hands_on/optimize.py)
checks whether the expected label appears among words in the output. It does not
enforce one unambiguous class. Direct execution of that function produced:

```text
score("Positive Negative Mixed", "Mixed") -> True
score("This is not Positive. It is Negative.", "Positive") -> True
```

Parse one allowed label, then compare it with the answer key. If explanations are
allowed, give the label a separate validated field. Test every class, conflicting
classes, negation, unknown labels, and an empty response. Keep format compliance
and classification accuracy separate.

The same capstone labels a double-charge ticket `High`, although its written
`High` rule requires a blocked paying customer and the ticket says the customer
can still work. Resolve the rubric or relabel the case before comparing prompts.
Otherwise the experiment can punish the model for following the supplied rule.

### F3. Basic eval helpers turn missing evidence into plausible numbers

Priority 1. [The metrics module](../evals-deep-dive/evals/metrics.py) uses `zip`
without validating lengths in accuracy and precision/recall. A reproduced call
returned `1.0` for one correct prediction against two expected labels. The
unpredicted case disappeared. Its confidence interval helper returns `(0.0, 0.0)`
for no observations and a zero-width interval for one observation.

Require aligned identities or equal lengths before aggregation. Classify missing
predictions explicitly according to the evaluation contract. Return an
insufficient-evidence state or error when an interval is not estimable. These
changes belong in the existing helpers and their tests. The newer
[decision module](../evals-deep-dive/evals/decision.py) already teaches stronger
contracts; this is inconsistent adoption, not missing statistical theory.

### F4. Preference data rewards an invented completed action

Priority 1. The first preferred answer in
[the DPO example](../fine-tuning-deep-dive/examples/10_preference_tuning.py)
claims the duplicate charge was found and refunded. The input only contains a
customer's complaint. There is no account lookup or successful refund result.

Replace the preferred answer with a truthful next step, or supply independently
recorded tool evidence that supports the completed action. Make factual support
and authorized action prerequisites for comparing tone.

The example also describes a thumbs-up response and an edited response as
interchangeable chosen/rejected candidates. A rating on one answer is not by
itself a pairwise preference. Preserve the same prompt and relevant context,
obtain two candidates, and record which response the reviewer prefers. An edited
correction will often be the chosen response. Do not infer that from its position.

### F5. The central knowledge and complexity shortcuts are too absolute

Priority 1. [The parent README](../README.md), [textbook map](../TEXTBOOK.md),
and [Fine-tuning](../fine-tuning-deep-dive/README.md) repeat the distinction that
fine-tuning changes behavior but not knowledge. A model can acquire factual
information through parameter updates, although acquisition can be inefficient
and can increase hallucination. The relevant research studies difficulty and
risk, rather than impossibility.
[Fine-tuning and new knowledge](https://arxiv.org/abs/2405.05904).

Use this narrower rule: fine-tuning changes parameters and learned behavior;
retrieval is usually easier to update, cite, permission, and delete when facts
change. Distinguish supervised instruction tuning from continued pretraining.

Likewise, a model can answer from knowledge in its parameters without retrieving
the fact into its context. The defensible RAG promise is that this application
requires evidence from supplied sources.

[Choosing](CHOOSING.md) says every higher rung costs more money and latency.
That is not a monotonic relationship. Fine-tuning can replace long prompts or
allow a smaller model. A tool lookup can avoid several model calls. Present
techniques as responses to different failure types, then compare their measured
cost, quality, and complexity. Add rules and classical classifiers before the
LLM choices.

### F6. Claude token counting is described as exact

Priority 1. [The token utility](../claude-api-deep-dive/utils/tokens.py) calls the
count authoritative rather than estimated, and
[the textbook](../claude-api-deep-dive/TEXTBOOK.md) repeats the exactness claim.
Anthropic explicitly describes an estimate that can differ from actual message
usage. It also distinguishes system-added tokens from billable content.
[Claude token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting).

Use counting for admission and planning with headroom. Reconcile spend from
response usage. Add an example comparing the preflight estimate with returned
usage, without asserting equality or requiring the values to differ.

### F7. Audio is incorrectly restricted to dedicated endpoints

Priority 2. [The Multimodal textbook](../multimodal-deep-dive/TEXTBOOK.md) says
speech does not travel in chat content blocks on these APIs. OpenAI documents
`input_audio` content blocks for audio-capable Chat Completions models.
[OpenAI audio guide](https://developers.openai.com/api/docs/guides/audio).

Keep transcription plus text generation plus synthesis as a valid architecture.
Label it as the path this lesson chooses. Add a model-specific comparison with
direct audio input and separate transcription quality from semantic task quality.

### F8. A durable engine is credited with an overly broad exactly-once guarantee

Priority 1. [Agent Harnesses](../agent-harness-deep-dive/README.md) describes
exactly-once replay across a mid-tool crash as a property of production durable
engines. Temporal distinguishes durable workflow replay from retried activities,
which require idempotency at their effects.
[Temporal on idempotency](https://temporal.io/blog/idempotency-and-durable-execution).

State the transaction boundary. A successful remote payment followed by a lost
response cannot be resolved by replaying the local transcript. Use the remote
operation's idempotency contract and reconciliation. Deskhand already explains
why its same-database version can make a narrower guarantee. Make that discussion
required reading and add the separating external-service failure exercise in R7.

### F9. The model catalog needs a refresh without changing every default

Priority 2. [Models](MODELS.md), dated 2026-08-17, says the current OpenAI models
are all GPT-5 and describes `gpt-5.6-sol` as the current flagship. Official docs
now list GPT-6 Astra. The snapshot has aged; that does not make the cheaper
teaching default wrong.
[GPT-6 Astra model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra).

Separate the pinned teaching configuration from the current market catalog.
Store model, endpoint, reasoning mode, supported parameters, source URL, and
verification date together. Resolve the internal contradiction where one part
of Models gives a `reasoning_effort: "none"` exception for GPT-5.6 parameters
while its parameter table describes unconditional rejection.

Two apparent update candidates are already handled. The fine-tuning retirement
notice matches the official availability dates, and the MCP migration notes
match the July 2026 revision. Preserve those updates.
[OpenAI deprecations](https://developers.openai.com/api/docs/deprecations),
[MCP July revision](https://blog.modelcontextprotocol.io/posts/2026-07-28/).

## Recommended additions

These are proposed paths, not files that already exist. The acceptance conditions
describe what a learner should be able to demonstrate. Priorities reflect the
general senior application engineer; role-specific options are marked.

### R1. Make senior ownership a visible learning path

Priority 1, integration gap. Add `docs/SENIOR-PATH.md` and
`docs/SENIOR-ASSESSMENT.md`. Link both from the parent README and Careers.

Require Evals, Production, Architecture, AI Data Engineering, GenAI Security,
Observability, Testing & Delivery, and the governance/incident material for the
senior application path. Treat Fine-tuning, Inference Platform, and advanced
media as role branches. Learning both provider dialects is useful but should not
delay measurement or security for an experienced engineer.

Make selected companions assessed extensions. Use Knowledge Desk for tenant
boundaries, Model Swap for a real model decision, Deskhand for durable effects,
and Askrepo Live for deployment. This recognizes existing work instead of
creating a second production curriculum.

The assessment should require a requirements brief, baseline, threat model,
cost estimate, release evidence, a tested recovery, and a defended design
decision. Give the learner an unfamiliar corpus and an unannounced failure.
Require them to explain when they would reject an LLM solution. Include an ADR
review and an operational handover, since senior work also means making another
engineer able to maintain the system.

### R2. Teach product value as an experiment

Priority 1, partial coverage. Create `ai-product-engineering-deep-dive`.

One big idea: an improved model score is useful only if the complete workflow
improves. Prerequisites are Evals and Production. Existing
[online eval](../evals-deep-dive/examples/12_online_eval.py) already teaches
uncertainty and guardrails; avoid reteaching its statistics.

Suggested sequence:

1. `examples/01_workflow_baseline.py`: compare human-only, rules, and model
   assistance on task completion and correction effort.
2. `examples/02_assignment_and_exposure.py`: stable user-level assignment,
   exposure logging, repeat users, and missing events.
3. `examples/03_experiment_integrity.py`: sample-ratio mismatch, attrition, and
   treatment contamination. A broken logger must prevent a launch decision.
4. `examples/04_cost_per_success.py`: model calls, retrieval, retries, review
   labor, and rework per successfully completed task.
5. `examples/05_launch_decision.py`: combine practical effect, guardrails,
   non-inferiority where appropriate, and the option to stop the project.

Use `hands_on/support_workflow.py` as a capstone. A synthetic user process can
teach instrumentation, but label it as simulation. It cannot prove real
adoption or business value. A field-study exercise should require consented
user observations and an honest inconclusive outcome when data is insufficient.

Microsoft's experiment research explains why assignment and logging integrity
must precede effect interpretation.
[Sample-ratio mismatch](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/).

### R3. Complete the real post-training path

Priority 1 for model customization roles, partial coverage and integration gap.
Extend `fine-tuning-deep-dive`; use `local-lora` rather than creating another
general fine-tuning repository.

[Example 09](../fine-tuning-deep-dive/examples/09_open_weights_lora.py) explicitly
does not train. [The mock trainer](../fine-tuning-deep-dive/finetune/mock_tuner.py)
builds a keyword table and fabricates its loss curve, which is disclosed and
suitable for lifecycle practice. It cannot teach optimizer debugging or adapter
quality. Local LoRA provides real MLX training, adapter fusion, and evaluation,
but its README scopes DPO out.

Add `examples/11_training_tokens_and_masks.py`,
`examples/12_adapter_training.py`, and `hands_on/train_and_release_adapter.py`.
Teach chat templates, target shifts, padding/EOS, truncation, assistant-only
loss, packing boundaries, gradient accumulation, precision, checkpoint resume,
and adapter/base compatibility. Make bad masks visibly train the wrong target.
Keep a tiny CPU mechanics path and label pretrained-weight downloads and the
optional MLX/CUDA paths.

Require train, development, and final test separation by source or task family.
Choose hyperparameters on development data. Report final held-out task quality,
general-capability regressions, measured memory, and serving behavior after
adapter merge or quantization. A smaller training loss is insufficient.

Add `examples/13_preference_objective.py` for a small numerical DPO exercise and
an optional actual trainer path. Explain the reference-policy term and test
reversed preferences. Put RLHF, verifiable rewards, GRPO, KL control, and reward
hacking in `POST-TRAINING.md`; require a grader-exploit experiment before an
optional reinforcement-learning lab. Full distributed RL training is specialist
work, not a prerequisite for every application engineer.

The TRL documentation provides concrete contracts for templates, packing, and
assistant-only loss that a messages JSONL validator cannot establish.
[SFT Trainer](https://huggingface.co/docs/trl/sft_trainer).

### R4. Add enterprise SQL and semantic correctness

Priority 1 for enterprise application work, partial coverage. Create
`structured-data-ai-deep-dive` after Prompt Engineering, Evals, and GenAI Security.

One big idea: executable SQL can still answer the wrong business question.
The existing [SQL example](../prompt-engineering-deep-dive/examples/05_text_to_sql.py)
is a prompt comparison. This dive should teach schema discovery, metric
definitions, join cardinality, grain, nulls, time zones, currency, and ambiguity.

Build `examples/01_metric_contract.py`, `examples/02_join_fanout.py`,
`examples/03_query_policy.py`, `examples/04_database_identity.py`, and
`examples/05_execution_eval.py`. Use a local database and independent answer
queries. Add adversarial schema descriptions, expensive queries, forbidden
functions, and cross-tenant requests. Enforce permissions in the database under
the actual application role, with statement and result limits.

The capstone, `hands_on/analyst.py`, should ask for clarification when two
revenue definitions fit, expose its metric and time window, and return results
with query provenance. Test correctness across several database states so a
wrong query cannot pass by coincidentally returning the same number once.
Use Spider 2.0 as a source of realistic workflow complexity, not a promise that
this small lab reproduces the benchmark.
[Spider 2.0](https://arxiv.org/abs/2411.07763).

### R5. Turn deployment companions into an operations practicum

Priority 1, integration gap. Add `docs/OPERATIONS-PRACTICUM.md`, anchored in
Askrepo Live and Knowledge Desk. Their READMEs already describe Docker,
deployment, persisted data, budgets, and telemetry. A new generic deployment
repository would duplicate them.

The practicum should start from a clean checkout, build an image, apply schema
migrations, configure secrets or workload identity, verify readiness, and serve
a request through the real process boundary. Follow with a rolling release,
stream cancellation, worker termination, backup restore, and rollback of a
model/prompt/index tuple. Require measured recovery time and a data-loss bound.
Distinguish restoring availability from undoing external actions.

Use local containers first, then one optional paid deployment with an explicit
teardown command and budget. Teach an infrastructure-as-code example for that
one target. Kubernetes administration is an optional platform branch, not a
reason to make everyone maintain a cluster.

For inference specialists, add
`inference-platform-deep-dive/hands_on/measure_runtime.py`. Collect real serving
metrics and compare them with the existing planner's assumptions, including
queueing, warmup, KV pressure, output lengths, and failed requests. A GPU-free
planner is not a GPU performance measurement. Preserve that honest distinction.

### R6. Make remote identity and delegation executable

Priority 1, partial coverage. Add
`mcp-deep-dive/examples/12_remote_authorization.py` and
`mcp-deep-dive/hands_on/authorized_tool_service.py`.

The [MCP notes](../mcp-deep-dive/PROTOCOL_2026.md) describe authorization
hardening, while the [README](../mcp-deep-dive/README.md) leaves OAuth for further
study. GenAI Security teaches application-owned identity, but not an end-to-end
remote authorization flow.

Use a local authorization server and the current supported SDK. Teach discovery,
PKCE where applicable, issuer and audience checks, scopes, expiry, credential
storage, revocation behavior, and the difference between an application's
identity and a user's delegated authority. Include background jobs that outlive
the initiating session. Do not let a model supply trusted identity fields.

Prove refusal for a wrong issuer, wrong audience, insufficient scope, and a
direct request bypassing the teaching client. A benign authorized request must
still work. Bind private catalog caches to the authorization context. The July
MCP release makes issuer validation and credential binding explicit.
[MCP authorization changes](https://blog.modelcontextprotocol.io/posts/2026-07-28/).

### R7. Cross the external-effect boundary in durable execution

Priority 1 for agents that act, partial coverage. Add
`agent-harness-deep-dive/examples/16_unknown_external_outcome.py`, or put the
exercise in Deskhand and make it part of the formal path.

Reuse Deskhand's persisted runs and approval model. Add a local HTTP payment
simulator with its own database. Let it commit an operation and drop the response.
The worker must represent the outcome as unknown, query or reconcile it, and
recover without charging again. Repeat the fault after a restart. Include
same-key/same-payload replay, same-key/different-payload conflict, and a fresh
operation. Document idempotency expiry.

Extend to an outbox and compensating action only when the scenario needs them.
Do not label a refund or cancellation as a universal rollback. This is the
specific gap left by a same-transaction ledger, not a need for another generic
agent loop.
[Temporal's external-effect discussion](https://temporal.io/blog/idempotency-and-durable-execution).

### R8. Teach the data improvement cycle

Priority 1, partial coverage. Add
`fine-tuning-deep-dive/hands_on/improve_dataset.py` and `DATA-CURATION.md`.

[Observability](../observability-deep-dive/obs/mining.py) already mines candidates
and leaves their answer keys blank for a human. Fine-tuning already validates
format, duplicates, and balance and discusses distillation. Join those pieces
into a reproducible cycle with annotation guidelines, adjudication, provenance,
near-duplicate families, privacy screening, and train/development/test assignment
before expansion.

Compare random selection with uncertainty or disagreement sampling under a
fixed labeling budget. Preserve a representative test sample because actively
selected cases are not an unbiased estimate of production quality. Add
synthetic examples only after checking support, diversity, and duplicate
lineage. Teacher output is a candidate label, not ground truth. Self-Instruct
provides a useful primary example of generation combined with filtering.
[Self-Instruct](https://arxiv.org/abs/2212.10560).

The exercise passes when it can trace an observed failure to a reviewed data
change and a separate held-out evaluation. It must be allowed to conclude that
the new data did not help. Keep retrieval corpus synchronization in AI Data
Engineering; this addition owns supervision and sampling.

### R9. Add abstention and human review as measured policies

Priority 1 for consequential decisions, otherwise Priority 2. Add
`evals-deep-dive/examples/15_selective_prediction.py` and
`typescript-ai-deep-dive/hands_on/review_queue/`, with links from AI UX.

[ML Foundations](../ml-foundations-for-ai-engineers/ml_foundations/calibration.py)
already teaches held-out temperature scaling. Extend it into a choice among
answering, asking for clarification, and routing to a reviewer. Report error
among answered cases, coverage, subgroup results, review delay, and cost. Fit
thresholds on calibration data, then test under a changed distribution. Token
probability must not silently become confidence that a whole answer is correct.
Selective classification provides the risk/coverage framing.
[Selective classification](https://arxiv.org/abs/1705.08500).

The UI exercise should preserve evidence, enforce reviewer roles, handle stale
approvals and queue overload, and allow correction. Check keyboard navigation,
focus after streamed updates, and screen-reader announcements against applicable
WCAG criteria. AI UX already asks for accessibility; the gap is an actual test.
[WCAG 2.2](https://www.w3.org/TR/WCAG22/).

### R10. Extend retrieval by failure type

Priority 2, missing or partial specialist coverage. Start with examples in RAG,
rather than a general advanced-RAG repository.

| Proposed path under `rag-deep-dive` | Missing lesson | Required observation |
| --- | --- | --- |
| `examples/17_embedding_selection.py` | Domain and language fit, query/document formatting, task-specific relevance | Compare fixed candidates on held-out queries and language slices with the generator held constant. |
| `examples/18_retriever_adaptation.py` | Contrastive learning, hard negatives, false negatives, retriever/reranker tuning | Show how a mislabeled near-match changes retrieval; preserve source-family splits and compare recall and ranking quality. |
| `examples/19_multihop_retrieval.py` | Decomposition, entity identity, relation evidence, SQL/graph traversal versus vector retrieval | Answer a question requiring two supported links, reject a missing link, and count extra latency and calls. |
| `RETRIEVAL-CHOICES.md` | Dense, sparse, hybrid, late interaction, long context, and GraphRAG selection | Map each method to a measured failure and a condition where its complexity is not justified. |

Sentence Transformers documents different similarity objectives and practical
training/evaluation contracts.
[Training overview](https://www.sbert.net/docs/sentence_transformer/training_overview.html).
Do not re-add HNSW or large-index benchmarking as if absent; RAG and Rag at Scale
already cover that ground.

### R11. Add document intelligence for enterprise inputs

Priority 2 generally, Priority 1 for document-heavy roles. Create
`document-intelligence-deep-dive` after Multimodal and AI Data Engineering.

The current [Multimodal README](../multimodal-deep-dive/README.md) explicitly
leaves multi-page/scanned PDFs to further study. The data-engineering parser
requires an injected OCR adapter. Neither is an end-to-end lesson in recovering
meaning from a difficult document.

One big idea: structure and provenance are part of the extracted answer. Build
`examples/01_reading_order.py`, `examples/02_tables_and_units.py`,
`examples/03_ocr_or_vision.py`, `examples/04_page_evidence.py`, and
`hands_on/reconcile_invoices.py`. Compare native parsing, OCR, and vision on
rotated scans, merged cells, repeated headers, conflicting totals, and multiple
currencies. Preserve page and bounding-box provenance, parser version, and an
abstention path. Test arithmetic consistency and evidence alignment separately
from JSON schema validity.

Docling's document model is a useful implementation reference for structure and
layout metadata. Its availability does not eliminate the need to evaluate a
parser on the actual document family.
[Docling document model](https://docling-project.github.io/docling/concepts/docling_document/).

### R12. Compare inference effort and automated prompt search

Priority 2, partial coverage. Add
`prompt-engineering-deep-dive/examples/07_inference_budget.py` and
`hands_on/search_prompts.py`.

The provider dives already expose reasoning controls. The missing decision is
how to allocate effort: one stronger call, repeated candidates, a verifier,
self-consistency, or a tool-assisted workflow. Compare actual selected-answer
success, latency, and total cost under a shared budget. `pass@k` assumes a
successful candidate can be identified; it is not the success rate of an
imperfect selector. Keep the hidden answer key inaccessible to that selector.
[Research on test-time compute](https://arxiv.org/abs/2408.03314).

For prompt search, separate proposal, development scoring, and untouched final
evaluation. Bound the optimization budget and show overfitting to the development
set. A framework adapter can follow the existing Professional Tools comparison
style. The new lesson is optimization discipline, not another framework tour.

### R13. Bound the wider AI-engineering claim

Priority 1 as documentation, role-dependent as code. Add
`docs/PREREQUISITES.md` and `docs/NON-LLM-BASELINES.md`.

[ML Foundations](../ml-foundations-for-ai-engineers/README.md) deliberately omits
classical model surveys. That is sensible for model-facing LLM mechanics, but
the course should say what senior software knowledge it assumes: SQL,
transactions, HTTP/authentication, concurrency, queues, probability, testing,
and basic deployment.

The baseline guide should compare rules, lookup, TF-IDF plus a linear classifier,
embeddings plus a classifier, and generative output on one bounded task. Cover
class imbalance, train/serve skew, preprocessing leakage, temporal/group splits,
threshold choice, and cost of errors. Add a small runnable baseline in ML
Foundations if readers cannot make that comparison from the guide alone.

Recommenders, forecasting, classical computer vision, feature stores, distributed
training, CUDA kernel optimization, and foundation-model pretraining need
separate role tracks if the ambition truly includes all professional AI
engineering. They should not all become mandatory chapters in this LLM course.

### R14. Exercise privacy across every retained copy

Priority 2, partial coverage. Add
`ai-data-engineering-deep-dive/examples/11_privacy_lifecycle.py` and extend
Governance's vendor assessment.

Deletion, lineage, ACLs, PII screening, and backups are already taught. The
remaining exercise should follow one subject across source records, chunks,
conversation memory, response caches, traces, annotation exports, training data,
and an external-provider state handle. Delete or expire each applicable copy,
then restore an old backup and prove that the deletion is reapplied. Record
what cannot be verified locally and who owns that dependency.

Distinguish cache eviction from deletion, access revocation from erasure, and
removing training rows from reversing a completed training job. Use a synthetic
subject and local service doubles. Add current provider-specific retention and
regional-processing evidence only for the optional integration path.

Regulatory orientation already exists in Responsibility. Improve its maintenance
with official legal-text links, jurisdiction, covered role, effective date,
verification date, and a named reviewer. This audit does not independently
certify its jurisdiction-specific legal claims.

## What I would build, and in what order

| Order | Work | Why this order |
| --- | --- | --- |
| 1 | F1 through F8, then the bounded Models refresh | Remove misleading safety and measurement lessons before adding more material that depends on them. |
| 2 | Senior path, assessment, prerequisites, and companion practicum | Much of the missing senior experience already has code. Make it discoverable and assessable. |
| 3 | Product experimentation, enterprise SQL, and the data improvement cycle | These add decisions and task families that the current course treats least deeply. |
| 4 | Remote authorization and external-effect recovery | Close the remaining practical boundaries for enterprise agents. |
| 5 | Real post-training or real inference measurements, according to role | Deepen the chosen specialty without requiring expensive hardware for everyone. |
| 6 | Document intelligence, selective prediction, retrieval extensions, privacy, and prompt search | Add these against actual domain needs, with their prerequisites in place. |

For the smallest useful expansion, create only two new repositories initially:
`ai-product-engineering-deep-dive` and `structured-data-ai-deep-dive`. Most other
recommendations are examples, capstone extensions, or Markdown files. Add
Document Intelligence when serving document-heavy roles. I would defer a third
provider course, another agent framework survey, and a standalone GraphRAG course
until a measured learning need justifies them.

Each new dive should retain the existing teaching contract: README, textbook,
exercises, numbered examples, a capstone, setup checks, tests of the actual
failure modes, CI, and a declared cost boundary. Register it throughout parent
navigation, chapter map, choosing guide, glossary, career map, applicable safety
and responsibility docs, changelog, submodules, social assets, and offline
verification. A link alone is not course integration.

## Verification performed

At the audit baseline, the parent checkers resolved 873 relative Markdown links
and 196 referenced paths. The offline manifest covered all 25 submodules.
Those checks validate navigation and inventory, not model behavior or remote
URLs. The Markdown checker does not validate heading anchors.

The F2 probes executed the unmodified `score` function extracted from its source
AST, avoiding provider imports. The F3 probes executed the unmodified standalone
metrics module through `runpy`. No model was involved. These reproduce the
findings without paying for a stochastic comparison. They are not substitutes
for regression tests when the fixes are implemented.

The audit did not rerun every course, inspect every dependency version, verify
every current price, or reproduce the companion deployments. Findings about
absence mean absence of a dedicated teaching path in the inspected scope,
not proof that a word never appears anywhere in the project.
