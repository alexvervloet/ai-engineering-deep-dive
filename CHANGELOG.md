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

### Changed

- OpenAI examples moved off `gpt-4o-mini` to `gpt-5.6-luna`, the current
  cost-optimized tier ($0.20/$1.20 per MTok against gpt-4o-mini's $0.15/$0.60).

### In progress

The rest of this pass is still running. Remaining: Anthropic API surface audit,
dependency pins across all repos, the parent reference docs, a per-repo content
audit of the other 16 dives, and new modules for concepts the series does not
yet cover.
