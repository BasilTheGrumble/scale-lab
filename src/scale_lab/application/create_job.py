from collections.abc import Callable
from typing import IO
from uuid import UUID

from scale_lab.application.ports import ObjectStorage, UnitOfWork
from scale_lab.domain.job import Job


async def create_job(
    file_id: str,
    uow_factory: Callable[[], UnitOfWork],
    run_id: UUID | None = None,
) -> Job:
    job = Job.create(file_id=file_id, run_id=run_id)

    async with uow_factory() as uow:
        await uow.jobs.add(job)
        await uow.commit()

    return job


async def create_job_from_upload(
    file_id: str,
    source: IO[bytes],
    uow_factory: Callable[[], UnitOfWork],
    object_storage: ObjectStorage,
    run_id: UUID | None = None,
) -> Job:
    job = Job.create_for_upload(file_id=file_id, run_id=run_id)
    object_key = f"inputs/{job.job_id}.wav"

    async with uow_factory() as uow:
        await uow.jobs.add(job)
        await uow.commit()

    try:
        await object_storage.put(
            key=object_key,
            source=source,
            content_type="audio/wav",
        )
    except Exception:
        async with uow_factory() as uow:
            await uow.jobs.save_upload_failed(job.job_id)
            await uow.commit()
        raise

    job.input_object_key = object_key
    job.mark_uploaded()

    async with uow_factory() as uow:
        saved = await uow.jobs.save_uploaded(job.job_id, object_key)
        if not saved:
            raise RuntimeError(f"Could not finalize upload for job {job.job_id}")

        await uow.commit()

    return job
