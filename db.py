from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import settings

sqlalchemy_database_uri = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    port=settings.DB_PORT,
    host=settings.DB_HOST,
    path=f"/{settings.DB_NAME or ''}",
)

engine = create_async_engine(sqlalchemy_database_uri,
                             pool_size=settings.POOL_SIZE,
                             max_overflow=settings.MAX_OVERFLOW,
                             pool_recycle=settings.POOL_RECYCLE,
                             pool_timeout=settings.POOL_TIMEOUT,
                             pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
