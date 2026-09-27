from datetime import datetime, timezone
from time import perf_counter
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from app.repositories.complaints import ComplaintRepository
from app.schemas import Complaint, ComplaintCreate, Status
from app.services.triage import TriageService

router = APIRouter(prefix="/api/complaints", tags=["complaints"])
repository = ComplaintRepository()
triage_service = TriageService()


@router.post("", response_model=Complaint, status_code=status.HTTP_201_CREATED)
async def create_complaint(payload: ComplaintCreate) -> Complaint:
    started = perf_counter()
    result, triaged_by = triage_service.triage(payload.text, payload.location)
    now = datetime.now(timezone.utc)
    complaint = Complaint(
        id=uuid4(),
        text=payload.text,
        location=payload.location,
        reporter_contact=payload.reporter_contact,
        category=result.category,
        priority=result.priority,
        status=Status.OPEN,
        ai_summary=result.summary,
        triaged_by=triaged_by,
        triage_latency_ms=round((perf_counter() - started) * 1000, 3),
        created_at=now,
        updated_at=now,
    )
    return await repository.create(complaint)


@router.get("/{id}", response_model=Complaint)
async def get_complaint(id: UUID) -> Complaint:
    complaint = await repository.get(id)
    if complaint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    return complaint
