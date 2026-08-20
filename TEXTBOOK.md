# The AI Engineering Textbook

*A companion to the [Deep Dives](README.md). Where each dive's README is a lab manual that tells you what to run, the TEXTBOOK.md in each repo is the lecture: the what, when, where, why, and how behind the code. This page introduces the textbook and links every chapter.*

---

## Why this exists

If you have ever taken a science or engineering course, you know the two halves of it. There is the lab, where you build things with your hands and watch them work, and there is the lecture and its textbook, where someone explains what you just saw and why it behaves the way it does. You need both. The lab without the theory is a sequence of steps you followed without understanding; the theory without the lab is trivia you cannot use.

This series has always been strong on the lab. Every dive is a repository you walk through, every concept is a small runnable program, and every section ends with something to run. What the series lacked was the lecture, the connected story that explains why each piece exists, where it came from, and how it fits with everything else. The theory was there, but scattered across README sections, code comments, and the moments of insight you only got if you happened to read closely.

The textbook is that missing half, gathered and told as a story. Each chapter takes one dive and explains its subject the way a good teacher would: starting from the problem the technique was invented to solve, tracing a little of its history, building the mental model you need, and being honest about the tradeoffs and the places it breaks. There is very little math. There is a lot of "here is why this works, and here is the moment the industry figured it out." You can read a chapter before doing its lab as a preview, or after as a way of connecting what you built to the larger picture. Either order works; doing both is the point.

## How to read it

The chapters follow the same sequence as the series. The eight core chapters build on each other, each adding a layer until you are operating a real application end to end. The bonus chapters branch off where they are most useful and can be read whenever their subject comes up. If you are new, read in order. If you know what you need, jump to it; each chapter stands on its own while linking to its neighbors.

If the question "what *is* a language model, really?" is still fuzzy, start with the primer in [HOW-LLMS-WORK.md](HOW-LLMS-WORK.md), which sits underneath the whole textbook. The [GLOSSARY.md](GLOSSARY.md) defines every term the chapters assume, and [MODELS.md](MODELS.md) covers the specific models and their prices. Once a system is real and has users, three operational pages sit alongside the chapters: [GOVERNANCE.md](GOVERNANCE.md) for the decision record, [INCIDENTS.md](INCIDENTS.md) for the runbooks, and [AI-UX.md](AI-UX.md) for the interface around a fallible model.

---

## The core path

The eight chapters that build on each other, in order. The thread runs: build the call, ask it well, ground it in knowledge, measure it, let it act, harden it, and operate it.

| Ch | Chapter | The one idea |
|----|---------|--------------|
| 1 | [The API Call](openai-api-deep-dive/TEXTBOOK.md) | You send a list of messages and get back a message. Everything else is detail on that request. |
| 2 | [The Same Idea, a Second Dialect](claude-api-deep-dive/TEXTBOOK.md) | The same request, the Anthropic way, and what a second provider teaches you about the design space. |
| 3 | [The Prompt Is the Program](prompt-engineering-deep-dive/TEXTBOOK.md) | The model is fixed; you change what you ask and how, and that is most of the quality you will get. |
| 4 | [Retrieval, or Teaching a Model What It Never Learned](rag-deep-dive/TEXTBOOK.md) | A model can only answer from what is in its context window; RAG puts the right text there. |
| 5 | [Measurement, or How to Stop Shipping by Vibes](evals-deep-dive/TEXTBOOK.md) | If you cannot measure it, you cannot improve it, so make quality a number you can rerun. |
| 6 | [The Loop That Acts](agents-deep-dive/TEXTBOOK.md) | An agent is a loop: the model picks a tool, you run it, you feed the result back, until it is done. |
| 7 | [The Attack That Ships With the Feature](prompt-injection-deep-dive/TEXTBOOK.md) | Treat everything the model reads and writes as untrusted, and contain the blast radius. |
| 8 | [The Dozen Lines Around the Call](ai-in-production-deep-dive/TEXTBOOK.md) | The model call is one line; production is the dozen lines that make it safe, cheap, observable, and reliable. |

## The bonus chapters

Standalone chapters that extend the core path. Each notes where it slots in.

| Ch | Chapter | The one idea | Slots in after |
|----|---------|--------------|----------------|
| 9 | [The Harness, or What Grows Around a Loop](agent-harness-deep-dive/TEXTBOOK.md) | Most agent work is building *on* a harness: hooks, permissions, sandboxing, subagents, durable runs. | Agents (6) |
| 10 | [The Window, or Memory as a Policy](context-engineering-deep-dive/TEXTBOOK.md) | The model knows only what is in its window, so manage it: memory, compaction, assembly. | Agents (6); pairs with RAG (4) |
| 11 | [More Than Text](multimodal-deep-dive/TEXTBOOK.md) | A multimodal model takes images and audio too; put the right modality in the right slot, mind the cost. | The API chapters (1, 2) |
| 12 | [The Two Hundred Millisecond Problem](realtime-voice-deep-dive/TEXTBOOK.md) | Conversational voice is a low-latency, full-duplex loop with interruption; every hundred milliseconds is felt. | Multimodal (11) |
| 13 | [Teaching Behavior, Not Facts](fine-tuning-deep-dive/TEXTBOOK.md) | Fine-tuning changes how a model behaves, not what it knows, and you must prove it beat your baseline. | RAG (4) + Evals (5) |
| 14 | [A Protocol, Not a Product](mcp-deep-dive/TEXTBOOK.md) | The Model Context Protocol: write a tool server once, and any client can discover and use it. | Agents (6) |
| 15 | [The Model on Your Own Machine](local-models-deep-dive/TEXTBOOK.md) | An open-weight model speaks the same API, so "local" is mostly an operations choice. | The API chapters (1, 2) |
| 16 | [The Next Six Weeks](observability-deep-dive/TEXTBOOK.md) | A prototype is judged once; a production system is judged continuously, so quality is a trend you watch. | Production (8); pairs with Evals (5) |
| 17 | [One Project, Every Lesson](deep-dive-capstone/TEXTBOOK.md) | The capstone, where the ideas from every chapter meet in one codebase and collide. | Everything |
| 18 | [The Tools Everyone Uses](professional-tools-deep-dive/TEXTBOOK.md) | Rebuild each from-scratch primitive with the professional tool and measure both: an adoption decision is an experiment, and its credibility is what you held constant. | Everything |
| 19 | [The Corpus Is the Product](ai-data-engineering-deep-dive/TEXTBOOK.md) | A retrieval index is a disposable, derived view of source truth, so versions beat arrival order, permissions travel with the chunk, and deletes are facts you keep. | RAG (4); before Production (8) |
| 20 | [The Model Is Not the Boundary](genai-security-deep-dive/TEXTBOOK.md) | Treat the model as an untrusted principal: identity, policy, provenance, isolation, budgets, release gates, and incident response live in enforceable code around it. | Prompt Injection (7); before Production (8) |
| 21 | [The Seams Between the Parts](architecture-deep-dive/TEXTBOOK.md) | Every other chapter teaches a component; this one teaches where the boundaries between them go, and what each boundary costs when you insist on measuring it. | Production (8); pairs with Observability (16) |
| 22 | [The Memory-and-Queue Scheduler](inference-platform-deep-dive/TEXTBOOK.md) | An inference platform turns finite accelerator memory and compute into latency, throughput, reliability, and cost outcomes by scheduling KV state and queued token work. | Local Models (15); Production (8); Architecture (21) |
| 23 | [The Evidence a Release Owes](testing-and-delivery-deep-dive/TEXTBOOK.md) | A release is a claim, and the claim is only as good as the independent evidence behind it: no check may take its expected answer from the input it judges, and no passing result counts unless it names the candidate it tested. | Evals (5) + Production (8); pairs with GenAI Security (20) |

---

## An aside, outside the numbering

One companion piece sits beside the book rather than inside it, because it is not
a subject in AI engineering but a change of language.

[**Writing It in TypeScript**](typescript-ai-deep-dive/TEXTBOOK.md) covers what
happens to everything above when the code ships in TypeScript instead of Python:
why a language whose types are erased at runtime turns out to suit this work,
where its compiler helps more than Python's tooling does, and the single
architectural difference that will take a server down. It has no chapter number
because it teaches no new idea; it translates the ones already here, and reports
which of them the compiler will help you with.

---

## A note on how these were written

The textbook holds itself to the same standard as the labs it accompanies, the one written down in [AUTHORING-LESSONS.md](AUTHORING-LESSONS.md): the reader believes what is on the page, so what is on the page has to be worth believing. The chapters teach the honest tradeoff over the tidy-but-false claim. They tell you where techniques fail, not just where they shine. When they cite a number or a result, it is one the labs actually produced, including the surprising and the unflattering ones. The goal is not to make the material sound impressive. It is to make it clear, accurate, and, where possible, enjoyable to read.

---

*Back to the [series overview](README.md) · The decision guide: [CHOOSING.md](CHOOSING.md) · The vocabulary: [GLOSSARY.md](GLOSSARY.md)*
