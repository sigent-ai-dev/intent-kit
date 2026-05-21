# Voice Agent Architecture — Intent Capture via Conversation

**Status**: Design (issue #26)
**Date**: 2026-05-21

## Overview

A voice interface for `/intent.capture` that enables business stakeholders to describe their big ideas verbally, with an AI agent conducting structured propose-and-steer elicitation and producing a valid `.intent/intent.md`.

```
Stakeholder speaks big idea
    → Voice agent (Nova Sonic 2) proposes interpretation
    → Stakeholder corrects/confirms verbally
    → Agent writes .intent/intent.md
    → Developer notified, continues from /intent.steer
```

## Architecture

### System Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           Entry Points                                     │
├─────────────┬────────────────┬──────────────────┬────────────────────────┤
│  Browser    │  Teams Bot     │  Zoom Bot        │  Phone (SIP)           │
│  (WebRTC)   │  (Bot SDK)     │  (Bot SDK)       │  (PJSIP bridge)       │
└──────┬──────┴───────┬────────┴────────┬─────────┴───────────┬────────────┘
       │              │                 │                      │
       └──────────────┴─────────────────┴──────────────────────┘
                                    │
                              WebSocket / Audio Stream
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        Voice Agent Service (ECS Fargate)                   │
│                                                                            │
│  ┌────────────────┐    ┌──────────────────────┐    ┌──────────────────┐  │
│  │  Audio Router   │───▶│  Nova Sonic 2 Engine    │───▶│  Response Audio  │  │
│  │  (WebSocket)    │    │  (STT + TTS + LLM)   │    │  (Streaming)     │  │
│  └────────────────┘    └──────────┬───────────┘    └──────────────────┘  │
│                                   │                                        │
│                          ┌────────▼────────┐                              │
│                          │  Strands Agents       │                              │
│                          │  Workflow         │                              │
│                          │                   │                              │
│                          │  ┌─────────────┐ │                              │
│                          │  │ Elicitation │ │                              │
│                          │  │ Agent       │ │                              │
│                          │  └─────────────┘ │                              │
│                          │  ┌─────────────┐ │                              │
│                          │  │ Section     │ │                              │
│                          │  │ Mapper      │ │                              │
│                          │  └─────────────┘ │                              │
│                          │  ┌─────────────┐ │                              │
│                          │  │ Validator   │ │                              │
│                          │  └─────────────┘ │                              │
│                          └─────────┬────────┘                              │
│                                    │                                        │
│                          ┌─────────▼────────┐                              │
│                          │  Output Writer    │                              │
│                          │  (.intent/*.md)   │                              │
│                          └──────────────────┘                              │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                     ┌──────────────────────────┐
                     │  Notification (nexctl)    │
                     │  Slack / MQTT → developer │
                     └──────────────────────────┘
```

### Component Responsibilities

| Component | Role | Technology |
|-----------|------|------------|
| **Audio Router** | Accept connections from all entry points, normalise to bidirectional audio stream | WebSocket server, audio codec handling |
| **Nova Sonic 2 Engine** | Real-time STT, TTS, and conversational LLM in a single streaming session | Amazon Nova Sonic 2 (aws-sdk-bedrock-runtime) |
| **Strands Agents Workflow** | Orchestrate the elicitation conversation through propose-and-steer phases | Strands Agents (Python) |
| **Elicitation Agent** | Implement propose-and-steer logic — propose interpretation, handle corrections, track coverage | LLM with structured prompts (Nova Sonic 2 native) |
| **Section Mapper** | Map conversational exchanges to the 7 intent sections in real-time | Rule-based + LLM classification |
| **Validator** | Validate the emerging intent against schema rules (single sentence, ≤7 SC, etc.) | Same logic as `intent check` |
| **Output Writer** | Write `.intent/intent.md`, `state.json`, `audit.md` when capture completes | File I/O or git commit via API |
| **Notification** | Alert developer that capture is complete, provide link to continue | Slack (nexctl pattern) or email |

## Strands Agents Workflow

```
┌─────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────┐
│  START  │────▶│  LISTEN &     │────▶│  PROPOSE       │────▶│  AWAIT   │
│         │     │  UNDERSTAND   │     │  INTERPRETATION│     │  RESPONSE│
└─────────┘     └──────────────┘     └───────────────┘     └────┬─────┘
                                                                  │
                        ┌─────────────────────────────────────────┘
                        │
                ┌───────▼───────┐
                │  ROUTE         │
                │  RESPONSE      │
                └───┬───┬───┬───┘
                    │   │   │
         ┌──────────┘   │   └──────────┐
         ▼              ▼              ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │ CONFIRM  │   │ CORRECT  │   │ REDIRECT │
  │ (accept) │   │ (adjust) │   │ (reframe)│
  └────┬─────┘   └────┬─────┘   └────┬─────┘
       │               │               │
       └───────────────┴───────────────┘
                       │
               ┌───────▼───────┐
               │  CHECK         │
               │  COVERAGE      │
               └───┬───────┬───┘
                   │       │
          ┌────────┘       └────────┐
          ▼                         ▼
  ┌──────────────┐          ┌──────────────┐
  │  MORE NEEDED │          │  COMPLETE    │
  │  (next topic)│          │  (validate)  │
  └──────┬───────┘          └──────┬───────┘
         │                         │
         └──── back to ────────────│
              PROPOSE              │
                                   ▼
                           ┌──────────────┐
                           │  SUMMARISE & │
                           │  CONFIRM     │
                           └──────┬───────┘
                                  │
                                  ▼
                           ┌──────────────┐
                           │  WRITE       │
                           │  OUTPUT      │
                           └──────────────┘
```

### State Tracking

The Strands Agents state maintains:

```python
class CaptureState(TypedDict):
    # Conversation state
    transcript: list[dict]          # Full conversation history
    current_interpretation: str     # Latest proposed big idea sentence
    corrections: list[dict]         # User corrections (high-value signal)

    # Section coverage
    sections_covered: dict[str, str]  # section_name → content extracted
    sections_confidence: dict[str, float]  # section_name → 0-1 confidence

    # Progress
    proposal_rounds: int            # Max 3 before proceeding
    alignment_reached: bool         # User confirmed interpretation
    coverage_complete: bool         # All 7 sections have content
```

## Entry Points

### 1. Browser (MVP — lowest complexity)

Proven by trainline-voice-poc. User opens a web page, clicks "Start Capture", speaks.

```
Browser (Web Audio API + WebSocket)
    → API Gateway (WebSocket)
    → ECS Fargate (Voice Agent)
    → Nova Sonic 2 (bidirectional audio stream)
```

### 2. Teams Call

Voice agent joins a Teams meeting as a bot participant.

```
Teams meeting invite includes bot
    → Teams Bot SDK receives audio stream
    → Forwards to Voice Agent via WebSocket
    → Bot speaks responses back into meeting
```

### 3. Zoom Call

Same pattern as Teams with Zoom's bot SDK.

```
Zoom meeting with bot participant
    → Zoom Bot SDK receives audio stream
    → Forwards to Voice Agent via WebSocket
    → Bot speaks responses back into meeting
```

### 4. Phone (SIP)

Proven by trainline-voice-poc's PJSIP integration. User dials a number.

```
Phone call → SIP trunk → PJSIP bridge → WebSocket → Voice Agent
```

## Propose-and-Steer Verbal Protocol

The elicitation agent follows the same principles as the text-based `/intent.capture` but adapted for voice:

### Opening

> "Hi, I'm here to help capture the intent behind your initiative. Tell me about the big idea — what are you trying to achieve? Don't worry about structure, just describe it naturally."

### After initial description — Propose

> "Okay, here's what I'm hearing. [Proposes one-sentence interpretation]. The main thing driving this seems to be [inferred motivation]. Am I on the right track, or should I adjust my understanding?"

### On correction

> "Got it — [acknowledges correction, restates]. That changes how I'm thinking about [affected section]. Let me ask about one thing: [single focused question if needed]."

### On coverage gap

> "One area I'd like to understand better is [uncovered section]. Can you tell me [specific question mapped to section]?"

### On completion

> "I think I have a good picture. Let me summarise what I've captured:
> - The intent is: [one sentence]
> - The key success criteria are: [list SC-NNN]
> - Open questions I still have: [CLR items]
>
> Does that capture it? I'll write this up and notify your developer to continue with the architecture decisions."

### Barge-in Handling

Essential for propose-and-steer — the stakeholder needs to interrupt when the AI's interpretation is wrong. Nova Sonic 2's native barge-in support (proven <800ms in trainline-poc) handles this. When interrupted:

1. Stop speaking immediately
2. Listen to the correction
3. Acknowledge: "Sorry, let me adjust..."
4. Incorporate correction and continue

## Meeting Chair Mode (Group Sessions)

For multi-stakeholder capture sessions:

1. **Introduction** — agent introduces itself and the session purpose
2. **Round-robin** — asks each participant for their perspective on the big idea
3. **Synthesis** — proposes unified interpretation, asks for group confirmation
4. **Conflict resolution** — if stakeholders disagree, surfaces the tension: "I'm hearing two different priorities here..."
5. **Parking lot** — topics that need offline resolution become CLR-NNN items
6. **Close** — summarises, lists action items, thanks participants

## Developer Handoff

When capture completes:

1. Voice agent writes files to configured location (local project dir or shared git repo)
2. Notification sent via Slack (using nexctl's MQTT → Lambda → Slack pattern):
   ```
   🎯 Intent captured: "Modernise portfolio construction system"
   Project: portfolio-modernisation
   Captured by: voice-session with @sarah, @james
   Open clarifications: 2
   
   Next: Run /intent.steer to begin architectural steering
   ```
3. Developer opens project, runs `intent check --verbose` to see the captured state
4. Continues with `/intent.steer` as normal

## Runtime Decision: Fargate (not AgentCore)

**Decision**: ECS Fargate for the voice agent service.

**Why not AgentCore**: AgentCore is request-response only — no WebSocket support, no bidirectional streaming, no persistent connections. Nova Sonic 2 requires `InvokeModelWithBidirectionalStream` (HTTP/2 duplex event streaming) which is fundamentally incompatible with AgentCore's invocation model.

| Requirement | AgentCore | Fargate |
|-------------|-----------|---------|
| WebSocket connections | Not supported | Supported (ALB + persistent TCP) |
| Bidirectional audio streaming | Not supported | Supported (long-running process) |
| 5-30 min continuous session | Not possible (discrete invocations) | Supported |
| Nova Sonic 2 integration | Impossible (needs duplex stream) | Works (BidiAgent pattern) |
| Managed session state | Built-in | Must implement (DynamoDB or in-memory) |

**AgentCore's role**: Could potentially host non-voice agents (e.g., the notification/handoff logic, or a text-based fallback agent), but the core voice service must run on Fargate.

### Nova Sonic 2 Connection Constraints

- **8-minute connection limit** — Nova Sonic 2 sessions auto-terminate after 8 minutes
- **Auto-reconnect**: Strands SDK's `BidiAgentLoop` handles this via `_restart_connection()` — replays conversation history (capped at 200KB) on new connection
- **175-second silence timeout** — connection drops if no audio for ~3 minutes
- **HTTP/2 duplex event stream** — not standard WebSocket; uses AWS Smithy event stream protocol

### Strands SDK Integration

The voice agent uses `strands-agents[bidi]` (server-side, no PyAudio dependency):

```python
from strands.experimental.bidi import BidiAgent, BidiNovaSonicModel

model = BidiNovaSonicModel(model_id="amazon.nova-sonic-v2:0")
agent = BidiAgent(model=model, tools=[...])
```

Custom `BidiInput`/`BidiOutput` protocols bridge WebSocket clients to the agent without local audio hardware.

## Infrastructure

### Reusable (from trainline-voice-poc):
- **ECS Fargate** — serverless containers for the voice agent service
- **ALB** — WebSocket-aware load balancing (preferred over API Gateway for long-lived connections)
- **Nova Sonic 2 SDK** — `strands-agents[bidi]` wrapping `InvokeModelWithBidirectionalStream`
- **Cognito** — authentication for browser sessions
- **WAF** — request filtering and rate limiting
- **CloudWatch** — logging and metrics

### New components needed:
- **BidiAgent elicitation workflow** — propose-and-steer logic as Strands Agent tools
- **WebSocket server** — FastAPI + Uvicorn bridging browser audio to BidiAgent
- **Teams/Zoom bot adapters** — audio bridging to meeting platforms
- **Output writer** — file I/O to produce `.intent/` artifacts
- **nexctl integration** — notification on completion
- **Session state store** — DynamoDB for conversation state persistence across reconnects

## MVP Scope

**Phase 1 — Browser only:**
- Web page with "Start Capture" button
- Nova Sonic 2 for voice conversation
- Strands Agents workflow implementing propose-and-steer
- Writes `.intent/intent.md` to a configurable location
- No meeting integration, no phone, no notification

**Phase 2 — Meeting integration:**
- Teams bot that can join a meeting
- Meeting chair mode with multi-participant handling
- Slack notification on completion

**Phase 3 — Full platform:**
- Zoom integration
- Phone/SIP dial-in
- nexctl notification integration
- Recording consent and transcript archival

## Open Questions

1. **File output location** — where does the voice agent write `.intent/`? Options: local git repo (requires access), S3 bucket (developer pulls), API call to a service
2. **Auth for browser** — Cognito (AWS-native) or generic OAuth (more portable)?
3. **Nova Sonic 2 region availability** — currently us-east-1 only; latency for non-US users?
4. **Cost model** — Nova Sonic 2 pricing per minute of conversation; acceptable for design sessions?
5. **Privacy** — should conversation audio be retained or discarded after transcript extraction?
