# Polaris Protocol

A protocol for commit-gated execution and causal integrity.

Polaris enforces one constraint:

> No side effect may occur unless it is the result of a committed,
> validated transition — and that fact must be independently verifiable.

Execution authority is structurally bound to canonical state.
Enforced by construction, not policy.

---

## Problem

Systems execute from state.

That state may be stale, invalidated by a concurrent transition, or
superseded before execution began. The system does not know. Execution
occurs regardless.

This is not an edge case. It is the default condition of every widely
deployed distributed system.

Logs record what happened. Audit reconstructs the sequence. Replay
reproduces the effects. These describe execution — they do not
establish authority to execute.

It is an absence of definition. No existing architecture specifies
execution authority as a structural property of committed canonical
state. The property has never been defined, enforced, or independently
verifiable.

Polaris defines it.

---

## Model

Polaris defines commit-gated execution.

Every action follows a deterministic progression:
Proposed Transition → Validation Pipeline → Commit Authority → Canonical State → Execution Gate → Side Effect

If any step fails, execution does not occur. No bypass path exists
in a conformant implementation.

Three structural invariants hold by construction:

- **I1** — For any committed state, successor is a partial function:
  defined for at most one next state.
- **I2** — No transition becomes committed without satisfying
  validation conditions.
- **I3** — Execution is permitted only when the request references
  the current canonical state.

From I1–I3 a non-trivial consequence follows: two independent
conformant implementations, given the same history, will permit
exactly the same set of execution effects — without communication,
without shared state, without trust.

Execution authority is verifiable by anyone. Trusted by none.

---

## What Polaris Is Not

**Not a blockchain.** A blockchain records what happened. Polaris
prevents unauthorized execution from happening in the first place.
Assumes a designated commit authority.

**Not an audit log.** Logs record what happened. Audit reconstructs
it. Replay reproduces it. None of these establish that execution was
structurally authorized to occur from the state it acted upon.
Polaris closes that gap — before execution, not after.

**Not a workflow engine.** Does not orchestrate business logic or
process flows.

**Not a policy engine.** Does not evaluate arbitrary runtime policy.

**Not a runtime framework.** This repository defines the
specification, not an implementation.

---

## Specification

| Document | Purpose |
|---|---|
| `SPEC.md` | Complete normative specification v1.0 |
| `QUICKSTART.md` | Minimal conformance path — five requirements |
| `KNOWN-GAPS.md` | Acknowledged limitations deferred to v1.1 |
| `REFERENCE-HASHES.md` | Canonical reference hash values for implementers |

---

## Reference Harness

An executable conformance harness is available under `reference/python/`.
17 tests exercise I1, I2, and I3 by construction.

```bash
pip install cryptography pytest
python -m pytest reference/python/tests/ -v
```

### Demo

The harness below demonstrates the invariants in practice.

```bash
python reference/python/examples/golden_chain.py
```
[PASS] valid chain verified

```bash
python reference/python/examples/tampered_chain.py
```
[FAIL]   tampered record detected at sequence 2
[REJECT] execution from stale state_ref
[REJECT] execution without commit

---

## Where to Start

**Implementing Polaris:** Read `QUICKSTART.md` first. Five
requirements define Level 1 conformance.

**Understanding the architecture:** Read `SPEC.md` (Section A →
Section G), then the section relevant to the component you are
building.

**Verifying conformance:** Read `SPEC.md` Section K for the
self-declaration checklist and PCIS-1 test specification.

**Checking your serialization:** See `REFERENCE-HASHES.md`.

---

## Technical Report

Lindberg, Daniel. "Polaris Protocol: Commit-Gated Execution and
Causal Integrity." POLARIS-TR-2026-001, v0.5, April 2026.

- Paper: https://polaris-protocol.org/paper/
- Zenodo: https://zenodo.org/records/19669105

---

## Status
Version:      1.0
License:      Specification — CC-BY-4.0
Reference implementations — Apache 2.0
Conformance:  Self-declared (Level 1)
PCIS-1 suite in development

Implementations are invited. Questions and errata: open an issue
tagged `[conformance]` or `[errata]`.
