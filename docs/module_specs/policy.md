Module Specification — domain/policy.py

Status: READY FOR IMPLEMENTATION
Version: 1.0
Tier: 0

1. Owns

This module owns the domain concept of a platform policy and its structural lifecycle state.

Policy
PolicyStatus
PolicyVerdict

2. Must NOT depend on

application/

infrastructure/

interface/

Redis, Postgres, filesystem, network, or any other I/O

Discovery mechanisms

Persistence

Human-review workflows

Runtime authorization

Policy registries

Allowed domain dependency:

domain.vocabulary

No other Zenith module imports are required.

3. Authority Boundary

MAY

Define Policy

Define PolicyStatus

Define PolicyVerdict

Validate structural/domain invariants of a Policy

Reject structurally invalid Policy states

MUST NOT

Discover policies

Persist policies

Activate or deactivate policies

Perform human review

Evaluate runtime authorization

Retrieve external state

Perform I/O

Decide when a lifecycle transition occurs

The domain validates whether a state is structurally valid.

The application layer owns how and when lifecycle transitions occur.

4. Contracts

PolicyStatus

Lifecycle states:

DISCOVERED
EXTRACTED
PENDING_REVIEW
APPROVED
ACTIVE
REVOKED

Lifecycle progression:

DISCOVERED
    ↓
EXTRACTED
    ↓
PENDING_REVIEW
    ↓
APPROVED
    ↓
ACTIVE
    ↓
REVOKED

The domain validates structural state consistency.

The application layer decides when a Policy transitions between states.

PolicyVerdict

Fixed policy outcomes:

ALLOW
DENY
REQUIRE_REVIEW
PROHIBITED

Policy

Required fields:

id: str
platform: str
operation: Operation
interface: Interface
verdict: PolicyVerdict
status: PolicyStatus
version: int
reviewed_by_human: bool

Operation and Interface are imported from:

domain.vocabulary

The module must not import any application, infrastructure, or interface implementation.

5. Structural Lifecycle Rules

The domain does not perform lifecycle transitions. It only rejects invalid combinations of fields.

Rule 1 — PROHIBITED policies cannot be ACTIVE

verdict == PROHIBITED
status == ACTIVE

must be rejected.

Rule 2 — ACTIVE policies require human review

status == ACTIVE
reviewed_by_human == False

must be rejected.

Rule 3 — APPROVED policies require human review

status == APPROVED
reviewed_by_human == False

must be rejected.

Valid examples

These states must be accepted:

PROHIBITED + REVOKED
ALLOW + ACTIVE + reviewed_by_human=True
REQUIRE_REVIEW + ACTIVE + reviewed_by_human=True
ALLOW + APPROVED + reviewed_by_human=True

The domain does not determine whether a policy SHOULD be approved or activated. It only determines whether the supplied state is structurally valid.

6. Invariants

A PROHIBITED Policy must never have ACTIVE status.

An ACTIVE Policy must have reviewed_by_human=True.

An APPROVED Policy must have reviewed_by_human=True.

Policy lifecycle transitions are application-owned.

The domain performs no I/O.

The domain does not retrieve external state.

The domain does not perform runtime authorization.

The domain does not perform policy discovery or persistence.

7. Required Tests

Tests must verify behavior, not implementation details.

def test_prohibited_policy_cannot_be_active():
    """PROHIBITED + ACTIVE is rejected."""

def test_active_policy_requires_human_review():
    """ACTIVE + reviewed_by_human=False is rejected."""

def test_approved_policy_requires_human_review():
    """APPROVED + reviewed_by_human=False is rejected."""

def test_reviewed_active_policy_is_valid():
    """ACTIVE + reviewed_by_human=True is accepted."""

def test_allow_active_policy_is_valid():
    """ALLOW + ACTIVE + reviewed_by_human=True is accepted."""

def test_approval_required_active_policy_is_valid():
    """REQUIRE_REVIEW + ACTIVE + reviewed_by_human=True is structurally valid."""

def test_no_forbidden_layer_imports():
    """Policy must not import application, infrastructure, or interface modules."""

The dependency-boundary test may use AST inspection.

8. Interface Exposed

Policy
PolicyStatus
PolicyVerdict

Expected construction shape:

Policy(
    id="...",
    platform="...",
    operation=Operation.EXECUTE,
    interface=Interface.API,
    verdict=PolicyVerdict.ALLOW,
    status=PolicyStatus.ACTIVE,
    version=1,
    reviewed_by_human=True,
)

9. Documentation

Codex must create/update:

domain/policy.py
tests/unit/domain/test_policy.py
domain/policy_struct.md

policy_struct.md must document:

ownership

dependencies

contracts

structural invariants

domain/application boundary

public interface

10. Explicit Scope

This implementation pass is limited to:

domain/policy.py
tests/unit/domain/test_policy.py
domain/policy_struct.md

Do not modify:

domain/vocabulary.py
domain/risk.py
domain/capability.py
domain/authorization.py
application/
infrastructure/
interface/

No speculative additions, abstractions, dependencies, or improvements.

If anything in this specification is ambiguous or conflicts with the existing repository, stop and report the ambiguity rather than guessing.