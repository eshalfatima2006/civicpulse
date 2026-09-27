from app.providers.triage.rules import RuleBasedTriage
from app.schemas import Category, Priority, TriageResult


class SimulatedTriage:
    name = "simulated"

    def __init__(self, *, should_fail: bool = False, malformed_result: bool = False) -> None:
        self._should_fail = should_fail
        self._malformed_result = malformed_result

    @classmethod
    def failing(cls) -> "SimulatedTriage":
        return cls(should_fail=True)

    @classmethod
    def malformed(cls) -> "SimulatedTriage":
        return cls(malformed_result=True)

    def triage(self, text: str, location: str) -> TriageResult:
        if self._should_fail:
            raise RuntimeError("simulated provider failure")
        if self._malformed_result:
            return TriageResult.model_construct(
                category=Category.OTHER,
                priority=Priority.NORMAL,
                summary="x" * 200,
                confidence=0.9,
            )

        result = RuleBasedTriage().triage(text, location)
        return TriageResult(
            category=result.category,
            priority=result.priority,
            summary=f"Simulated {result.category.value} report at {location[:100]}.",
            confidence=0.9,
        )
