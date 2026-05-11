"""
Polaris Gate — Rejection Demo
==============================
Demonstrates the three structural rejection reasons.

Run from repo root:
    python reference/python/examples/rejection_demo.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gate import PolarisGate, Reason


class CanonicalStore:
    def __init__(self, ref): self._ref = ref
    def current(self): return self._ref


print("Polaris Gate — Rejection Demo")
print("=" * 44)

# 1. STALE_STATE_REFERENCE
print("\n[1] Stale state reference")
store = CanonicalStore("sha256:S1")
gate  = PolarisGate(store)
d = gate.authorize("sha256:S0")
print(f"    state_ref=S0, current=S1")
print(f"    → {d}")
assert d.reason == Reason.STALE_STATE_REFERENCE

# 2. EXECUTION_WITHOUT_COMMIT
print("\n[2] No canonical state exists")
store = CanonicalStore(None)
gate  = PolarisGate(store)
d = gate.authorize("sha256:S0")
print(f"    state_ref=S0, current=None")
print(f"    → {d}")
assert d.reason == Reason.EXECUTION_WITHOUT_COMMIT

# 3. INVALID_STATE_REFERENCE
print("\n[3] Invalid state reference")
store = CanonicalStore("sha256:S1")
gate  = PolarisGate(store)
d = gate.authorize(None)
print(f"    state_ref=None")
print(f"    → {d}")
assert d.reason == Reason.INVALID_STATE_REFERENCE

# 4. PERMIT
print("\n[4] Authorized execution")
store = CanonicalStore("sha256:S1")
gate  = PolarisGate(store)
d = gate.authorize("sha256:S1")
print(f"    state_ref=S1, current=S1")
print(f"    → {d}")
assert d.permitted

print("\n" + "=" * 44)
print("[PASS] rejection demo complete")
