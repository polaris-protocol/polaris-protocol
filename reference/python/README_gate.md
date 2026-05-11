# Polaris Gate

**Blocks execution when the request state is no longer the committed canonical state.**

```python
gate = PolarisGate(canonical_store)

decision = gate.authorize(state_ref)

if decision.permitted:
    execute()
else:
    reject(decision.reason)
    # → "STALE_STATE_REFERENCE"
```

Or raise on block:

```python
gate.assert_authorized(state_ref)
execute()  # only reaches here if authorized
```

---

## The problem

A system observes state `S0` and decides to act.
Before the action executes, another process commits a transition to `S1`.
The action executes anyway — from superseded state.

Polaris Gate blocks this before the side effect is produced.

---

## Where to place the gate

Place it immediately before the side effect. One line.

### Payment

```python
def send_payment(request):
    gate.assert_authorized(request.state_ref)

    payment_provider.charge(
        user_id=request.user_id,
        amount=request.amount,
    )
```

If the state has been superseded: `BLOCK: STALE_STATE_REFERENCE`.
No payment from stale state.

### Workflow / external call

```python
def execute_activity(activity_input):
    gate.assert_authorized(activity_input.state_ref)

    external_api.call(activity_input.payload)
```

If the workflow resumed from a stale checkpoint,
execution is blocked before the call.

See `examples/` for trading orders and agent tool calls.

---

## How it works

The gate owns the canonical state reference.
The caller provides only the state they observed.

```python
class PolarisGate:
    def authorize(self, state_ref: str) -> Decision:
        current_ref = self._store.current()
        if state_ref != current_ref:
            return Decision(False, "STALE_STATE_REFERENCE")
        return Decision(True)
```

`canonical_store` is any object with a `.current() -> str` method.

---

## Rejection reasons

| Reason | When |
|---|---|
| `STALE_STATE_REFERENCE` | `state_ref` ≠ current canonical state |
| `INVALID_STATE_REFERENCE` | caller did not provide a valid state reference |
| `EXECUTION_WITHOUT_COMMIT` | no current canonical state exists |

---

## Minimum test

```python
def test_blocks_stale():
    store = SimpleStore(current="S1")
    gate  = PolarisGate(store)

    decision = gate.authorize("S0")

    assert not decision.permitted
    assert decision.reason == "STALE_STATE_REFERENCE"
```

---

## Background

Polaris Gate implements the execution gate from the Polaris Protocol —
a structural model for execution authority in distributed systems.

Specification: [github.com/polaris-specs/polaris-protocol](https://github.com/polaris-specs/polaris-protocol)
Paper: SRDS 2026 (submitted May 2026)
