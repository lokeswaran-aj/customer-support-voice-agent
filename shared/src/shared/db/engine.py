from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import AsyncSession, sessionmaker

from shared.core.settings import settings

async_engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
