from psycopg_pool import AsyncConnectionPool

from scale_lab.settings import Settings


def create_pool(settings: Settings) -> AsyncConnectionPool:
    return AsyncConnectionPool(
        kwargs={
            "host": settings.postgres_host,
            "port": settings.postgres_port,
            "dbname": settings.postgres_db,
            "user": settings.postgres_user,
            "password": settings.postgres_password.get_secret_value(),
        },
        min_size=1,
        max_size=4,
        open=False,
    )
