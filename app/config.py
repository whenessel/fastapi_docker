import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DIR = Path(__file__).parent.parent / "app"


class Settings(BaseSettings):
    PROJECT_DIR: os.PathLike[str] = Path(__file__).parent.parent
    ENVIRONMENT: Literal["DEV", "PYTEST", "STG", "PRD"] = os.getenv("APP_ENV")
    OPEN_API: str = os.getenv("APP_OPEN_API", "")
    base_app_url: str = os.getenv("APP_HOST", "https://frontend-host.com")

    s3_region: str = os.getenv("AWS_DEFAULT_REGION")
    s3_access_key: str = os.getenv("AWS_S3_ACCESS_KEY_ID")
    s3_secret_access_key: str = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
    s3_bucket_name: str = os.getenv("AWS_S3_BUCKET")
    s3_bucket_region: str = os.getenv("AWS_S3_DEFAULT_REGION")

    sentry_dsn: str = os.getenv("SENTRY_DSN")

    email_labs_app_key: str = os.getenv("EMAIL_LABS_APP_KEY")
    email_labs_secret_key: str = os.getenv("EMAIL_LABS_APP_KEY")
    email_smtp: str = os.getenv("EMAIL_LABS_SMTP")
    email_sender: str = os.getenv("EMAIL_LABS_SENDER")
    email_dev: str = os.getenv("EMAIL_DEV")

    email_mailjet_app_key: str = os.getenv("MAILJET_EMAIL_API_KEY")
    email_mailjet_secret_key: str = os.getenv("MAILJET_EMAIL_SECRET")
    email_mailjet_sender: str = os.getenv("MAILJET_EMAIL_SENDER")
    sms_mailjet_api_key: str = os.getenv("MAILJET_SMS_API_KEY")
    sms_mailjet_sender: str = os.getenv("MAILJET_SMS_SENDER")

    # API
    REJESTR_IO_KEY: str = os.getenv("REJESTR_IO_KEY")
    GUS_KEY: str = os.getenv("GUS_API")
    GUS_API_DEV: str = os.getenv("GUS_API_DEV")
    API_VIDEO: str = os.getenv("API_VIDEO")
    API_VIDEO_UPLOAD: str = os.getenv("API_VIDEO_UPLOAD")

    # POSTGRESQL DEFAULT DATABASE
    DEFAULT_DATABASE_HOSTNAME: str = os.getenv("DB_HOST")
    DEFAULT_DATABASE_PORT: str = os.getenv("DB_PORT")
    DEFAULT_DATABASE_DB: str = os.getenv("DB_DATABASE")
    DEFAULT_DATABASE_USER: str = os.getenv("DB_USERNAME")
    DEFAULT_DATABASE_PASSWORD: str = os.getenv("DB_PASSWORD")

    # DEFAULT_SQLALCHEMY_DATABASE_URI: str = os.getenv("DEFAULT_SQLALCHEMY_DATABASE_URI")

    # POSTGRESQL TEST DATABASE
    TEST_DATABASE_HOSTNAME: str = "postgres"
    TEST_DATABASE_USER: str = "postgres"
    TEST_DATABASE_PASSWORD: str = "postgres"
    TEST_DATABASE_PORT: str = "5432"
    TEST_DATABASE_DB: str = "postgres"
    # TEST_SQLALCHEMY_DATABASE_URI: str = ""
    # TEST_SQLALCHEMY_DATABASE_URI: str = os.getenv("TEST_SQLALCHEMY_DATABASE_URI")

    model_config = SettingsConfigDict(
        env_prefix="", env_file_encoding="utf-8", env_file=f"{APP_DIR}/.env", extra="allow"
    )


@lru_cache
def get_settings() -> BaseSettings:
    # path = Path(__file__).parent.parent / "app" / ".env.testing"
    # return Settings(_env_file=path.as_posix(), _env_file_encoding="utf-8")
    return Settings()
