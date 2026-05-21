# Example: Developer Platform (Vague Input)

This example shows how `/intent.capture` handles vague input through the propose-and-steer interaction model.

## Phase 1: Capture

### Input (vague — just a few words)

```
/intent.capture internal developer platform
```

### Interaction

**AI:**

> Here's my read of what you're describing:
>
> **The big idea**: Build an internal developer platform that centralises tooling, reduces cognitive load on application teams, and provides self-service infrastructure provisioning.
>
> **What I think is driving this**: Teams are spending too much time on undifferentiated infrastructure work (CI pipelines, deployment configs, monitoring setup) instead of building product features.
>
> **Success would look like**:
> - Developers can provision a new service (with CI, deployment, monitoring) in minutes not days
> - Common patterns are encoded as templates, not tribal knowledge
> - Platform team serves N application teams without linear headcount scaling
>
> **What I'm assuming**: You're a platform/infra team building for internal application developers, not building a developer tool product for external customers.
>
> Am I reading this right, or should I adjust my understanding?

**User:**

> Close but not quite. We're not an infra team — we're a small startup (12 devs) and everyone is drowning in setup overhead. There's no platform team. The idea is to build golden paths that reduce the decisions each dev has to make when starting something new.

**AI:**

> Ah, different context entirely. Not "platform team serves app teams" but "startup standardises its own practices so 12 developers stop reinventing the wheel on every new service/feature."
>
> That shifts the emphasis from provisioning infrastructure to **encoding decisions** — the value isn't in automating AWS setup, it's in having pre-made answers to "which database?", "how do we auth?", "what does our CI look like?" so individual devs don't deliberate on solved problems.
>
> Revised read:
>
> **The big idea**: Codify the startup's technical decisions into reusable templates and golden paths so developers start from proven patterns instead of making 50 setup decisions per project.
>
> **Driving this**: At 12 devs, every project starts differently. Onboarding takes too long because nothing is standardised. Decisions get re-made (sometimes inconsistently) rather than inherited.
>
> **Success**: New service goes from `git init` to deployed-with-CI in an hour. New developer can ship their first feature in week 1, not week 3.
>
> Is that closer?

**User:**

> Yes exactly. And the other thing — we want to make sure we don't end up with 4 different auth approaches and 3 different ORMs. It's about consistency as much as speed.

**AI:**

> Perfect. "Consistency" is the quality attribute that distinguishes this from just having good docs. The intent is about **enforced consistency** — not just "here are our patterns" but "these patterns are the default and deviation requires justification."
>
> I have enough to draft. Here's the captured intent:

### Output: `.intent/intent.md`

```markdown
# Intent: Developer Golden Paths

**Intent ID**: INT-001
**Captured**: 2026-05-21
**Actor**: user

## Context

12-developer startup with no platform team. Each new service/feature starts from scratch with ad-hoc technology choices. The result is inconsistency (multiple auth approaches, different ORMs, varied CI setups) and slow onboarding (3+ weeks to first feature for new devs). No existing standardisation beyond informal Slack conversations.

## Intent

Codify the startup's technical decisions into enforceable golden paths so developers inherit proven patterns by default and achieve consistency across services without a dedicated platform team.

## Motivation

At current growth rate, inconsistency compounds — every new hire inherits a different mental model. Onboarding cost scales linearly with codebase entropy. Acting now (at 12 devs) is dramatically cheaper than retrofitting at 30.

## Quality Attributes

- QA-001: Developer experience — golden paths must feel like acceleration, not bureaucracy
- QA-002: Consistency — services built from golden paths share auth, ORM, CI, and observability patterns
- QA-003: Escapability — teams can deviate with documented justification (ADR), not silently
- QA-004: Maintainability — golden paths evolve with the team's learning, not ossify

## Success Criteria

- SC-001: New service goes from init to deployed-with-CI in under 1 hour using a golden path
- SC-002: New developer ships their first feature within 5 working days of starting
- SC-003: 90% of services use the same auth approach (measured by codebase audit)
- SC-004: Deviations from golden paths are documented (ADR exists for each deviation)

## Assumptions

- The team will agree on "the one way" for auth, data access, and CI (confidence: medium — requires facilitated decision-making)
- Templates/scaffolding are sufficient — this doesn't require a runtime platform or service mesh (confidence: high)
- The 12 developers are senior enough to use templates without hand-holding (confidence: high)

## Clarifications

- CLR-001: OPEN — what's the current stack? (Language, frameworks, cloud provider) This shapes what the golden paths contain.
- CLR-002: OPEN — are there existing services that represent "the good pattern" we should encode, or are we designing from scratch?
```

### Key observations

1. **Three proposal rounds** — vague input → first proposal (wrong framing) → correction → refined proposal → second correction → alignment
2. **User's corrections were the most valuable signal** — "not an infra team" and "consistency as much as speed" both fundamentally reshaped the intent
3. **AI showed its reasoning** — "I'm interpreting this as platform team serves app teams" let the user catch the wrong assumption immediately
4. **Two CLR items remain OPEN** — the conversation surfaced enough for a valid intent, but technical context is still needed before steering
