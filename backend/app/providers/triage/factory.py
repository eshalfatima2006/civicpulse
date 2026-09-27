import os

from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import SimulatedTriage


def get_provider() -> SimulatedTriage | RuleBasedTriage:
    provider = os.getenv("TRIAGE_PROVIDER", "rules").lower()
    if provider == "simulated":
        return SimulatedTriage()
    if provider == "rules":
        return RuleBasedTriage()
    if provider == "llm":
        raise NotImplementedError("LLM triage provider is not implemented")
    return RuleBasedTriage()
