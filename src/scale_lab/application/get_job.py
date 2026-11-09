from collections.abc import Callable
from uuid import UUID

from scale_lab.application.ports import UnitOfWork
from scale_lab.domain.job import Job


async def get_job(
    job_id: UUID,
    uow_factory: Callable[[], UnitOfWork],
) -> Job | None:
    async with uow_factory() as uow:
        return await uow.jobs.get_by_id(job_id)
