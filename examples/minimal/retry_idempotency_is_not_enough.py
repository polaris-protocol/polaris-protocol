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

executed = set()

def execute(tx_id, state_ref, gate):
    if tx_id in executed:
        print(f"SKIP: {tx_id} already executed (idempotent)")
        return
    if not gate.permit(state_ref):
        print(f"BLOCK: {tx_id} — state '{short(state_ref)}' "
              f"is superseded (idempotency does not help here)")
        return
    executed.add(tx_id)
    print(f"PERMIT: {tx_id} executed")

S1 = {"balance": 100, "version": 1}
gate = StateGate(S1)
ref1 = h(S1)

S2 = {"balance": 50, "version": 2}
gate.commit(S2)

execute("tx-001", ref1, gate)
execute("tx-001", ref1, gate)
