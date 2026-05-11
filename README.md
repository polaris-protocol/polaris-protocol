# Polaris Protocol

**No side effect may occur unless it is authorized from the current committed canonical state.**

Distributed systems execute from state that may be stale, superseded by a concurrent transition, or invalidated before execution begins. Logs record what happened. Audit reconstructs it. Neither establishes whether execution was authorized to occur from the state it acted upon.

Polaris makes this constraint explicit and enforces it at execution time.

---

## The constraint

In a commit-gated system, execution follows this path:

```
Proposed Transition → Validation → Commit Authority
→ Canonical State → Execution Gate → Side Effect
```

If an execution request references a state that is no longer canonical, the gate returns `BLOCK` before any effect is produced.

Three structural invariants hold in every conformant implementation:

- **I1** — Each committed state has at most one successor
- **I2** — No transition commits without passing validation
- **I3** — Execution is permitted only from the current canonical state

---

## Quick start

```bash
python reference/python/examples/rejection_demo.py
```

```bash
pip install cryptography pytest
python -m pytest reference/python/tests/ -v
```

---

## What this is not

**Not a blockchain.** Assumes a designated commit authority.

**Not an audit log.** Operates before effects, not after.

**Not a workflow engine.** Does not orchestrate business logic.

**Not a full runtime framework.** Provides a minimal execution gate and a normative specification.

---

## Specification

| Document | Purpose |
|---|---|
| `SPEC.md` | Complete normative specification v1.0 |
| `QUICKSTART.md` | Five requirements for Level 1 conformance |
| `KNOWN-GAPS.md` | Limitations deferred to v1.1 |
| `REFERENCE-HASHES.md` | Canonical hash vectors for implementers |

---

## Status

- Version: 1.0
- License: Specification — CC-BY-4.0 / Reference implementations — Apache 2.0
- Conformance: Level 1 (reference implementation)
- Paper: SRDS 2026 (submitted May 2026)

Implementations are invited.
Questions and errata: open an issue tagged `[conformance]` or `[errata]`
