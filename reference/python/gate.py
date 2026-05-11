"""
Polaris Gate
============
Blocks execution when the request state is no longer
the committed canonical state.

Usage:
    gate = PolarisGate(canonical_store)
    decision = gate.authorize(state_ref)

    if decision.permitted:
        execute()
    else:
        reject(decision.reason)
        # → "STALE_STATE_REFERENCE"

Or raise on block:
    gate.assert_authorized(state_ref)
    execute()
"""

from dataclasses import dataclass
from typing import Optional


class Reason:
    STALE_STATE_REFERENCE    = "STALE_STATE_REFERENCE"
    EXECUTION_WITHOUT_COMMIT = "EXECUTION_WITHOUT_COMMIT"
    INVALID_STATE_REFERENCE  = "INVALID_STATE_REFERENCE"


@dataclass(frozen=True)
class Decision:
    permitted: bool
    reason: Optional[str] = None

    def __str__(self) -> str:
        if self.permitted:
            return "[PERMIT]"
        return f"[BLOCK] {self.reason}"


class ExecutionNotAuthorizedError(Exception):
    """Raised by assert_authorized when execution is not permitted."""
    pass


class PolarisGate:
    """
    Execution gate. Owns the canonical state reference.
    Caller provides only the state_ref they observed.
    """

    def __init__(self, canonical_store):
        """
        Args:
            canonical_store: Any object with a .current() -> str method
                             returning the current canonical state hash.
        """
        self._store = canonical_store

    def authorize(self, state_ref: str) -> Decision:
        """
        Returns PERMIT if state_ref matches current canonical state.
        Returns BLOCK with a structured reason otherwise.

        Args:
            state_ref: Hash of the state the caller observed.
        """
        if not isinstance(state_ref, str) or not state_ref:
            return Decision(False, Reason.INVALID_STATE_REFERENCE)

        current_ref = self._store.current()

        if current_ref is None:
            return Decision(False, Reason.EXECUTION_WITHOUT_COMMIT)

        if state_ref != current_ref:
            return Decision(False, Reason.STALE_STATE_REFERENCE)

        return Decision(True)

    def assert_authorized(self, state_ref: str) -> None:
        """
        Raises ExecutionNotAuthorizedError if execution is not permitted.
        Use when an exception is more natural than a return value.

        Args:
            state_ref: Hash of the state the caller observed.
        """
        decision = self.authorize(state_ref)
        if not decision.permitted:
            raise ExecutionNotAuthorizedError(decision.reason)
