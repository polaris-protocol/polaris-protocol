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

S1 = {"order_status": "pending", "version": 1}
gate = StateGate(S1)

checkpoint = {"state_ref": h(S1), "action": "approve_payment"}
print(f"Checkpoint saved: state_ref={short(checkpoint['state_ref'])}")

S2 = {"order_status": "cancelled", "version": 2}
gate.commit(S2)
print("State advanced: order cancelled")

state_ref = checkpoint["state_ref"]
if gate.permit(state_ref):
    print("PERMIT: approve_payment executed")
else:
    print("BLOCK: checkpoint survived — context did not")
