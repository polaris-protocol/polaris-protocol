"""
Polaris Gate — Stale State Demo
=================================
Shows the core failure mode Polaris prevents.

  Worker A observes state S1 and decides to act.
  Worker B commits a transition: S1 → S2.
  Worker A attempts execution from S1.
  Gate blocks. Worker A re-observes and retries.

Run from repo root:
    python reference/python/examples/stale_state.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../../")))

from gate import PolarisGate, Reason


class CanonicalStore:
    def __init__(self, ref): self._ref = ref
    def current(self):       return self._ref
    def advance(self, ref):  self._ref = ref


store = CanonicalStore("S1")
gate  = PolarisGate(store)

print("Polaris Gate — Stale State Demo")
print("=" * 44)

# Worker A observes S1
worker_a_ref = store.current()
print(f"\n[Worker A] observed: {worker_a_ref}")
print(f"[Worker A] decision: proceed with side effect")

# Worker B commits S1 → S2
print(f"\n[Worker B] commits: S1 → S2")
store.advance("S2")
print(f"[Canonical] current state: {store.current()}")

# Worker A attempts execution from S1
print(f"\n[Worker A] attempts execution (state_ref={worker_a_ref})")
decision = gate.authorize(worker_a_ref)
print(f"[Gate]     {decision}")
assert not decision.permitted
assert decision.reason == Reason.STALE_STATE_REFERENCE
print(f"\n→ BLOCKED (stale state)")
print(f"→ re-observe required")

# Worker A re-observes and retries
print(f"\n[Worker A] re-observes: {store.current()}")
worker_a_ref = store.current()
decision = gate.authorize(worker_a_ref)
print(f"[Gate]     {decision}")
assert decision.permitted
print(f"\n→ PERMIT (current canonical state)")

print("\n" + "=" * 44)
print("[PASS] stale state demo complete")
