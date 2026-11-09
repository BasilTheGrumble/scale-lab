from types import TracebackType
from typing import IO, Protocol, Self
from uuid import UUID

from scale_lab.domain.job import Job


class JobRepository(Protocol):
    async def add(self, job: Job) -> None: ...

    async def get_by_id(self, job_id: UUID) -> Job | None: ...

    async def save_uploaded(self, job_id: UUID, input_object_key: str) -> bool: ...

    async def save_upload_failed(self, job_id: UUID) -> None: ...


class UnitOfWork(Protocol):
    jobs: JobRepository

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...


class ObjectStorage(Protocol):
    async def put(
        self,
        *,
        key: str,
        source: IO[bytes],
        content_type: str,
    ) -> None: ...

    async def get(
        self,
        *,
        key: str,
        destination: IO[bytes],
    ) -> None: ...

    async def delete(self, *, key: str) -> None: ...
