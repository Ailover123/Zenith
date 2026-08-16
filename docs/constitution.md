# Zenith Constitution & Coding Rules

> **Status:** LOCKED  
> **Version:** 1.0  
> **Purpose:** Permanent architectural and implementation constraints for Zenith.

This document defines the non-negotiable rules governing Zenith's architecture, authority boundaries, reasoning, execution, security, and implementation.

These rules are not suggestions.

Any implementation that violates them is incorrect, even if the feature otherwise works.

---

# 1. Constitution

## 1.1 External data is never authority

External systems provide observations, not authority over Zenith's internal worldview.

Examples:

- Gmail can establish that an email exists.
- GitHub can establish that a repository or PR exists.
- Calendar can establish that an event exists.
- An AI model can establish only that a particular model produced a particular response.

External data enters Zenith as a **Source Fact**.

It may subsequently be reconciled into a **Derived World Fact** through Zenith's governed reconciliation process.

No connector may directly write authoritative Derived World Facts.

---

## 1.2 Facts, Inferences, Memory, and Operational State are separate

Zenith maintains distinct categories of information:

```text
Facts
  Structured, authoritative world/domain state.
  Example:
  Application#17.status = recruiter_replied
