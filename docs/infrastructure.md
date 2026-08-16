# Zenith Infrastructure

> **Status:** LOCKED ARCHITECTURAL REFERENCE  
> **Version:** 1.0  
> **Purpose:** Complete infrastructure map of Zenith from user interaction to external-world execution and back.

---

# 1. System Overview

Zenith is a persistent authority and state system, not a permanently resident reasoning process.

Its state remains available continuously while reasoning processes may wake on demand, execute a bounded reasoning cycle, persist their results, and terminate.

```text
                                USER
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      ZENITH CORE        │
                    │ Persistent Authority    │
                    │ Identity + Memory       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      TASK MANAGER       │
                    │ Lifecycle + Dormancy    │
                    │ Parent / Child Tasks    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌──────────────────┐     ┌──────────────────────┐
          │ REASONING /      │     │ EVENT & OBSERVATION  │
          │ PLANNING         │     │ LAYER                │
          └────────┬─────────┘     └──────────┬───────────┘
                   │                          │
                   ▼                          ▼
          ┌──────────────────┐     ┌──────────────────────┐
          │ CONTEXT          │     │ CONNECTORS           │
          │ ASSEMBLY         │     │ Gmail / GitHub /     │
          │                  │     │ Calendar / etc.      │
          └────────┬─────────┘     └──────────┬───────────┘
                   │                          │
                   ▼                          ▼
          ┌──────────────────┐     ┌──────────────────────┐
          │ PLAN             │     │ NORMALIZATION        │
          │       ↓          │     │        ↓             │
          │ SANITY CHECK     │     │ RECONCILIATION       │
          │       ↓          │     └──────────┬───────────┘
          │ REVALIDATE       │                │
          └────────┬─────────┘                │
                   │                          │
                   └────────────┬─────────────┘
                                ▼
                       ┌─────────────────┐
                       │   WORLD STATE   │
                       │ Facts           │
                       │ Inferences      │
                       │ Events          │
                       └────────┬────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │ DECISION / ATTENTION    │
                    │                         │
                    │ ACT / DELEGATE / WAIT   │
                    │ ASK / SURFACE / IGNORE  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   CAPABILITY BROKER     │
                    │                         │
                    │ Trust                   │
                    │ Delegation              │
                    │ Policy                  │
                    │ Risk                    │
                    │ Constraints              │
                    │ Resource Coordination   │
                    │ Approval                │
                    │ Telemetry               │
                    │ Replay Protection       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    EXECUTION LAYER      │
                    │                         │
                    │ API / MCP / Browser     │
                    │ Device / A2A             │
                    └────────────┬────────────┘
                                 │
                                 ▼
                         EXTERNAL WORLD