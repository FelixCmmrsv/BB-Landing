import os

from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import BigInteger, String, DateTime, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncAttrs

load_dotenv()
engine = create_async_engine(url=os.getenv("SQLALCHEMY_URL"))

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class NewUser(Base):
    __tablename__ = "new_users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    profile: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)