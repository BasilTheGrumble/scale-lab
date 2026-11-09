from collections.abc import AsyncGenerator
from contextlib import AsyncExitStack, asynccontextmanager, closing

import boto3
from botocore.config import Config
from fastapi import FastAPI

from scale_lab.api.routers.jobs import router as jobs_router
from scale_lab.db import create_pool
from scale_lab.infrastructure.s3.object_storage import S3ObjectStorage
from scale_lab.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = Settings()

    async with AsyncExitStack() as stack:
        pool = await stack.enter_async_context(create_pool(settings))
        await pool.wait(timeout=10)

        session = boto3.session.Session()

        s3_client = stack.enter_context(
            closing(
                session.client(
                    "s3",
                    endpoint_url=settings.s3_endpoint_url,
                    region_name=settings.s3_region,
                    aws_access_key_id=settings.s3_access_key,
                    aws_secret_access_key=settings.s3_secret_key.get_secret_value(),
                    config=Config(
                        s3={"addressing_style": "path"},
                        max_pool_connections=16,
                    ),
                )
            )
        )

        app.state.db_pool = pool
        app.state.object_storage = S3ObjectStorage(
            client=s3_client,
            bucket=settings.s3_bucket,
        )

        yield


app = FastAPI(lifespan=lifespan)
app.include_router(jobs_router)
