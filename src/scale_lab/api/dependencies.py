from collections.abc import Callable

from fastapi import Request
from psycopg_pool import AsyncConnectionPool

from scale_lab.application.ports import ObjectStorage, UnitOfWork
from scale_lab.infrastructure.postgres.unit_of_work import PostgresUnitOfWork


async def get_object_storage(request: Request) -> ObjectStorage:
    storage: ObjectStorage = request.app.state.object_storage
    return storage


async def get_uow_factory(request: Request) -> Callable[[], UnitOfWork]:
    pool: AsyncConnectionPool = request.app.state.db_pool
    return lambda: PostgresUnitOfWork(pool)
