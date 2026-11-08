CREATE TABLE jobs (
    job_id UUID PRIMARY KEY,
    run_id UUID,
    file_id TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN (
            'pending',
            'processing',
            'completed',
            'failed'
        )),

    received_at TIMESTAMPTZ NOT NULL,
    published_at TIMESTAMPTZ,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,

    input_duration_s DOUBLE PRECISION
        CHECK (input_duration_s > 0),

    input_size_bytes BIGINT
        CHECK (input_size_bytes > 0),

    attempt_count INTEGER NOT NULL DEFAULT 0
        CHECK (attempt_count >= 0),

    processing_cpu_s DOUBLE PRECISION
        CHECK (processing_cpu_s >= 0),

    processing_wall_s DOUBLE PRECISION
        CHECK (processing_wall_s >= 0),

    output_path TEXT,
    error_code TEXT,
    error_message TEXT
);
