# Changelog

Notable changes to the AI Engineering: Deep Dives series, newest first.

Each entry records what changed and, where it matters, why. Changes inside a
submodule are listed under that submodule's name; the submodule's own history
has the per-file detail.

Format loosely follows [Keep a Changelog](https://keepachangelog.com). This
series is not versioned, so entries are grouped by date instead of release.

---

## 2026-08-08: currency audit

A full pass over every submodule (except `architecture-deep-dive`) checking that
the code runs and the prose describes current practice as of August 2026.

### Ground truth used for this pass

Verified against live sources on 2026-08-08, not from memory:

| Fact | Source |
|------|--------|
| OpenAI model IDs and availability | `GET /v1/models` on a real key, plus the pricing and deprecations pages |
| Anthropic model IDs, pricing, thinking API | `claude-api` skill reference, cached 2026-06-24 |
| Python package versions | PyPI JSON API |
| MCP SDK 2.0 breaking changes | `py.sdk.modelcontextprotocol.io/migration/`, confirmed by installing it |

Two things worth recording because they contradict what a search will tell you:

- **`o4-mini` and `o3` are still live in the API.** The February and August 2026
  retirements that show up in search results were ChatGPT retirements, not API
  ones. Both still appear in `GET /v1/models`.
- **`gpt-4o-mini` is not deprecated.** It still works. It was replaced in the
  examples because it is a 2024 model and no longer represents current practice,
  not because it broke.

### Fixed

- **mcp-deep-dive: the repo did not run.** `requirements.txt` asked for
  `mcp[cli]>=1.2.0` while its own comment said "pin to a 1.x release". MCP Python
  SDK 2.0.0 shipped 2026-07-28, so a fresh install resolved to 2.0.0 and every
  server and client example failed at import: `mcp.server.fastmcp` no longer
  exists (`FastMCP` is now `MCPServer` in `mcp.server.mcpserver`). Eight files
  were affected.

- **openai-api-deep-dive: two request bodies would have 400'd.** `hands_on/ask.py`
  and the batch example build their request as a dict, so the `max_tokens` rename
  below missed them on the first pass.

- **The `stop` parameter is gone from the entire GPT-5 line**, which broke the
  stop-sequences lesson, the `--stop` flag on `ask.py`, and the OpenAI branch of
  the prompt-engineering provider. Only the legacy gpt-4o line still accepts it.

### Changed

- **OpenAI examples moved off `gpt-4o-mini` to `gpt-5.4-nano`.** Not because
  gpt-4o-mini broke (it still works) but because it is a 2024 model.

  The first choice here was `gpt-5.6-luna`, the newest cheap tier. Probing it
  against what the dives actually do killed that idea: the 5.6 tiers reject
  `temperature` and `top_p`, and refuse function calling on
  `/v1/chat/completions` unless you set `reasoning_effort: "none"` or move to the
  Responses API. `prompt-engineering-deep-dive` alone has 25 files touching
  `temperature`. `gpt-5.4-nano` costs the same ($0.20/$1.25 vs $0.20/$1.20),
  is current generation, and defaults `reasoning.effort` to `none`, so every
  existing lesson survives.

- **`max_tokens` is now `max_completion_tokens` on OpenAI calls only.** The
  GPT-5 line rejects the old name. Anthropic still uses `max_tokens`, so the
  Claude branch of every dual-provider `providers.py` is untouched, as is
  local-models-deep-dive, whose local servers still expect the old name.

- **Stop sequences became a lesson about retirement.** Rather than delete the
  example, it now shows the 400 on a current model, the old behaviour on
  gpt-4o-mini, and the structured-output schema that replaces it.

- **fine-tuning-deep-dive tells the truth about the OpenAI path.** OpenAI is
  winding down self-serve fine-tuning (2026-05-07, 2026-07-02, 2027-01-06 by
  cohort), so the README's promise that one env var runs a real paid fine-tune
  is no longer true. The mock lifecycle is unchanged and is now the main path.

- MODELS.md rebuilt around the GPT-5 line, with the three parameter changes that
  break GPT-4 era code, and Claude's Opus 5 / Sonnet 5 added.

### Deliberately not changed

Stored results are records, not configuration, so the model names in them stay
as they were when the run happened:

- `deep-dive-capstone/evals/*` (a run from 2026-07-04)
- `professional-tools-deep-dive/*/VERDICT.md`, its `LESSONS.md`, and the exercise
  citing a judge model
- `AUTHORING-LESSONS.md`, which records observed model behaviour

Re-running those comparisons on `gpt-5.4-nano` is follow-up work. A find and
replace would have made them claim something that never ran.

- **deep-dive-capstone had the same MCP breakage**, found later via the pin
  audit: `askrepo/mcp_server.py` imports `mcp.server.fastmcp` and its
  requirements allowed 2.x. Ported and pinned the same way.

- **Dependency pins now carry an upper bound.** `context-engineering` and
  `prompt-engineering` asked for `anthropic>=0.40.0` while every sibling asked
  for `>=0.111.0`, and 0.40 predates `messages.parse`. Nothing anywhere had an
  upper bound, which is exactly how the MCP breakage happened, so provider SDKs
  are now ranged (`anthropic>=0.111.0,<1`, `openai>=2.0,<3`).

### Added

Five new modules, each covering something the series did not mention at all.
Every one was verified against the live API before being written up.

- **openai-api-deep-dive, example 26: the Responses API.** The dive taught Chat
  Completions and never mentioned the other endpoint, which matters now the
  Assistants API shuts down on 2026-08-26. Covers server-side conversation state
  and hosted tools, and is explicit that the cost is portability, since
  `/v1/chat/completions` is the dialect Ollama, LM Studio, vLLM and LiteLLM all
  speak and example 17 depends on that.

- **context-engineering-deep-dive, section 11: server-side compaction and
  context editing.** The dive built compaction by hand and never said the API
  now does it. Covers compaction (summarizes, needs Sonnet/Opus 4.6+) versus
  context editing (clears, runs on Haiku 4.5), and the trap where keeping only
  `.text` silently drops the compaction block, which stays invisible until the
  first real compaction near 150K tokens.

- **agent-harness-deep-dive, section 15: Managed Agents.** Referenced in six
  places, never demonstrated. Framed as the far end of the axis the dive walks,
  with a table mapping each section's problem to its hosted answer. Opt-in via
  `--real` because it provisions billable infrastructure; it cleans up after
  itself.

- **agent-harness-deep-dive, section 16: Agent Skills.** Progressive-disclosure
  instructions. Placed in the harness dive because which skills to attach is
  harness configuration, and because a skill can ship scripts that execute.

- **agents-deep-dive, examples 16 and 17: tool search, programmatic tool
  calling, and the memory tool.** The first two share a cause: the dive assumed
  a small tool surface and a small number of calls, and both assumptions fail in
  the context window. The memory tool is the counterpart to section 9, which
  dies with the process. The example implements the storage backend including
  the path-traversal guard, since memory paths are model-generated.

### Known follow-ups

- The seven `professional-tools-deep-dive` verdicts were measured on
  `gpt-4o-mini` and now carry a dated note saying so. Re-running them on
  `gpt-5.4-nano` is a deliberate exercise, not a find and replace.
- `realtime-voice-deep-dive` remains simulation-only and was not otherwise
  touched by this pass.
