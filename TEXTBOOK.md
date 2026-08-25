# The AI Engineering Textbook

*A companion to the [Deep Dives](README.md). Each dive's README is a lab manual that tells you what to run. The TEXTBOOK.md in each repo is the lecture that explains why the code looks the way it does. This page introduces the textbook and links every chapter.*

---

## Why this exists

If you have ever taken a science or engineering course, you know it comes in two halves. In the lab you build things with your hands and watch them work. In the lecture someone explains what you just saw and why it behaves that way. You need both halves. A lab with no theory is a sequence of steps you followed without understanding, and theory with no lab is trivia you cannot use.

This series has always been strong on the lab. Every dive is a repository you walk through, every concept is a small runnable program, and every section ends with something to run. What it lacked was the lecture, the connected story of why each piece exists, where it came from, and how it fits with everything else. The theory was in there. It was just scattered across README sections, code comments, and the odd insight you only caught if you happened to read closely.

The textbook is that missing half, gathered up and told as a story. Each chapter takes one dive and explains its subject the way a good teacher would. It starts from the problem the technique was invented to solve, traces a little of its history, builds the mental model you need, and stays honest about the tradeoffs and the places it breaks. There is very little math. There is a lot of "here is why this works, and here is the moment the industry figured it out." Read a chapter before its lab as a preview, or after it to connect what you built to the larger picture. Either order works. Doing both is the point.

## How to read it

The chapters follow the same sequence as the series. The eight core chapters build on each other, each one adding a layer until you are operating a real application end to end. The bonus chapters branch off where they are most useful, and you can read them whenever their subject comes up. If you are new, read in order. If you already know what you need, jump straight to it. Each chapter stands on its own and links to its neighbors.

If "what is a language model, really?" is still fuzzy, start with the primer in [HOW-LLMS-WORK.md](docs/HOW-LLMS-WORK.md), which sits underneath the whole textbook. [GLOSSARY.md](docs/GLOSSARY.md) defines every term the chapters assume, and [MODELS.md](docs/MODELS.md) covers the specific models and their prices. Once a system is real and has users, three operational pages sit alongside the chapters. [GOVERNANCE.md](docs/GOVERNANCE.md) holds the decision record, [INCIDENTS.md](docs/INCIDENTS.md) holds the runbooks, and [AI-UX.md](docs/AI-UX.md) covers the interface around a fallible model.

---

## The core path

The eight chapters that build on each other, in order. The thread runs from building the call, to asking it well, grounding it in knowledge, measuring it, letting it act, hardening it, and operating it.

| Ch | Chapter | The one idea |
|----|---------|--------------|
| 1 | [The API Call](openai-api-deep-dive/TEXTBOOK.md) | You send a list of messages and get back a message. Everything else is detail on that request. |
| 2 | [The Same Idea, a Second Dialect](claude-api-deep-dive/TEXTBOOK.md) | The same request done the Anthropic way, and what a second provider teaches you about the space of possible designs. |
| 3 | [The Prompt Is the Program](prompt-engineering-deep-dive/TEXTBOOK.md) | The model is fixed. You change what you ask and how you ask it, and that is most of the quality you will get. |
| 4 | [Retrieval, or Teaching a Model What It Never Learned](rag-deep-dive/TEXTBOOK.md) | A model can only answer from what is in its context window. RAG puts the right text there. |
| 5 | [Measurement, or How to Stop Shipping by Vibes](evals-deep-dive/TEXTBOOK.md) | If you cannot measure it you cannot improve it, so make quality a number you can rerun. |
| 6 | [The Loop That Acts](agents-deep-dive/TEXTBOOK.md) | An agent is a loop. The model picks a tool, you run it, you feed the result back, and you repeat until it is done. |
| 7 | [The Attack That Ships With the Feature](prompt-injection-deep-dive/TEXTBOOK.md) | Everything the model reads and writes is untrusted. Contain the blast radius. |
| 8 | [The Dozen Lines Around the Call](ai-in-production-deep-dive/TEXTBOOK.md) | The model call is one line. Production is the dozen lines that make it safe, cheap, observable, and reliable. |

## The bonus chapters

Standalone chapters that extend the core path. Each notes where it slots in.

| Ch | Chapter | The one idea | Slots in after |
|----|---------|--------------|----------------|
| 9 | [The Harness, or What Grows Around a Loop](agent-harness-deep-dive/TEXTBOOK.md) | Most agent work happens on top of a harness that adds hooks, permissions, sandboxing, subagents, and durable runs. | Agents (6) |
| 10 | [The Window, or Memory as a Policy](context-engineering-deep-dive/TEXTBOOK.md) | The model knows only what is in its window, so manage it with memory, compaction, and assembly. | Agents (6); pairs with RAG (4) |
| 11 | [More Than Text](multimodal-deep-dive/TEXTBOOK.md) | A multimodal model takes images and audio too. Put each one in the right slot and mind the cost. | The API chapters (1, 2) |
| 12 | [The Two Hundred Millisecond Problem](realtime-voice-deep-dive/TEXTBOOK.md) | Conversational voice is a low-latency, full-duplex loop with interruption, and every hundred milliseconds gets felt. | Multimodal (11) |
| 13 | [Teaching Behavior, Not Facts](fine-tuning-deep-dive/TEXTBOOK.md) | Fine-tuning changes how a model behaves, not what it knows, and you must prove it beat your baseline. | RAG (4) + Evals (5) |
| 14 | [A Protocol, Not a Product](mcp-deep-dive/TEXTBOOK.md) | Write a tool server once against the Model Context Protocol and any client can discover and use it. | Agents (6) |
| 15 | [The Model on Your Own Machine](local-models-deep-dive/TEXTBOOK.md) | An open-weight model speaks the same API, so running local is mostly an operations choice. | The API chapters (1, 2) |
| 16 | [The Next Six Weeks](observability-deep-dive/TEXTBOOK.md) | A prototype gets judged once. A production system gets judged continuously, so quality is a trend you watch. | Production (8); pairs with Evals (5) |
| 17 | [One Project, Every Lesson](deep-dive-capstone/TEXTBOOK.md) | The capstone, where the ideas from every chapter meet in one codebase and start arguing with each other. | Everything |
| 18 | [The Tools Everyone Uses](professional-tools-deep-dive/TEXTBOOK.md) | Rebuild each hand-written piece with the professional tool and measure both. An adoption decision is an experiment, and what you held constant is what makes it believable. | Everything |
| 19 | [The Corpus Is the Product](ai-data-engineering-deep-dive/TEXTBOOK.md) | A retrieval index is a disposable, derived view of source truth. Versions beat arrival order, permissions travel with the chunk, and a delete is a fact you keep. | RAG (4); before Production (8) |
| 20 | [The Model Is Not the Boundary](genai-security-deep-dive/TEXTBOOK.md) | The model is an untrusted principal. Identity, policy, provenance, isolation, budgets, release gates, and incident response all live in enforceable code around it. | Prompt Injection (7); before Production (8) |
| 21 | [The Seams Between the Parts](architecture-deep-dive/TEXTBOOK.md) | Every other chapter teaches a component. This one teaches where the boundaries between them go, and what each boundary costs once you insist on measuring it. | Production (8); pairs with Observability (16) |
| 22 | [The Memory-and-Queue Scheduler](inference-platform-deep-dive/TEXTBOOK.md) | An inference platform turns finite accelerator memory and compute into latency, throughput, reliability, and cost outcomes by scheduling KV state and queued token work. | Local Models (15); Production (8); Architecture (21) |
| 23 | [The Evidence a Release Owes](testing-and-delivery-deep-dive/TEXTBOOK.md) | A release is a claim, only as good as the independent evidence behind it. No check may take its expected answer from the input it judges, and no passing result counts unless it names the candidate it tested. | Evals (5) + Production (8); pairs with GenAI Security (20) |
| 24 | [The Numeric Contracts Beneath the Model](ml-foundations-for-ai-engineers/TEXTBOOK.md) | Shapes decide what can interact, loss decides what training rewards, attention decides what each token can read, and calibration, quantization, and retained state decide what an inference result means and costs. | The API chapters (1, 2); before Fine-tuning (13), Local Models (15), and Inference Platforms (22) |

---

## An aside, outside the numbering

One companion piece sits beside the book rather than inside it. It teaches no new
subject in AI engineering, only a change of language.

[Writing It in TypeScript](typescript-ai-deep-dive/TEXTBOOK.md) covers what happens to
everything above when the code ships in TypeScript instead of Python. Why a language
whose types are erased at runtime turns out to suit this work, where its compiler helps
more than Python's tooling does, and the one architectural difference that will take a
server down. It has no chapter number because it teaches no new idea. It translates the
ones already here and reports which of them the compiler will catch for you.

---

## A note on how these were written

The textbook holds itself to the same standard as the labs it accompanies, the one written down in [AUTHORING-LESSONS.md](docs/AUTHORING-LESSONS.md). The reader believes what is on the page, so what is on the page has to be worth believing. The chapters teach the honest tradeoff instead of the tidy-but-false claim, and they tell you where a technique fails as readily as where it works. Every number and result they cite came out of the labs, including the surprising ones and the unflattering ones. Sounding impressive was never the aim. Being clear, being right, and where possible being fun to read, was.

---

*Back to the [series overview](README.md) · [CHOOSING.md](docs/CHOOSING.md) is the decision guide · [GLOSSARY.md](docs/GLOSSARY.md) is the vocabulary*
