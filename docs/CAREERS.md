# Careers: what each dive is called on a job description

This series has one stated goal, which is to get a pre-AI software engineer to the
point where they would clear an AI Engineer bar. But you built everything from scratch,
so the work goes by different names in job postings, résumés, and interviews than it
does here. This page is the translation. Each dive mapped to the vocabulary a hiring
manager uses, and to the industry tools that productionize what you built by hand.

> **The pitch that lands in interviews.** "I built X from scratch, so I understand what
> the framework is doing" beats "I've used the framework." A candidate who hand-wrote an
> agent loop can reason about why a run took twelve steps. One who only called
> `AgentExecutor.run()` cannot. Lead with the thing you built and name the tool second.
> That is the whole reason this series builds from scratch. See the "but everyone uses
> agents" note in [CHOOSING.md](CHOOSING.md).

Find the dive you worked through, read the résumé line you can now honestly write, and
skim the tools so you recognize them in a posting and can say "that's the productionized
version of the retriever, eval, or loop I built."

---

## The map

### 1–2. OpenAI API / Claude API
- **Job-description phrases:** "integrate LLM APIs," "function calling / tool use," "streaming responses," "token/cost management," "structured outputs."
- **Industry tools:** OpenAI SDK, Anthropic SDK, the Vercel AI SDK, LiteLLM (multi-provider routing).
- **Résumé line:** *"Built LLM-backed features against the OpenAI and Anthropic APIs: tool calling, streaming, structured JSON output, and per-request cost/token budgeting."*
- **Interview:** you can explain the stateless request/response model, why "memory" is just resending messages, and how tool calling actually works (the model *requests*, your code *executes*).

### 3. Prompt Engineering
- **Job-description phrases:** "prompt design/optimization," "few-shot," "chain-of-thought," "structured extraction," "reduce hallucination."
- **Industry tools:** prompt templates, DSPy (programmatic prompt optimization), `guidance`/`outlines` (constrained decoding), provider structured-output modes.
- **Résumé line:** *"Designed and iterated production prompts (few-shot, chain-of-thought, role and format control), measured against an eval set rather than by feel."*
- **Interview:** you can name when a better prompt fixes the problem vs when you need to climb to RAG or fine-tuning ([CHOOSING.md](CHOOSING.md)).

### 4. RAG
- **Job-description phrases:** "retrieval-augmented generation," "semantic/vector search," "embeddings," "grounding & citations," "reduce hallucination with retrieval."
- **Industry tools:** pgvector, Pinecone, Weaviate, Qdrant, Chroma, FAISS / hnswlib (the ANN index you built by hand in §15); LlamaIndex / LangChain retrievers; Cohere / Voyage rerankers.
- **Résumé line:** *"Built a RAG pipeline end to end (chunking, embeddings, hybrid + reranked retrieval, grounded generation with citations) and measured retrieval (hit-rate, MRR) and answer quality separately."*
- **Interview:** you can explain the exact-vs-approximate (brute force vs IVF/HNSW) recall-for-speed tradeoff and why chunking and reranking matter more than the vector DB choice.

### 5. Evals
- **Job-description phrases:** "LLM evaluation," "offline & online evals," "LLM-as-judge," "A/B testing," "quality regression gates."
- **Industry tools:** Braintrust, promptfoo, Langfuse, Ragas, OpenAI Evals, DeepEval, Arize Phoenix.
- **Résumé line:** *"Stood up an evaluation harness (judge-bias controls, paired intervals, power planning, and multiplicity-aware release thresholds) and gated releases on reproducible evidence in CI."*
- **Interview:** most candidates are weakest here, so lead with it. You can explain why "it seems better" ships regressions, why a statistically detectable gain may not matter, and why repeated looks or many metrics need a predeclared error budget.

### 6. Agents
- **Job-description phrases:** "agentic systems," "tool-calling agents," "multi-step/autonomous workflows," "workflow vs agent."
- **Industry tools:** LangGraph, the OpenAI Agents SDK, CrewAI, AutoGen, LlamaIndex agents.
- **Résumé line:** *"Built tool-using agents (the loop, multi-tool routing, step limits, error recovery, human-in-the-loop approval, tracing) and knew when a fixed workflow was the better, cheaper choice."*
- **Interview:** you hand-wrote the loop, so you can debug why an agent takes too many steps and explain the workflow-vs-agent decision from experience.

### Agent Harnesses (bonus)
- **Job-description phrases:** "build on the Agent SDK / hosted agents," "agent orchestration," "multi-agent / parallel orchestration," "tool sandboxing," "permission policies / guardrails," "subagents," "computer use," "headless/agentic automation," "durable/resumable agents," "checkpointing / stateful workflows," "human-in-the-loop steering," "workflow graphs (LangGraph)."
- **Industry tools:** the Claude Agent SDK, OpenAI Agents SDK, Claude Code, Managed/hosted agents, LangGraph (graph orchestration + checkpointers), computer-use tools, sandbox runtimes (E2B, Modal, Firecracker/gVisor), and durable-execution engines (Temporal, Inngest, Restate).
- **Résumé line:** *"Built agents on top of an agent harness (permission policies, hooks/guardrails, sandboxed tool execution, subagents, headless runs, durable checkpoint/resume, parallel fan-out orchestration, mid-run steering, and graph control flow) and could articulate when to adopt the SDK vs hand-roll the loop."*
- **Interview:** this answers the now-standard question head on. "You have a working loop. When do you throw it away for the SDK, and what does it give you?" You built every join (hooks, policy, sandbox, subagents, headless, checkpoint and resume, parallel orchestration, steering, graph routing), so you know exactly what the SDK hardens, including the orchestration and durable-execution machinery that starts to matter the moment an agent fans out, runs long, or needs steering.

### 7. Prompt Injection & Guardrails
- **Job-description phrases:** "LLM/AI security," "guardrails," "prompt-injection defense," "red-teaming," "content moderation," "PII handling."
- **Industry tools:** Llama Guard, NeMo Guardrails, Guardrails AI, Lakera, Rebuff, provider moderation endpoints.
- **Résumé line:** *"Hardened LLM features against prompt injection and unsafe tool use by treating model I/O as untrusted, containing blast radius, and adding input and output guardrails."*
- **Interview:** unusually deep for a candidate. You can discuss why direct secret-leak attacks fail while task-aligned indirect injection lands, and what defense in depth buys you.

### GenAI Security (bonus)
- **Job-description phrases:** "AI/ML security engineering," "AI threat modeling," "secure agentic systems," "model and data supply-chain security," "AI red teaming," "OWASP LLM Top 10," "NIST AI RMF," "least privilege / policy as code," "sandboxing," "AI incident response."
- **Industry tools:** OPA or Cedar-style policy engines; Sigstore/Cosign and SLSA provenance; garak and promptfoo-style adversarial suites; SBOM and dependency scanners; egress proxies; container or microVM isolation such as gVisor and Firecracker; the organization's SIEM and incident platform.
- **Résumé line:** *"Built a deterministic GenAI security control plane covering the full OWASP LLM Top 10: threat models, sensitive-data boundaries, signed artifact provenance, poisoning gates, sink validation, trusted agent identity and approvals, tenant-safe retrieval, SSRF and sandbox policy, denial-of-wallet budgets, adversarial release gates, and rehearsed incident recovery."*
- **Interview:** you can move beyond "we added guardrails" and draw where authority really lives. You can explain why a tool schema is not authorization, why a checksum is not provenance, why post-filtered retrieval leaks, why an allowlisted hostname can still reach metadata, why a Python wrapper is not a sandbox, and why a block-everything red-team result fails the release. This is senior-level evidence because the capstone proves the naive boundary fails, the hardened boundary passes without losing benign utility, and recovery is tied to a regression gate.

### 8. Production (LLMOps)
- **Job-description phrases:** "LLMOps," "observability," "cost/latency optimization," "reliability (retries, fallbacks, circuit breakers)," "caching," "prompt versioning," "eval gates."
- **Industry tools:** Langfuse, Helicone, LangSmith, Arize Phoenix, OpenTelemetry, semantic caches (GPTCache), feature-flag/prompt-registry tooling.
- **Résumé line:** *"Operated LLM features in production: structured tracing, per-request cost budgets, retries/fallbacks, response caching, versioned prompts behind eval gates."*
- **Interview:** you can enumerate the dozen concerns around the model call, which is what separates "I called an API" from "I ran it for real users."

### Observability (bonus)
- **Job-description phrases:** "LLM observability / monitoring," "data & concept drift," "model performance monitoring," "quality/regression monitoring," "alerting & on-call," "SLOs / error budgets."
- **Industry tools:** Langfuse, Arize (Phoenix), Evidently, NannyML, WhyLabs, Grafana/Prometheus, OpenTelemetry, PagerDuty; continuous LLM-as-judge scorers.
- **Résumé line:** *"Built LLM observability from logs: operational metrics (p95 latency, cost/request, refusal rate), input/embedding drift detection, a sampled LLM-as-judge for quality regressions, and z-score + persistence alerting tuned to catch incidents without alert fatigue."*
- **Interview:** you can explain why LLM monitoring differs from classic tabular MLOps (no feature vector, labels rarely arrive), why quality has to be sampled rather than measured, and the false-alarm-versus-detection-lag tradeoff that alerting cannot escape. Pairs directly with Evals and Production.

### Context Engineering (bonus)
- **Job-description phrases:** "context management," "conversation memory," "prompt caching / cost optimization," "long-context handling."
- **Industry tools:** provider prompt caching, mem0, Zep, LangMem, context-compaction features in the SDKs.
- **Résumé line:** *"Managed model context under a token budget: sliding-window and summary (compaction) memory, cross-session long-term recall, and cache-aware assembly, trading tokens against the prompt-cache bill deliberately."*
- **Interview:** you can explain the counterintuitive result that compaction can raise cost by breaking the prompt cache (§10).

### Multimodal (bonus)
- **Job-description phrases:** "vision / document AI," "OCR / structured extraction," "speech-to-text / text-to-speech," "multimodal."
- **Industry tools:** GPT-4o / Claude vision, Whisper / Deepgram (STT), ElevenLabs / OpenAI TTS, document extraction (Textract, Document AI), CLIP-style image embeddings, native PDF input.
- **Résumé line:** *"Built multimodal features: vision-based document extraction to structured JSON (screenshot and native PDF), speech-to-text and text-to-speech, and image-token cost control."*
- **Interview:** you can reason about image token cost, and native-PDF vs screenshot extraction as the enterprise default.

### Realtime Voice (bonus)
- **Job-description phrases:** "voice AI," "conversational voice agents," "realtime / low-latency speech," "speech-to-speech," "telephony / IVR."
- **Industry tools:** the OpenAI Realtime API, LiveKit, Pipecat, Vapi, Retell, Deepgram, ElevenLabs; WebRTC / WebSocket transports.
- **Résumé line:** *"Built realtime voice agents: turn detection, barge-in/interruption handling, latency budgeting, and the STT->LLM->TTS vs speech-to-speech architecture tradeoff."*
- **Interview:** you can talk about the sub-second latency budget, why barge-in needs full-duplex audio and fast cancellation, and when to pick a pipeline over speech-to-speech.

### ML Foundations for AI Engineers (bonus)
- **Job-description phrases:** "ML fundamentals," "PyTorch," "model internals," "transformers and attention," "training and inference," "calibration," "quantization."
- **Industry tools:** NumPy, PyTorch autograd and scaled-dot-product attention, reliability diagrams, hardware-specific quantizers, and runtime memory profilers.
- **Résumé line:** *"Built and tested the numeric path beneath an LLM call: tensor shape contracts, stable softmax and cross-entropy, gradient checks, masked multi-head attention, a tiny causal transformer, sampling controls, held-out calibration, measured quantization drift, and component-level training and inference memory accounts."*
- **Interview:** you can trace a token from embedding to logits, explain why causal masking needs a counterfactual test, keep softmax probability separate from calibrated confidence, and refuse to turn a bit width or weights-only byte count into an unsupported speed or capacity claim.

### Fine-tuning (bonus)
- **Job-description phrases:** "model fine-tuning," "SFT / preference tuning (DPO) / RFT," "LoRA / PEFT," "distillation," "dataset curation."
- **Industry tools:** Hugging Face `trl`/`peft`/`transformers`, Axolotl, Unsloth, Together / Fireworks fine-tuning, MLX on Apple silicon. (OpenAI is winding self-serve fine-tuning down through 2026 into January 2027, so hosted SFT on the big closed providers is a shrinking skill; the open-weight LoRA path is where this work is moving.)
- **Résumé line:** *"Fine-tuned models for behavior: built and validated the dataset, ran the job, and gated on a held-out win-rate vs the base model, and knew when a prompt or RAG was the cheaper fix."*
- **Interview:** you can place SFT vs preference tuning (DPO) vs reinforcement fine-tuning (RFT), and explain "the dataset is the product" plus the eval gate.

### MCP (bonus)
- **Job-description phrases:** "Model Context Protocol," "tool servers / integrations," "connect LLMs to external systems."
- **Industry tools:** the MCP SDK, hosted/remote MCP servers, provider MCP connectors.
- **Résumé line:** *"Built an MCP server and client from scratch (JSON-RPC tool discovery and invocation) and integrated tools/data into an agent over the protocol."*
- **Interview:** you can explain MCP as "a tool is a name + description + schema, spoken over a protocol instead of an import."

### Local Models (bonus)
- **Job-description phrases:** "open-weight / self-hosted inference," "on-prem / private LLMs," "quantization," "GPU cost/throughput."
- **Industry tools:** Ollama, vLLM, llama.cpp, Hugging Face TGI, LM Studio, SGLang; GGUF/AWQ/GPTQ quantization.
- **Résumé line:** *"Ran open-weight models locally/self-hosted (Ollama, vLLM), reasoned about quantization tradeoffs, and treated local vs API as an ops decision (privacy, cost, control)."*
- **Interview:** you can frame "local" as mostly an ops choice and discuss the quantization quality/size tradeoff.

### Inference Platform Engineering (bonus)
- **Job-description phrases:** "LLM inference / serving platform," "GPU fleet orchestration," "model serving performance," "capacity planning," "distributed inference," "admission control / load shedding," "SLOs and autoscaling."
- **Industry tools:** vLLM, SGLang, Hugging Face TGI, NVIDIA Triton/TensorRT-LLM, Ray Serve, Kubernetes device plugins and custom-metric autoscaling, Prometheus/Grafana, GPU/fabric discovery and scheduling.
- **Résumé line:** *"Designed an LLM inference control plane from memory and workload evidence: sized weights and KV cache, measured TTFT/TPOT/token throughput, evaluated batching/caching/quantization/speculation, selected TP/PP/DP/EP layouts, placed GPU groups, bounded overload, scaled queued token work, gated canaries, and planned burst capacity and cost."*
- **Interview:** you can explain why weight fit is not service fit, why four-bit is not a throughput claim, when tensor parallelism should stay inside a fast-link domain, why CPU is a poor serving scaler, and how a requirement survives removal of the test case that was meant to prove it. The capstone produces the deciding control for every fleet claim and fails under independent workload, placement, shedding, and rollout counterfactuals.

### Professional Tools (bonus)
- **Job-description phrases:** "experience with LangChain/LangGraph/LlamaIndex," "LLM observability (Langfuse)," "eval frameworks," "framework evaluation / build-vs-buy," "production LLM tooling."
- **Industry tools:** the whole tool column of this page, used rather than name-dropped. LiteLLM, Instructor, LlamaIndex, DeepEval, LangGraph, Llama Guard, Guardrails AI, Langfuse.
- **Résumé line:** *"Evaluated and adopted production LLM frameworks against hand-rolled baselines: ported each primitive to the tool, measured both on one held-constant eval, and made build-vs-buy calls from data (what the tool automated, what it hid, when to hand-roll)."*
- **Interview:** this dive turns every "name the tool" line above into "I've used it, and here's exactly what it does and where it bit." From measurement, you can say that a metric library brought its own definition of the metric, that a framework dropped a citation contract while every score stayed green, that a provider router failed without a sound on one route, and that an observability platform priced a run to the cent from tokens alone. And you can say that "should we adopt this?" is an experiment whose credibility is whatever you held constant. Hard to beat for build-vs-buy and staff-level "should we take on this dependency?" conversations.

### Architecture (bonus)
- **Job-description phrases:** "system design for AI products," "LLM application architecture," "multi-tenant RAG," "design reviews / ADRs," "staff engineer," "scalability and reliability of ML services."
- **Industry tools:** the decisions rather than the products. Job queues and load shedding, circuit breakers, shared session stores, dedicated inference tiers (vLLM, TGI, Ollama), ingest pipelines, canary and shadow deploys, per-tenant retrieval filters.
- **Résumé line:** *"Owned the architecture of an LLM application end to end: measured each structural decision (state placement, request shape, model tiering, guard placement, degradation, index freshness, rollout, tenant isolation) against a reproducible stressor and documented them as ADRs with the conditions that would reverse them."*
- **Interview:** this is the dive that gives you numbers instead of opinions in a design review. You can say that in-process conversation state scored 62% correct at four workers, that a fallback took availability from 0% to 100% while correctness fell to 17%, that an output guard on a stream detected every violation and prevented none, that filtering permissions after the model call leaked another tenant's contract terms verbatim, and that a circuit breaker saved 2.9x wall clock while moving p95 by nothing at all. The strongest single dive for staff-level and system-design rounds, because every claim comes with what would flip it.

### Testing & Delivery (bonus)
- **Job-description phrases:** "CI/CD for ML," "release engineering," "test strategy," "SDLC and quality gates," "supply-chain security," "progressive delivery / canary deploys," "SRE," "build and release provenance."
- **Industry tools:** pytest and Hypothesis, `unittest.mock` specs and autospeccing, VCR-style contract fixtures, Locust/k6, GitHub Actions matrices, Dependabot and dependency review, CodeQL, `pylock.toml` (PEP 751) and pip-tools/uv, Argo Rollouts and Flagger, feature flags, Sigstore and SLSA provenance.
- **Résumé line:** *"Built a release-evidence pipeline for an AI system: declared required evidence independently of the checks that ran, held SDK contracts separate from recorded fixtures, proved invariants with property tests and shrinking, derived load evidence with explicit units, tested after-commit retry and idempotency, gated on the artifact tuple, locked dependencies to PEP 751, executed the support promise in CI, bound scanner findings to an independent severity policy, and staged shadow/canary rollout with a verified rollback."*
- **Interview:** you can explain why a passing test suite is not a release decision, and name the failure shape that proves it, which is a check that reads its expected answer out of the input it judges. You can say that `requires-python = ">=3.11"` is metadata until CI runs on 3.11, that a lost response after commit is what makes a blind retry duplicate a charge, that `unittest` exits green on zero discovered tests, that a green result is worthless unless it names the candidate digest and revision it tested, and that a metamorphic assertion over floats has to state its tolerance. The capstone runs twelve real decisions over one candidate and flips under eight independent perturbations, so every claim it makes has a counterfactual behind it. Strongest dive for release-engineering, SRE, and "how would you ship this safely?" rounds.

---

## Turning the whole series into a résumé

You don't list thirteen line items. You synthesize. A strong summary bullet:

> *"AI engineer: built RAG, tool-using agents, and multimodal features against the
> OpenAI and Anthropic APIs; stood up LLM evaluation and observability; hardened
> against prompt injection; and operated it all in production with cost, caching,
> and reliability controls."*

Then keep the per-dive lines above as detail bullets for the specific roles you are
targeting. In the interview, whatever they dig into, the move is the same. Describe the
thing you built, then name the tool that productionizes it.

*(The tool names here are examples of their category, current as of writing, and they
turn over fast. What does not turn over is the thing underneath, which is why this
series teaches that.)*
