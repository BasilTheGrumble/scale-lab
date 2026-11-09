from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4


class JobStatus(StrEnum):
    UPLOADING = "uploading"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class Job:
    job_id: UUID
    file_id: str
    received_at: datetime
    status: JobStatus = JobStatus.PENDING
    run_id: UUID | None = None
    input_object_key: str | None = None

    @classmethod
    def create(
        cls,
        file_id: str,
        run_id: UUID | None = None,
        *,
        job_id: UUID | None = None,
    ) -> Self:
        if not file_id.strip():
            raise ValueError("file_id must not be empty")

        return cls(
            job_id=uuid4() if job_id is None else job_id,
            file_id=file_id,
            received_at=datetime.now(UTC),
            run_id=run_id,
        )

    @classmethod
    def create_for_upload(cls, file_id: str, run_id: UUID | None = None) -> Self:
        job = cls.create(file_id=file_id, run_id=run_id)
        job.status = JobStatus.UPLOADING
        return job

    def mark_uploaded(self) -> None:
        if self.status != JobStatus.UPLOADING:
            raise ValueError(f"Cannot complete upload from status {self.status}")

        if not self.input_object_key:
            raise ValueError("Input object key is required")

        self.status = JobStatus.PENDING
