from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "scale_lab"
    postgres_user: str = "scale_lab"
    postgres_password: SecretStr

    s3_endpoint_url: str = "http://rustfs:9000"
    s3_bucket: str = "scale-lab"
    s3_region: str = "us-east-1"
    s3_access_key: str
    s3_secret_key: SecretStr
