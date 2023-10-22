from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


from app.utils.logger import sqlalchemy_logger as logger
from config import initial_config as config


engine = create_async_engine(
    url=config.POSTGRESS_URL,
    future=True,
    # echo=True,
    pool_size=20,
    max_overflow=20,
)

AsyncSessionFactory: async_sessionmaker = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session
