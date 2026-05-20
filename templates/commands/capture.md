---
description: Capture structured business intent from a big idea description — Phase 1 of IDD.
handoffs:
  - label: Steer Architecture
    agent: intent.steer
    prompt: Create steering decisions for this intent
    send: true
  - label: Clarify Intent
    agent: intent.clarify
    prompt: Identify under-specified areas in the intent
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/intent.capture` is the big idea description. This might be a sentence, a paragraph, or a path to an existing document. Your job is to structure it into the seven-section intent format.

### Execution Flow

1. **Parse the big idea** from user input.
   - If empty: ERROR "No idea description provided. Describe the big idea you want to capture."
   - If a file path: read the file and extract the seven sections from its content.

2. **Create the intent directory** if it doesn't exist:
   ```
   .intent/
   ```

3. **Load template**: Read `templates/intent-template.md` for required structure.

4. **Extract and structure the seven sections**:

   For each section, follow these rules:

   **Context**: Extract environmental facts, constraints, prior art. If the user mentions existing systems, regulatory requirements, team structure, or organisational context — it goes here. DO NOT put solution ideas here.

   **Intent**: Distill the big idea into a SINGLE declarative sentence. This is the hardest part. Rules:
   - Must be falsifiable (you can verify if the shipped system satisfies it)
   - Must be a single sentence (≤ 3 sentence boundaries)
   - Must describe the OUTCOME, not the approach
   - If you cannot distill to one sentence, ask the user to clarify which aspect is the primary intent

   **Motivation**: Extract urgency, timing, cost of inaction. WHY NOW, not why at all.

   **Quality Attributes**: Extract NFRs. Tag each QA-NNN. If the user doesn't mention NFRs, infer reasonable ones from the domain and mark assumptions. Common categories: latency, throughput, availability, data residency, security posture, compliance, scalability.

   **Success Criteria**: Extract observable outcomes. Tag each SC-NNN. Each must be testable. If the user provides vague success ("it should work well"), push for specifics. Limit: maximum 7 success criteria. If more exist, the intent is too broad — suggest splitting.

   **Assumptions**: Extract beliefs not yet verified. Tag confidence (high/medium/low). Common sources: technology assumptions, team capability assumptions, data availability assumptions, timeline assumptions.

   **Clarifications**: Identify gaps or ambiguities. Each gets a CLR-NNN ID. If something is genuinely unclear and would affect architecture, mark it OPEN. Limit: maximum 5 open clarifications. More than 5 suggests the intent isn't ready for capture — the user needs more discovery.

5. **Validate the captured intent**:
   - `context` is non-empty
   - `intent` is a single declarative sentence
   - `motivation` is non-empty
   - `success_criteria` has at least 1 item
   - No more than 5 OPEN clarifications
   - No more than 7 success criteria (if more, suggest splitting the intent)

6. **Write `.intent/intent.md`** using the template structure.

7. **Write audit entry** to `.intent/audit.md`:
   ```markdown
   ## [ISO 8601 timestamp] — Intent captured

   **Actor**: [user/agent]
   **Phase**: capture
   **Outcome**: [complete | incomplete — N validation errors]
   **Intent summary**: [the single sentence]
   ```

8. **Update state** in `.intent/state.json`:
   ```json
   {
     "current_phase": "capture",
     "phase_complete": true,
     "intent_id": "INT-001",
     "captured_at": "<timestamp>",
     "validation_errors": []
   }
   ```

9. **Report completion**: Show the intent summary, any open clarifications, and readiness for `/intent.steer`.

## Guidelines

- This is a BIG IDEA capture, not a feature specification. If the user describes something that sounds like a single user story, ask whether there's a larger initiative it belongs to.
- Make informed guesses for Quality Attributes and Assumptions based on the domain — document them clearly.
- The intent sentence is the most important output. Spend effort getting it right.
- DO NOT make architectural decisions. That's Phase 2.
- DO NOT decompose into features. That's Phase 4.
- If the user provides a document/file path, read it and synthesise — don't just copy sections verbatim.
