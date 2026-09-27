from app.schemas import Category, Priority, TriageResult


class RuleBasedTriage:
    name = "rules"

    def triage(self, text: str, location: str) -> TriageResult:
        normalized = text.lower()
        category = Category.OTHER
        for keywords, candidate in (
            (("water", "leak", "pipe", "flood"), Category.WATER),
            (("electric", "power", "outage", "wire"), Category.ELECTRICITY),
            (("trash", "garbage", "sewer", "sanitation"), Category.SANITATION),
            (("road", "pothole", "street", "traffic"), Category.ROADS),
            (("light", "lamp", "dark"), Category.STREETLIGHTS),
        ):
            if any(keyword in normalized for keyword in keywords):
                category = candidate
                break

        priority = Priority.NORMAL
        if any(keyword in normalized for keyword in ("emergency", "danger", "urgent", "critical")):
            priority = Priority.HIGH
        elif any(keyword in normalized for keyword in ("minor", "small")):
            priority = Priority.LOW

        return TriageResult(
            category=category,
            priority=priority,
            summary=f"Reported {category.value} issue near {location[:100]}.",
            confidence=0.6,
        )
