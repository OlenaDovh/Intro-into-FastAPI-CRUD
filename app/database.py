from collections.abc import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Надає асинхронну сесію бази даних.

    Використовується як залежність у FastAPI для роботи з базою даних.

    Yields:
        Асинхронна сесія SQLAlchemy.
    """

    async with async_session() as session:
        yield session
