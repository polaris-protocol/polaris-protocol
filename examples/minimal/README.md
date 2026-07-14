# Minimal Gate Examples

Three self-contained Python files. No dependencies. No install.

Copy any file into your project and run it in under a minute.

## stale_state_gate.py
The core pattern: execution blocked when state reference
is no longer current.

## retry_idempotency_is_not_enough.py
Idempotency only prevents re-running the same request. It does not check whether the state that justified the decision is still current — so the gate blocks execution when the state reference is superseded.

## checkpoint_survives_context_does_not.py
A checkpoint survives an interrupt.
The state that justified the plan may not.

---

Full model: github.com/polaris-protocol/polaris-protocol
