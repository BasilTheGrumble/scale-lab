from collections.abc import Callable
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from scale_lab.api.dependencies import get_object_storage, get_uow_factory
from scale_lab.api.schemas import JobResponse
from scale_lab.application.create_job import create_job_from_upload
from scale_lab.application.get_job import get_job
from scale_lab.application.ports import ObjectStorage, UnitOfWork

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobResponse)
async def read_job(
    job_id: UUID,
    uow_factory: Annotated[
        Callable[[], UnitOfWork],
        Depends(get_uow_factory),
    ],
) -> JobResponse:
    job = await get_job(job_id, uow_factory)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return JobResponse(
        job_id=job.job_id,
        run_id=job.run_id,
        file_id=job.file_id,
        status=job.status,
        received_at=job.received_at,
    )


@router.post("", response_model=JobResponse, status_code=201)
async def post_job(
    file: Annotated[UploadFile, File()],
    file_id: Annotated[str, Form(min_length=1, pattern=r"\S")],
    uow_factory: Annotated[Callable[[], UnitOfWork], Depends(get_uow_factory)],
    object_storage: Annotated[ObjectStorage, Depends(get_object_storage)],
    run_id: Annotated[UUID | None, Form()] = None,
) -> JobResponse:
    job = await create_job_from_upload(
        file_id=file_id,
        source=file.file,
        uow_factory=uow_factory,
        object_storage=object_storage,
        run_id=run_id,
    )
    return JobResponse.model_validate(job, from_attributes=True)
