from uuid import UUID

from psycopg import AsyncConnection
from psycopg.rows import dict_row

from scale_lab.domain.job import Job, JobStatus


class PostgresJobRepository:
    def __init__(self, conn: AsyncConnection) -> None:
        self._conn = conn

    async def add(self, job: Job) -> None:
        await self._conn.execute(
            """
            INSERT INTO jobs (
                job_id,
                run_id,
                file_id,
                status,
                received_at,
                input_object_key
                )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                job.job_id,
                job.run_id,
                job.file_id,
                job.status.value,
                job.received_at,
                job.input_object_key,
            ),
        )

    async def get_by_id(self, job_id: UUID) -> Job | None:
        async with self._conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT
                    job_id,
                    file_id,
                    received_at,
                    status,
                    run_id,
                    input_object_key
                FROM jobs
                WHERE job_id = %s
                """,
                (job_id,),
            )

            row = await cursor.fetchone()

        if row is None:
            return None

        return Job(
            job_id=row["job_id"],
            file_id=row["file_id"],
            received_at=row["received_at"],
            status=JobStatus(row["status"]),
            run_id=row["run_id"],
            input_object_key=row["input_object_key"],
        )

    async def save_uploaded(self, job_id: UUID, input_object_key: str) -> bool:
        cursor = await self._conn.execute(
            """
            UPDATE jobs
            SET input_object_key = %s, status = %s
            WHERE job_id = %s AND status = %s
            """,
            (
                input_object_key,
                JobStatus.PENDING.value,
                job_id,
                JobStatus.UPLOADING.value,
            ),
        )
        return cursor.rowcount == 1

    async def save_upload_failed(self, job_id: UUID) -> None:
        await self._conn.execute(
            """
            UPDATE jobs
            SET status = %s, error_code = 'upload_failed', finished_at = now()
            WHERE job_id = %s AND status = %s
            """,
            (JobStatus.FAILED.value, job_id, JobStatus.UPLOADING.value),
        )
