from typing import AsyncGenerator

import orjson
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.settings import settings


class Base(DeclarativeBase):
    pass


def orjson_serializer(obj) -> bytes:
    """
    Orjson serializer.

    :param obj: An object to be serialized.
    """
    return orjson.dumps(obj, option=orjson.OPT_NAIVE_UTC).decode()


engine = create_async_engine(
    settings.DATABASE_URL,
    json_serializer=orjson_serializer,
    json_deserializer=orjson.loads,
)
async_session_maker = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncGenerator, None]:
    async with async_session_maker() as session:
        yield session
