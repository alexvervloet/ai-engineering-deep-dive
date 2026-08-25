# Capstone: Ask the Dives

One project that exercises the whole series. A codebase Q&A tool, built step by step,
one deep dive at a time. You point it at a directory of code and docs, ask questions in
plain English, and get answers with `file:line` citations. Its default corpus is this
repo, which makes the capstone self-referential. The course answers questions about
itself, and you have read everything without writing any of it, so you know the ground
truth well enough to eval it honestly.

Working name: `askrepo`. Rename at will. The roadmap doesn't care.

> Two ways to pitch it. To a user, "a chat interface over any codebase". To yourself,
> "RAG, agentic retrieval, evals, guardrails, and ops around one corpus".

---

## The shape (decisions made up front)

- **Local-first, not hosted.** `askrepo index <path>` + `askrepo ask "…"` against
  any local directory. No uploads, no accounts, no multi-tenancy. A repo you cloned
  from the internet is exactly as untrusted as an upload, so the security story
  (step 6) survives intact, without turning the capstone into a product. Hosted
  upload is a stretch goal, not a step.
- **Its own git repo inside the series directory**, at `./deep-dive-capstone/`. Every
  dive already follows that pattern, being a self-contained repo and eventually a
  submodule. The capstone gets its own clean linear history and tags, and clones of
  the series carry it along.
- **Eval runs record a corpus manifest.** Separate histories mean a capstone tag
  cannot pin the corpus state, so the eval runner (v04) stamps each corpus repo's
  HEAD SHA into every run and into `baseline.run.json`. That makes the numbers
  reproducible against any corpus rather than only this one. Once the dives become
  submodules, a superproject tag pins every SHA at once as well.
- **One linear history, one tag per step.** `main` is always the latest, and
  `git checkout v03-rag` shows the project as it stood after the RAG step. No
  long-lived per-step branches, because they rot the first time you fix something
  early. Optional dives do get feature branches, since they are genuinely parallel.
  See [Branch-off features](#branch-off-features).
- **House rules apply.** Provider-agnostic (`PROVIDER=openai|anthropic` in `.env`,
  same pattern as every dive's `providers.py`), keys in the keychain via `secrun`
  ([SECRETS.md](SECRETS.md)), a `check_setup.py`, and a first runnable thing that is
  offline and free, using a mock provider borrowed from the Production dive.
- **The output is the argument.** Every step's definition of done is something you can
  run and see, and eval numbers get reported as measured, unflattering ones included.
  [AUTHORING-LESSONS.md](AUTHORING-LESSONS.md) governs here.

## Final layout (where you end up)

```
deep-dive-capstone/        # its own git repo, like every dive
├── README.md              # the story of the project, step by step
├── check_setup.py
├── requirements.txt
├── .env.example           # PROVIDER / MODEL only, no keys
├── askrepo/
│   ├── cli.py             # index / ask / chat / eval / redteam subcommands
│   ├── providers.py       # v01: OpenAI + Anthropic + mock behind one interface
│   ├── prompts.py         # v02: system prompt, citation format, few-shots
│   ├── indexer.py         # v03: walk a repo, chunk md + py, embed, store
│   ├── retrieve.py        # v03: hybrid (vector + keyword) retrieval
│   ├── answer.py          # v03: retrieve → prompt → answer with citations
│   ├── agent.py           # v05: tool-loop retrieval (grep / read / list)
│   ├── guardrails.py      # v06: untrusted-content defenses, output checks
│   ├── ops.py             # v07: cache, cost meter, retries, structured logs
│   └── mcp_server.py      # branch: expose ask/search as MCP tools
├── evals/
│   ├── golden.jsonl       # v04: the question set (see design below)
│   ├── run_evals.py       # v04: runner + scorers + judge
│   ├── redteam.jsonl      # v06: injection fixtures
│   └── baseline.run.json  # v04: frozen numbers you must beat, not vibes
└── fixtures/
    └── evil-repo/         # v06: a tiny corpus with planted injections
```

---

## The steps

| Tag | Dive exercised | What exists when it's done |
|-----|----------------|----------------------------|
| `v00-scaffold` | (house style) | CLI skeleton, mock provider, `check_setup.py`; works offline |
| `v01-chat` | OpenAI API (1) · Claude API (2) | Real streamed answers from either provider, one flag apart |
| `v02-prompt` | Prompt Engineering (3) | System prompt with citation discipline; declines off-topic asks |
| `v03-rag` | RAG (4) | Index this repo, ask, and get cited answers back. The demo moment |
| `v04-evals` | Evals (5) | Golden set + runner + frozen baseline numbers |
| `v05-agent` | Agents (6) | Agentic retrieval, and a measured RAG-vs-agent verdict |
| `v06-hardened` | Prompt Injection (7) | Red-team suite; attack success rate before/after defenses |
| `v07-production` | Production (8) | Caching, cost budget, retries, logs; the ops story |

### v00-scaffold: prove it runs before it thinks

`cli.py` with `ask` wired to a **mock provider** that returns a canned answer.
`check_setup.py` in the house pattern. No API key exists yet anywhere in the story.

**Done when:** `python -m askrepo ask "hello"` answers offline, and
`check_setup.py` passes on a fresh clone with no key.

### v01-chat: the API call (dives 1–2)

`providers.py` with three backends (OpenAI, Anthropic, mock) behind one
`complete(messages) -> stream` interface. Lift the shape from
`agents-deep-dive/agent/providers.py`; every dive repeats it because it works.

**Done when:** the same question streams a real answer under `PROVIDER=openai` and
`PROVIDER=anthropic`, run via `secrun`, and the mock still passes with no key.

### v02-prompt: teach it its job (dive 3)

`prompts.py` holds the system prompt that defines the contract. Answer only from
provided context, cite `path:line` for every claim, and say "not in this corpus" when it
isn't. Add few-shot examples of good cited answers. At this tag there is no retrieval
yet, so you paste context by hand, and that is the lesson. The prompt contract is
testable before the pipeline exists.

**Done when:** given a pasted chunk it cites that chunk, and asked something outside
the chunk it declines instead of improvising. Keep five or six before-and-after
transcripts as a prompt regression file. They become eval seeds in v04.

### v03-rag: the heart (dive 4)

`indexer.py` walks a directory, chunks markdown by heading and Python by
function/class (adapt `rag-deep-dive/rag/chunking.py` + `loader.py`), embeds, and
stores (`rag/store.py`). `retrieve.py` does hybrid vector + keyword retrieval
(`rag/keyword.py`). Remember what ex07 of that dive actually showed. Hybrid is not
strictly better, so keep the blend weight configurable and let v04 measure it rather
than asserting it. `answer.py` glues retrieve, the v02 prompt, and the provider
together, printing cost per question using the token math from the API dives.

**Done when:** `askrepo index .. && askrepo ask "which dive covers barge-in?"`
answers with a citation into `realtime-voice-deep-dive/` that resolves to a real file
and line. The corpus is the parent directory, which now contains the capstone itself.
Decide here whether the indexer excludes its own directory or leans into the
self-reference, because it changes what the golden set can ask.

### v04-evals: numbers before opinions (dive 5)

The golden set (design below) plus `run_evals.py`, built on the patterns in
`evals-deep-dive/evals/` (`runner.py`, `scorers.py`, `judges.py`, `metrics.py`).
Freeze the first honest run as `baseline.run.json`, the same way the evals dive does.
This lands before the agent step on purpose. The whole point of v05 is a comparison, and
a comparison needs a yardstick that predates both contestants.

**Done when:** one command prints retrieval hit@5, citation precision, judged
correctness, cost, and latency for the RAG pipeline. Every run, `baseline.run.json`
included, carries a corpus manifest holding the HEAD SHA of each corpus repo it was
measured against. And the baseline is committed. Report the numbers you got, not the
numbers you wanted.

### v05-agent: the showdown (dive 6)

`agent.py` is a tool loop (`agents-deep-dive/agent/loop.py` plus `tools.py`) with
`grep`, `read_file`, and `list_dir` over the corpus. Retrieval by searching rather than
embedding. Then run `askrepo eval --mode rag` against `--mode agent` on the same golden
set.

Here is the honest expectation. On a corpus this small and this well-organized, the
agent may match or beat RAG on correctness while costing several times more per
question. Or RAG's embeddings may fumble the exact-name lookups the agent greps in one
step. Whichever way it lands, the table is the deliverable. Write the verdict into the
README with the numbers next to it.

**Done when:** both modes run the full golden set and the comparison table
(correctness, hit rate, cost, latency, per-category breakdown) is committed.

### v06-hardened: the corpus is hostile (dive 7)

`fixtures/evil-repo/`: a tiny fake project whose README, docstrings, and comments
carry injections drawn from `prompt-injection-deep-dive/guardrails/attacks.py`:
"ignore your instructions", tool-abuse lures, exfiltration bait. Note which attacks
matter here. Task-aligned indirect injection, meaning a comment that looks like a
relevant instruction, lands far more reliably than "print your system prompt".
`guardrails.py` adds the defenses from that dive: content demarcation, output checks
(`output_checks.py`), and tighter tool permissions for agent mode, since the agent's
`read_file` is how the injection gets delivered.

**Done when:** `askrepo redteam` runs `redteam.jsonl` against both modes and
reports attack success rate, and the README shows the before-and-after numbers,
including whatever the defenses did not stop.

### v07-production: the dozen lines around the call (dive 8)

`ops.py` lifts from `ai-in-production-deep-dive/prod/`: answer and embedding caching
(`cache.py`), a cost meter with a per-session budget that refuses instead of
overspending (`cost.py`), retries with backoff (`reliability.py`), and structured JSON
logs of every call (`observability.py`). The test suite runs entirely on the mock
provider, so CI never needs a key.

**Done when:** a repeated question shows a visible cache hit at roughly zero cost, a
full eval run prints its total spend, the logs let you reconstruct any answer after the
fact, and the tests pass offline.

---

## The eval set design (v04)

One JSONL line per question, the same shape as `evals-deep-dive/datasets/qa.jsonl`
extended with retrieval ground truth:

```json
{"id": "loc-03", "category": "locator",
 "question": "Which deep dive covers barge-in, and what is barge-in?",
 "expected_files": ["realtime-voice-deep-dive/README.md"],
 "keypoints": ["realtime voice dive", "user interrupts mid-response"],
 "answerable": true}
```

Aim for 40 to 60 questions in total, split roughly evenly across these categories.

| Category | Probes | Example |
|----------|--------|---------|
| `locator` | retrieval routing | "Which dive covers barge-in?" |
| `concept` | doc understanding | "Per the glossary, what does temperature change?" |
| `code` | code chunking + reading | "What does `harness/policy.py` decide?" |
| `cross-dive` | multi-chunk synthesis | "How do the evals and fine-tuning dives relate?" |
| `negative` | honesty | "What's the capital of France?", where the correct answer is a decline |
| `adversarial` | v06 wiring | questions whose retrieved chunks contain planted bait (fixtures corpus only) |

Five metrics. `retrieval hit@5` asks whether any `expected_files` came back, scored
from the pipeline with no model needed. `citation precision` asks whether the cited
paths resolve and appear in `expected_files`. `judged correctness` uses the LLM judge
from `evals/judges.py` against `keypoints`, and you spot-check about ten judgments by
hand once, as the evals dive says to. Then `cost` and `latency` per question. For
`negative` questions, skip hit@5 and score a decline as 1.0.

Then the ritual. The first honest run becomes `baseline.run.json`, committed. Every
later change (chunk size, blend weight, prompt tweak, agent mode) gets compared against
it. The deltas are the story. The absolutes are only a starting point.

---

## Branch-off features

These run genuinely parallel to the main line, so they get feature branches, merged to
`main` when done. The work then shows up in history with no stale branch left behind.

| Branch | Dive | What it adds |
|--------|------|--------------|
| `feat/mcp` | MCP | `mcp_server.py` exposing `ask` + `search` as MCP tools; then point Claude Code at it and ask it questions about this repo, closing the meta loop. Pattern: `mcp-deep-dive/servers/`, and `agents-deep-dive/agent/mcp_server.py` shows the same agent-to-MCP move. |
| `feat/context` | Context Engineering | `askrepo chat`: multi-turn sessions with token budgeting and compaction (`context/memory.py`, `assemble.py`, `tokens.py`); decide which retrieved chunks survive across turns. |
| `feat/local` | Local Models | Ollama backend for embeddings *and* answers: "index a private codebase without sending a byte to a provider." Rerun the v04 evals against it and publish the quality gap honestly. |
| `feat/harness` | Agent Harnesses | Permission policy and sandbox around agent mode's file tools (`harness/policy.py`, `sandbox.py`). v06 showed the file tools are where the attack lands, and this is the structural fix. |
| `feat/observability` | Observability | `askrepo watch` (`watch.py`): trend the capstone's own eval runs and the corpus drifting under the frozen baseline. Not the dive's subject, which is a service's request traffic; a CLI has none, and what it accumulates instead is runs and a corpus. The deliverable is the noise floor between two runs of an unchanged config, which decides which of v05's and ext-local's published comparisons were ever real. |

## Explicit non-goals (and honest stretch goals)

- **Hosted upload and multi-user.** That is a product rather than a capstone. If you
  ever want it, it is a branch off v07, and the new work is tenancy and storage rather
  than AI.
- **Voice, multimodal, fine-tuning.** Bolt-ons for a project shaped like this one. If
  you want a token gesture, there is voice-ask via the realtime dive, "explain this
  architecture diagram" via multimodal, and fine-tuning the citation format on v04
  transcripts. None of them justify a step of their own, so don't force them.

## Getting started

```bash
cd ~/Documents/WebDev/AI/DeepDives
mkdir deep-dive-capstone && cd deep-dive-capstone && git init
# build v00 per above, then:
git add -A && git commit -m "v00: offline scaffold" && git tag v00-scaffold
```

From there every step is the same: build, hit its "done when", commit, tag. When a
later step reveals a flaw in earlier code, fix it on `main`. The tags are historical
snapshots rather than maintained lines, which is exactly why this structure survives.
