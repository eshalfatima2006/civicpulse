import logging

from app.providers.triage.base import TriageProvider
from app.providers.triage.factory import get_provider
from app.providers.triage.rules import RuleBasedTriage
from app.schemas import TriageResult

logger = logging.getLogger(__name__)


class TriageService:
    def __init__(self, provider: TriageProvider | None = None) -> None:
        self.provider = provider or get_provider()

    def triage(self, text: str, location: str) -> tuple[TriageResult, str]:
        try:
            result = self.provider.triage(text, location)
            result = TriageResult.model_validate(result.model_dump())
            return result, self.provider.name
        except Exception as error:
            logger.warning("Triage provider failed: %s", error.__class__.__name__)
            result = RuleBasedTriage().triage(text, location)
            return result, "rules:fallback"
