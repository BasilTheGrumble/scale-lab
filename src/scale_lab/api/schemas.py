from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from scale_lab.domain.job import JobStatus


class JobResponse(BaseModel):
    job_id: UUID
    run_id: UUID | None
    file_id: str
    status: JobStatus
    received_at: datetime


class CreateJobRequest(BaseModel):
    file_id: str = Field(min_length=1, pattern=r"\S")
    run_id: UUID | None = None
