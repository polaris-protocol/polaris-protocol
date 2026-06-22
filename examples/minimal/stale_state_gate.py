import hashlib, json

def h(state):
    return hashlib.sha256(
        json.dumps(state, sort_keys=True).encode()
    ).hexdigest()

def short(ref):
    return ref[:12]

class StateGate:
    def __init__(self, state):
        self.canonical = h(state)

    def commit(self, new_state):
        self.canonical = h(new_state)

    def permit(self, state_ref):
        return state_ref == self.canonical

S1 = {"balance": 100, "version": 1}
gate = StateGate(S1)
planned_ref = h(S1)

S2 = {"balance": 50, "version": 2}
gate.commit(S2)

if gate.permit(planned_ref):
    print("PERMIT: execute side effect")
else:
    print(f"BLOCK: state '{short(planned_ref)}' is superseded "
          f"(current: '{short(gate.canonical)}')")
