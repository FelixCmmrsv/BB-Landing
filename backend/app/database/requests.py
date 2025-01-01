from datetime import datetime
from sqlalchemy import select, asc, update

from backend.app.database.models import NewUser, async_session


async def add_user(first_name: str, last_name: str, username: str, email: str, profile: str, description: str):
    async with async_session() as session:
        async with session.begin():
            new_user = NewUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile=profile,
                description=description,
                created_at=datetime.now()
            )
            session.add(new_user)


async def get_user_by_username(username: str):
    async with async_session() as session:
        async with session.begin():
            stmt = select(NewUser).where(NewUser.username == username)
            result = await session.execute(stmt)
            return result.scalar_one()


async def get_users_not_agreed():
    async with async_session() as session:
        async with session.begin():
            stmt = select(NewUser).where(NewUser.approved == False)
            result = await session.execute(stmt)
            return result.scalars().all()


async def get_users_agreed():
    async with async_session() as session:
        async with session.begin():
            stmt = select(NewUser).where(NewUser.approved == True)
            result = await session.execute(stmt)
            return result.scalars().all()


async def get_users():
    async with async_session() as session:
        async with session.begin():
            stmt = select(NewUser).order_by(asc(NewUser.created_at))
            result = await session.execute(stmt)
            return result.scalars().all()


async def approve_user(user_id: int):
    async with async_session() as session:
        async with session.begin():
            stmt = update(NewUser).where(NewUser.id == user_id).values(approved=True)
            await session.execute(stmt)


async def added_user(user_id: int):
    async with async_session() as session:
        async with session.begin():
            stmt = update(NewUser).where(NewUser.id == user_id).values(added=True)
            await session.execute(stmt)


async def get_user_by_id(user_id: int):
    async with async_session() as session:
        async with session.begin():
            stmt = select(NewUser).where(NewUser.id == user_id)
            result = await session.execute(stmt)
            return result.scalar_one()