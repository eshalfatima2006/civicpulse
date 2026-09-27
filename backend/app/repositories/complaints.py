from uuid import UUID

from app.schemas import Complaint


class ComplaintRepository:
    # TODO: replace with Postgres in Phase 2
    def __init__(self) -> None:
        self._complaints: dict[UUID, Complaint] = {}

    async def create(self, complaint: Complaint) -> Complaint:
        self._complaints[complaint.id] = complaint
        return complaint

    async def get(self, id: UUID) -> Complaint | None:
        return self._complaints.get(id)
