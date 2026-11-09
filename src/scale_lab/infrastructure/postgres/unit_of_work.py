from types import TracebackType
from typing import Self

from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

from scale_lab.application.ports import JobRepository
from scale_lab.infrastructure.postgres.job_repository import PostgresJobRepository


class PostgresUnitOfWork:
    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool
        self._conn: AsyncConnection | None = None
        self._committed = False
        self.jobs: JobRepository

    async def __aenter__(self) -> Self:
        if self._conn is not None:
            raise RuntimeError("Unit of Work is already active")

        conn = await self._pool.getconn()

        self._conn = conn
        self._committed = False
        self.jobs = PostgresJobRepository(conn)

        return self

    async def commit(self) -> None:
        if self._conn is None:
            raise RuntimeError("Unit of Work is not active")

        if self._committed:
            raise RuntimeError("Unit of Work is already committed")

        await self._conn.commit()
        self._committed = True

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._conn is None:
            raise RuntimeError("Unit of Work is not active")

        conn = self._conn
        self._conn = None

        try:
            await conn.rollback()
        finally:
            await self._pool.putconn(conn)
