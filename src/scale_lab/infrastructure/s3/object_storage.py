from __future__ import annotations

import asyncio
from typing import IO, TYPE_CHECKING

from boto3.s3.transfer import TransferConfig

if TYPE_CHECKING:
    from types_boto3_s3.client import S3Client


class S3ObjectStorage:
    def __init__(self, client: S3Client, bucket: str) -> None:
        self._client = client
        self._bucket = bucket
        self._transfer_config = TransferConfig(
            multipart_threshold=8 * 1024 * 1024,
            multipart_chunksize=8 * 1024 * 1024,
            max_concurrency=4,
            use_threads=True,
        )

    async def put(
        self,
        *,
        key: str,
        source: IO[bytes],
        content_type: str,
    ) -> None:
        await asyncio.to_thread(
            self._client.upload_fileobj,
            source,
            self._bucket,
            key,
            ExtraArgs={"ContentType": content_type},
            Config=self._transfer_config,
        )

    async def get(
        self,
        *,
        key: str,
        destination: IO[bytes],
    ) -> None:
        await asyncio.to_thread(
            self._client.download_fileobj,
            self._bucket,
            key,
            destination,
            Config=self._transfer_config,
        )

    async def delete(self, *, key: str) -> None:
        await asyncio.to_thread(
            self._client.delete_object,
            Bucket=self._bucket,
            Key=key,
        )
