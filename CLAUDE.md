<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
at specs/001-intent-init/plan.md
<!-- SPECKIT END -->

## Dependencies

### Intent Capture Agent Service (sigent-ai-dev/intent-capture-agent)

The `intent capture` CLI subcommand is a thin HTTP client that calls the
Intent Capture Agent service. The service does not exist yet.

**Status**: Pending — issue sigent-ai-dev/intent-capture-agent#11
**Blocking**: `intent capture start/status/connect` will error without a deployed service

**API contract expected by the CLI** (`src/intent_cli/capture.py`):
- `POST /sessions` → `{ session_id, join_url, status }`
- `GET /sessions/:id` → `{ status, progress: { sections_covered }, participants }`
- `GET /sessions/:id/result` → `{ intent_md, state, audit_md }`
- `DELETE /sessions/:id` → 204

**To verify**: `intent capture check-service` (once implemented)

When the service ships, update this section to "Active" and add the default URL.
