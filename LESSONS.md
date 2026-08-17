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
