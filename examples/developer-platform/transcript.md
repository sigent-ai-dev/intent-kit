# Example: Developer Platform (Vague Input)

This example was produced by actually running the `/intent.capture` workflow against a real `.intent/` project. It demonstrates how the propose-and-steer interaction model handles vague input.

## Setup

```bash
intent init dogfood-real
```

## Phase 1: Capture

### Input (vague — just a few words)

```
/intent.capture internal developer platform
```

### Step 1: Input Assessment

The input is **vague** — three words, no clear outcome, no context. The command classifies this and enters the propose-and-steer interaction.

### Step 2: AI Proposes Interpretation

> Here's my read of what you're describing:
>
> **The big idea**: Build an internal developer platform that codifies your team's technical decisions into reusable templates and golden paths, reducing setup overhead and enforcing consistency across services.
>
> **What I think is driving this**: Developers are spending too much time on undifferentiated work (CI setup, auth wiring, deployment config) and making inconsistent choices that compound over time.
>
> **Success would look like**:
> - New service goes from init to deployed in under an hour
> - All services share the same auth/data/CI patterns by default
> - Deviations are documented, not silent
>
> **What I'm assuming**: This is for an internal team (not a product for external developers), and you don't have a dedicated platform team.
>
> Am I reading this right, or should I adjust my understanding?

### User Response

> Close but not quite. We're not building infrastructure — we're a 12-dev startup and everyone is drowning in setup overhead. No platform team. The idea is golden paths that reduce decisions, plus consistency enforcement so we don't end up with 4 different auth approaches.

### Step 2 (round 2): AI Incorporates Correction

> Got it — different framing. Not "platform team serves app teams" but "startup standardises its own practices." The key addition is **consistency enforcement** — not just templates but making deviation require justification.
>
> Revised:
>
> **The big idea**: Codify the startup's technical decisions into enforceable golden paths so developers inherit proven patterns by default and achieve consistency across services without a dedicated platform team.
>
> **Driving**: At 12 devs, inconsistency compounds fast. Every new hire inherits a different mental model.
>
> **Success**: New service in <1 hour. First feature from new dev in <1 week. 90% consistency on core patterns.
>
> Is that closer?

### User Response

> Yes exactly.

### Step 3: AI Drafts Full Intent

With alignment reached in 2 rounds, the AI drafts the complete 7-section intent document.

### Step 4: AI Presents for Confirmation

> Here's the captured intent. Review it — I'll adjust anything that doesn't match your thinking.
>
> [shows full intent.md — see output below]
>
> Does this capture what you're trying to do? Flag anything that feels off — especially the Intent sentence and Success Criteria, since everything downstream traces to those.

### User Response

> Looks good. Ship it.

### Step 5-7: Validate, Write, Report

```
intent check --verbose

  PASS  Project exists: .intent/ directory found
  PASS  State file valid: state.json parsed successfully
  PASS  Phase gates: All phase gates consistent
  PASS  Intent sections present: All 7 required sections present
         Found: ['Context', 'Intent', 'Motivation', 'Quality Attributes',
         'Success Criteria', 'Assumptions', 'Clarifications']
  PASS  Intent is single sentence: Intent section is concise

All checks passed
```

---

## Output: `.intent/intent.md`

```markdown
# Intent: Developer Golden Paths

**Intent ID**: INT-001
**Captured**: 2026-05-21
**Actor**: user

## Context

Small engineering team without a dedicated platform team. Each new service or feature starts from scratch with ad-hoc technology choices, leading to inconsistency across the codebase (multiple auth approaches, different ORMs, varied CI setups). Onboarding new developers takes longer than necessary because there are no standardised patterns to learn.

## Intent

Codify the team's technical decisions into enforceable golden paths so developers inherit proven patterns by default and achieve consistency across services without a dedicated platform team.

## Motivation

Inconsistency compounds with team growth — every new hire inherits a different mental model of how things are built. Setup overhead on every new service wastes senior engineering time on solved problems. Acting now while the team is small is dramatically cheaper than retrofitting later.

## Quality Attributes

- **QA-001**: Developer experience — golden paths must feel like acceleration, not bureaucracy
- **QA-002**: Consistency — services built from golden paths share auth, data access, CI, and observability patterns
- **QA-003**: Escapability — teams can deviate with documented justification (ADR), not silently
- **QA-004**: Maintainability — golden paths evolve with the team's learning, not ossify

## Success Criteria

- **SC-001**: New service goes from init to deployed-with-CI in under 1 hour using a golden path
- **SC-002**: New developer ships their first feature within 5 working days of starting
- **SC-003**: 90% of services use the same auth approach (measured by codebase audit)
- **SC-004**: Deviations from golden paths are documented (ADR exists for each deviation)

## Assumptions

- **ASM-001** [medium]: The team will agree on "the one way" for auth, data access, and CI (requires facilitated decision-making)
- **ASM-002** [high]: Templates and scaffolding are sufficient — no runtime platform or service mesh needed
- **ASM-003** [high]: Developers are senior enough to use templates without hand-holding

## Clarifications

### CLR-001
**Prompt:** What is the current tech stack? (Language, frameworks, cloud provider)
**Resolution:** OPEN — needed before steering to determine what the golden paths contain

### CLR-002
**Prompt:** Are there existing services that represent "the good pattern" to encode, or are we designing from scratch?
**Resolution:** OPEN — shapes whether this is extraction or invention
```

---

## Output: `.intent/state.json`

```json
{
  "project_name": "dogfood-real",
  "intent_id": "INT-001",
  "current_phase": "capture",
  "phases": {
    "capture": { "complete": true, "completed_at": "2026-05-21T05:30:00Z" },
    "steer": { "complete": false },
    "define": { "complete": false },
    "decompose": { "complete": false }
  },
  "created_at": "2026-05-21T05:12:48Z"
}
```

---

## Output: `.intent/audit.md` (appended entry)

```markdown
## 2026-05-21T05:30:00Z — Intent captured

**Actor**: user/agent
**Phase**: capture
**Outcome**: complete
**Intent summary**: Codify the team's technical decisions into enforceable golden paths so developers inherit proven patterns by default and achieve consistency across services without a dedicated platform team.
```

---

## Key Observations

1. **Two proposal rounds** — vague "internal developer platform" → first proposal → user correction ("not infra, consistency enforcement") → revised proposal → confirmed
2. **User's correction was the high-value signal** — "consistency enforcement" and "12-dev startup" fundamentally shaped the quality attributes and success criteria
3. **AI showed reasoning** — "I'm assuming this is for an internal team, no platform team" let the user confirm without needing to state the obvious
4. **Two CLR items remain OPEN** — the conversation was sufficient for a valid intent but tech stack context is still needed before Phase 2
5. **`intent check` validates** — all 7 sections present, intent is concise, gates consistent
