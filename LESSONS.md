# Lessons

## 2026-08-17: Check the global agent instructions explicitly

Expected: repository-local instruction discovery would find the applicable
`AGENTS.md` before committing.

Actual: this workspace has no repository-local `AGENTS.md`; the applicable file
was the global `~/.codex/AGENTS.md`, clarified by the user after the first search.

Next time: when a user refers to global agent instructions, read
`~/.codex/AGENTS.md` directly before planning, staging, or committing.

## 2026-08-17: Validate hand-written MCP envelopes against the SDK

Expected: the abbreviated MCP 2026 announcement request body would be sufficient
for the raw Streamable HTTP example.

Actual: the Python SDK correctly returned HTTP 400 until `_meta` included both
`io.modelcontextprotocol/protocolVersion` and
`io.modelcontextprotocol/clientCapabilities` in addition to client information.

Next time: test protocol examples end to end against the current Tier 1 SDK and
inspect its validation types when a prose announcement abbreviates the wire shape.

## 2026-08-17: Parent submodule registration needs Git metadata access

Expected: `git submodule add` could register an already-built child repository
from the writable workspace.

Actual: ordinary workspace access could edit project files but could not lock the
parent repository's `.git/config` or index, so registration stopped before making
any tracked change.

Next time: run parent-repository submodule and index operations in the approved
Git environment when `.git` is mounted read-only inside the workspace sandbox.

## Root-level unittest discovery is not universal across legacy dives

- **Expected:** the capstone README command `python -m unittest discover -v`
  would execute its tracked `tests/test_*.py` files from the submodule root.
- **Actual:** Python 3.13 reported zero tests and exited nonzero because that legacy
  `tests/` directory is not importable. Explicit `discover -s tests -v` ran 71
  tests successfully without modifying the user's dirty submodule.
- **Next time:** validate every declared root command instead of inferring it from
  prose. For legacy layouts without `tests/__init__.py`, give unittest an explicit
  start directory and retain a nonempty-suite assertion where the repo owns CI.

## 2026-08-20: Inspect tracked history before adding an apparently absent file

Expected: adding a missing parent `LESSONS.md` would create a new file.

Actual: the path already existed in Git history but was absent from the visible
working tree, so the first commit replaced three earlier lessons. The loss was
detected immediately by comparing the commit diff with the intended new entry.

Next time: before adding a repository-root convention file, check both the working
tree and `git cat-file -e HEAD:<path>`. If the path is tracked but not materialized,
read its committed contents and preserve them before editing.

## 2026-08-20: Offline execution can still require installed SDK interfaces

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

## 2026-08-20: Push a submodule before the parent commit that points at it

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
