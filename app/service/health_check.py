from loguru import logger

from app.config import get_settings
from app.db import engine
from app.service.aws_s3 import s3_client

settings = get_settings()


async def test_db():
    try:
        with engine.connect():
            return {"db": "healthy"}
    except Exception as err:
        logger.exception(err)
        raise err


async def test_storage():
    try:
        response = s3_client.head_bucket(Bucket=settings.s3_bucket_name)
        # print("@@@@@@@@@@@@@", response)
    except Exception as err:
        logger.exception(err)  # , exc_info=True
        raise err

    return {"storage": "healthy"}


async def run_healthcheck() -> dict[str, str]:
    await test_db()
    await test_storage()
    return {"status": "ALIVE"}
