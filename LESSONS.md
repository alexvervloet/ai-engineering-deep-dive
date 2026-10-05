# Lessons

## Check the global agent instructions explicitly

Expected: repository-local instruction discovery would find the applicable
`AGENTS.md` before committing.

Actual: this workspace has no repository-local `AGENTS.md`; the applicable file
was the global `~/.codex/AGENTS.md`, clarified by the user after the first search.

Next time: when a user refers to global agent instructions, read
`~/.codex/AGENTS.md` directly before planning, staging, or committing.

## Validate hand-written MCP envelopes against the SDK

Expected: the abbreviated MCP 2026 announcement request body would be sufficient
for the raw Streamable HTTP example.

Actual: the Python SDK correctly returned HTTP 400 until `_meta` included both
`io.modelcontextprotocol/protocolVersion` and
`io.modelcontextprotocol/clientCapabilities` in addition to client information.

Next time: test protocol examples end to end against the current Tier 1 SDK and
inspect its validation types when a prose announcement abbreviates the wire shape.

## Parent submodule registration needs Git metadata access

Expected: `git submodule add` could register an already-built child repository
from the writable workspace.

Actual: ordinary workspace access could edit project files but could not lock the
parent repository's `.git/config` or index, so registration stopped before making
any tracked change.

Next time: run parent-repository submodule and index operations in the approved
Git environment when `.git` is mounted read-only inside the workspace sandbox.

## Root-level unittest discovery is not universal across legacy dives

Expected: the capstone README command `python -m unittest discover -v` would run its
tracked `tests/test_*.py` files from the submodule root.

Actual: Python 3.13 reported zero tests and exited nonzero, because that legacy
`tests/` directory is not importable. An explicit `discover -s tests -v` ran all 71
tests without touching the user's dirty submodule.

Next time: validate every declared root command instead of inferring it from prose.
For legacy layouts with no `tests/__init__.py`, give unittest an explicit start
directory, and keep a nonempty-suite assertion wherever the repo owns CI.

## Inspect tracked history before adding an apparently absent file

Expected: adding a missing parent `LESSONS.md` would create a new file.

Actual: the path already existed in Git history but was absent from the visible
working tree, so the first commit replaced three earlier lessons. The loss was
detected immediately by comparing the commit diff with the intended new entry.

Next time: before adding a repository-root convention file, check both the working
tree and `git cat-file -e HEAD:<path>`. If the path is tracked but not materialized,
read its committed contents and preserve them before editing.

## Offline execution can still require installed SDK interfaces

Expected: the capstone test suite and local-model sizing lesson would run from a
fresh Python because their behavior is offline and the capstone mock needs no
dependencies.

Actual: capstone local-provider tests patch `openai.OpenAI`, which requires the
module to be installed, and importing the local-model package loads `dotenv` before
the sizing-only example runs. Both failed in isolated CI while passing on the
dependency-rich development machine.

Next time: distinguish "no network or service at execution time" from "standard
library only." Verify in isolated environments and install declared dependencies
even when the selected runtime path makes no external call.

## Push a submodule before the parent commit that points at it

Expected: pushing the parent's updated submodule pointer and the submodule's own
commits in whichever order they were finished would be equivalent, since both ended
up on their remotes within a minute of each other.

Actual: the parent pointer was pushed first, referencing a submodule commit that was
still local. The parent workflow checks out submodules recursively, so
`actions/checkout` failed with exit code 128 and the message "Fetched in submodule
path 'testing-and-delivery-deep-dive', but it did not contain b160d96. Direct
fetching of that commit failed." The whole matrix was skipped. Pushing the submodule
afterwards did not retrigger the parent, so the red run stayed red until it was
explicitly rerun.

Next time: push child repositories first, then the parent commit that advances their
pointers. Before pushing a parent pointer, confirm the target commit is on the child
remote with `git -C <sub> branch -r --contains <sha>`. Treat a green child run as no
evidence at all about the parent.

## A doc path can be a test input, not just a link

Expected: moving the twelve reference docs into `docs/` was a link problem. Rewrite
every `../SECRETS.md` to `../docs/SECRETS.md`, confirm the link checker goes green,
done.

Actual: the link checker went green while two classes of reference stayed broken,
because neither one is a Markdown link. The capstone documents its eval fixtures as
shell commands (`askrepo ask ... --context ../MODELS.md`) inside backticks, and a
dozen dive READMEs point at `../SECRETS.md` from inside `#` comment blocks in setup
snippets. A reader follows both. No link checker sees either. The eval fixture is the
worse of the two, because it is a path the reader is told to type, so a stale one
makes the documented command fail instead of merely 404ing.

The move was safe in one respect that could easily have gone the other way.
`askrepo`'s indexer picks its corpus by file extension rather than from an explicit
file list, so `docs/` came along with no change at all. A hardcoded manifest would
have shrunk the corpus without saying so and changed every eval score with it.

Next time: after moving a file, grep for the bare filename across every extension,
not just `*.md`, and not just inside link syntax. The link checker is a floor, not a
verification. Check whether anything selects files by an explicit list before
assuming a move is inert.

## A numbering convention can be a tested invariant

Expected: the Testing & Delivery textbook numbering its sections `## 1.` to `## 13.`
was an inconsistency, since every other chapter numbers them `chapter.section`, and
`docs/GLOSSARY.md` already cited that chapter as §23.x. Renumbering looked like a
tidy-up with no consumer.

Actual: `tests/test_manifest.py` asserts `^## <n>\. ` in TEXTBOOK.md for every lesson,
because the bare numbers are what tie a lesson together across README, TEXTBOOK, and
EXERCISES. The renumber turned that three-way correspondence into a failing test, and
the parent's CI matrix caught it on push rather than anything local. The glossary's
apparent off-by-one was not a defect either: it counts the chapter intro as §23.1, so
its citations were already coherent.

Next time: before renumbering or renaming anything a document uses as an identifier,
grep the sibling test suite for the pattern, not just the prose. A heading that looks
like formatting may be an interface. And when two files disagree about a numbering
scheme, find out which one is enforced before deciding which one is wrong.

## CodeQL's quality suite drowned the security findings

**Expected.** Turning on CodeQL with `security-and-quality` would give readers a
public Security tab worth looking at.

**What happened.** The first run produced 112 open alerts. Eleven were security
findings. The other 101 were quality notes: unused imports, and `py/unsafe-cyclic-import`
fired repeatedly on the `architecture-deep-dive` provider-seam variants, which are
near-identical `app.py` files by design because the whole chapter is the same app
rewritten five ways. A tab with 112 alerts on it argues against the repo instead of
for it, which is the opposite of why it was published.

**Next time.** Use `security-extended` on a teaching repo. The quality suite is aimed
at a codebase you are maintaining, not one where the duplication and the deliberate
mistakes are the lesson. Switching suites auto-closed all 101 quality alerts on the
next run.

**Also.** The dismissal API wants `used in tests` and `false positive` with spaces.
The underscore forms that appear in most examples return HTTP 422.

## Two API assumptions the audit only caught by running them

**Expected.** Auditing the new `responses/` track, two claims looked wrong on sight.
Background mode with `store=False` should be rejected, because a job you poll by ID
has to be stored somewhere. And `response_format` on the Responses endpoint should be
silently ignored, because unknown JSON keys usually are, which would make the
`text.format` rename a nasty silent migration bug worth teaching.

**What happened.** Both were wrong, in opposite directions. `background=True` with
`store=False` is accepted and the response stays retrievable through polling, so the
docstring under audit was right and the reviewer was not. And `response_format` returns
a 400 whose message names `text.format` and links the docs, so the rename is the part
of that migration the endpoint handles best. The second one had already been written
into TEXTBOOK.md as fact before the probe ran, and had to be rewritten.

**Next time.** In this series, an assertion about provider behaviour is a probe, not a
recollection, and that applies to the reviewer exactly as much as to the author. Write
the six-line script against the live API before the paragraph, not after. The tell is
the word "because": every one of these was a plausible mechanism reasoned forward into
a fact.

**Also.** Two of the best teaching moments in the track came out of being wrong.
`responses.parse` raising `pydantic.ValidationError` on a truncated object, rather than
returning a `None` to check, is a better lesson than the one originally planned, and it
was only found by capping `max_output_tokens` to see what would happen.

## The lockfile that turned out to be a lesson

**Expected.** A sweep to standardize dependency declarations, starting from the
reading that four dives had a `pyproject.toml` and Testing & Delivery had a Python
lockfile the others were missing. The obvious job was to propagate both.

**What happened.** Both halves were wrong. Five dives have a `pyproject.toml`, not
four, and they are exactly the five with an importable package the lessons import as
a library, so the split tracks a real difference rather than drift. And no dive has a
lockfile at all. Testing & Delivery's `pylock.toml` is an empty PEP 751 document with
`packages = []`, written as course material for its chapter on locking: `check_setup.py`
parses it, `tests/test_locking.py` asserts on it, and `examples/08_dependency_locking.py`
audits it. Copying it into 23 siblings would have spread a teaching prop that locks
nothing, and in the dives with real dependencies an empty lock would have been a lie.

The drift that did exist was in version bounds, and nobody had gone looking for it.
`architecture-deep-dive` asked for `openai>=1.40.0` and `anthropic>=0.34.0`, unbounded,
a different major than every sibling. Seven more libraries across 18 dives had a floor
and no ceiling.

**Next time.** Before propagating a file across the series, check what reads it. A
config file that appears in exactly one repo is as likely to be that repo's subject as
it is to be a gap, and this series is full of files that exist to be examined rather
than obeyed. Grepping for the filename found the answer in one command.

## A text sweep over hard-wrapped Markdown misses what sits on the line break

**Expected.** Converting uncontracted forms ("it is", "cannot", "does not") to
contractions across the series looked like a per-line scan. Find the pattern, judge
whether it's emphasis, rewrite the line.

**What happened.** The prose is hard-wrapped at about 90 characters, so a good number
of the phrases straddle a newline: `do` ending one line and `not back.` starting the
next. A line-oriented scanner reports those files as clean. The first pass through the
parent docs missed roughly sixty of them, and they only surfaced because the same files
got re-scanned with a detector that joins each line to its successor before matching.

That detector then missed a second batch, because a continuation line inside a
blockquote or a list starts with `>` or `-` before the word. Stripping the leading
marker before joining found the rest. Two classes of miss, both invisible to the
obvious tool, both found by re-running rather than by reading.

The other surprise was the opposite of a miss. A fair number of the matches are text
that must stay byte-for-byte: `CANNOT ANSWER:` is a sentinel `askdb/generate.py` writes
and `tests/test_evaluate.py` asserts on, "What is 23 * 47?" is the literal prompt in
`examples/02_one_tool_call.py`, and "You are a helpful assistant." is a system message
in `examples/07_token_counting.py`. Prose quoting a string the code also contains is
not prose. Grepping the source for the quoted phrase before editing settled each case
in one command.

**Next time.** For any regex sweep over this repo's Markdown, run two detectors, one
per line and one across each line boundary with list and quote markers stripped, and
verify by re-scanning after the edits rather than trusting the first pass. Before
rewriting anything inside quotes, grep the examples for it.

## The version audit found more in a resolver than in a changelog

**Expected.** A monthly currency sweep reads like a documentation task. Check the
provider pricing pages, check PyPI and npm for newer releases, update the numbers and
the pins, done. The interesting findings would be in release notes.

**What happened.** The release notes were the least useful source of the three, and
two of the four real findings came from running a command rather than reading a page.

Both provider SDKs had gone major, which a changelog tells you. What it doesn't tell
you is whether your repo can actually take the upgrade. `pip install --dry-run` with
the proposed pin set answered that in seconds: litellm still requires
`openai<3.0.0` and `httpx<1.0`, so `professional-tools-deep-dive` cannot install the
current SDK at all, a month after it shipped. No document anywhere says "this repo is
blocked." It's an emergent property of two metadata files, and the only way to see it
is to ask the resolver.

The second one the same way. `anthropic` 1.0's migration guide says the sampling
parameters were removed. Installing 1.5.0 and running `inspect.signature` on
`messages.create` showed exactly which names were gone and that `extra_body` was
there to catch them, which is the difference between writing a note about the change
and writing the code that survives it.

The third was a caret. `"@anthropic-ai/sdk": "^0.116.0"` had been quietly pinned to
0.116.x for nine minor releases, because caret on a `0.x` version locks the minor.
`npm install` never complained, the tests passed, and nothing surfaced it except
comparing the lockfile to the registry.

And the finding with an actual deadline came from a deprecations page rather than a
release note: `o4-mini`, the default in a runnable example, shuts down on 2026-10-23.
Release notes announce what arrived. Only the deprecations page announces what leaves,
and what leaves is the half that breaks a repo.

**Next time.** Run the audit as four passes, not one. Query the registries for current
versions (`pypi.org/pypi/<pkg>/json`, `registry.npmjs.org/<pkg>`) rather than reading
about them. Dry-run the proposed pin set before writing a single number, because a
bound in a transitive dependency vetoes your upgrade silently. Install the new major
and introspect the signatures you actually call. And read every provider's
deprecations page first, before the changelogs, because that's where the dates are.

## The deprecations page lists models, not the libraries that default to them

**Expected.** Last month's lesson said to read every provider's deprecations page first,
because that's where the dates are. Do that, grep the series for each model id on the
list, and every deadline is accounted for.

**What happened.** The grep finds the ids the series writes down. It can't find an id a
library chooses for you. `gpt-3.5-turbo` shuts down on 2026-10-23, and the series only
mentioned it in prose, so the grep looked harmless. But `llama-index-llms-openai`, even
at its newest release, still defaults to `gpt-3.5-turbo`, and the professional-tools
LlamaIndex chapter deliberately scores the library at its defaults. Nothing in the repo
names the model the chapter will call on that day. Resolving `Settings.llm.model` in
the dive's own venv found it in one line.

Two smaller surprises. Seven repos show green CI, but none has run since GitHub took
Node 20 off its runners on 2026-09-23, and they still use node20 actions. A green badge
dates from the last push, not from today. And a research agent ranked an MCP spec rewrite
as its second-highest risk, while the MCP dive had already been rewritten for that spec.
Research says what changed in the world. Only the repo says whether that's news here.

**Next time.** For every library with a model default (LlamaIndex, LangChain, DeepEval,
litellm), resolve the default at runtime and check it against the deprecations list. Read
each repo's last CI run date next to its action versions, and treat a run older than a
runner change as unknown rather than passing. Grep the repo for every outside finding
before ranking it.

## The cheaper replacement model costs more per photo

**Expected.** OpenAI names `gpt-6-luna` as the replacement for `gpt-5.4-nano`, at half
the per-token price. The plan was to swap the id, add `reasoning_effort="none"` so
temperature and tools keep working, and watch the cost examples get cheaper.

**What happened.** Text did get cheaper. Images didn't. Both models bill 1.2 tokens per
32-pixel patch and cap `detail: "high"` at 3,000 tokens. But when the request leaves
`detail` out, nano treats it like "high" and luna doesn't shrink the image at all. A
3000x3000 photo with no `detail` cost 3,000 tokens on nano and 10,603 on luna, so half
the price per token came out at about 1.8 times the price per photo. Past 30,000 patches
luna returns a 400 where nano just resized. The multimodal dive never sets `detail`.

Measuring that turned up an older bug. The dive's image estimator used tile constants
(2,833 base, 5,667 per tile) that put a 512x512 image at 8,500 tokens. Both models
bill 307. The estimator had been about 28 times high since it was written, and nothing
caught it, because nothing compared it to a bill.

**Next time.** A model migration needs a probe for every input type the series sends,
not only text: `usage.prompt_tokens` on a few image sizes with `detail` set and unset.
And any estimator that teaches a number should have one test that pins it to a measured
bill, so a wrong constant fails instead of teaching.

## A green live run can be testing the wrong provider

**Expected.** To verify a dive on the new OpenAI default, run its lessons under
`secrun` and look for non-zero exit codes. Every dive defaults `PROVIDER` to openai.

**What happened.** All twenty prompt-engineering lessons passed, and none of them had
called OpenAI. That dive's local `.env` sets `PROVIDER=claude`, `MODEL=claude-haiku-4-5`
and `REASONING_MODEL=claude-sonnet-4-6`, left over from earlier work, and `load_dotenv()`
fills them in. The run proved the Claude path still worked, which nobody had changed.
It only surfaced because a deliberate override test came back with an Anthropic 404 for
a model named `gpt-4o-mini`. Setting `PROVIDER=openai` alone wasn't enough either, since
`MODEL` still pointed at a Claude id and every call 404'd.

**Next time.** Before a live verification run, read the dive's `.env` and pin every
variable that selects a provider or model on the command line, blanking the ones you want
at their defaults. Then make the run print which model answered, and check it.

## Every wrapper library has its own copy of the model list

**Expected.** In professional-tools, the frameworks pass extra keyword arguments through
to the OpenAI SDK, so moving to `gpt-6-luna` meant adding `reasoning_effort="none"` to
each call, same as the plain-SDK dives.

**What happened.** Each library had its own opinion of the new model, and the opinions
disagreed. LlamaIndex 0.7.9 refused to construct a client at all ("Unknown model
'gpt-6-luna'"), because it looks up context windows by name. DeepEval sends
`temperature=0` on every judge call even when you never asked for one, so a bare model
name 400s; it needs the parameter through `generation_kwargs`. LiteLLM 1.101 was fine,
but the dive's stale venv had 1.92, which rejected `reasoning_effort` for luna, and that
nearly sent us chasing a bump we didn't need.

The quiet one was cost. DeepEval 4.2.3 has no price for nano or luna, and an unknown
model doesn't raise, it reports `evaluation_cost` as 0. Since the August move to nano,
the chapter's "DeepEval costs about 12 times more" comparison would have printed the
judging pipeline as free. The hand-rolled side of the same comparison was still pricing
at gpt-4o-mini's rate through a constant named `GPT_4O_MINI_PRICE`.

**Next time.** After a model change, construct each framework's client for the new id
before editing anything, and probe one call per library. Treat a cost of exactly 0 from
a paid model as a missing price, not a cheap run. And sync the venv to requirements.txt
before believing any version-specific failure.

## A better model broke the security lessons

**Expected.** Moving the prompt-injection dive to `gpt-6-luna` would be the same edit
as everywhere else: swap the id, turn reasoning off, check the examples still run.

**What happened.** Every example ran, and the dive stopped teaching anything. Its method
is to show an attack land and then build the defense that stops it. Measured with 10 runs
of each of the four indirect attacks: 30 of 40 landed on `gpt-5.4-nano` and on
`gpt-4o-mini`, 8 of 40 on `gpt-5.4-mini`, and 0 of 40 on luna. A green run hid it, because
"the injection didn't land" is a valid outcome the examples print politely. Two runs of
example 03 looked like bad luck, and only a count over many runs showed the rate had
gone to zero. The dive now pins `gpt-4o-mini` on purpose and says why.

**Next time.** For any lesson whose point is a model failing (injection, hallucination,
refusal, judge bias), measure the failure rate on the new model before migrating, not
just whether the script exits 0. A model upgrade can remove the very failure a lesson
exists to show.
