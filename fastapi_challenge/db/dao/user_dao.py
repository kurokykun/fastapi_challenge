from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_challenge.db.dependencies import get_db_session
from fastapi_challenge.db.models.users import User


class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def get_all_users(self, limit: int, offset: int) -> List[User]:
        raw = await self.session.execute(select(User).limit(limit).offset(offset))
        return list(raw.scalars().fetchall())

    async def filter(self, email: Optional[str] = None, is_active: Optional[bool] = None) -> List[User]:
        query = select(User)
        if email:
            query = query.where(User.email == email)
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_by_id(self, id: UUID) -> Optional[User]:
        row = await self.session.execute(select(User).where(User.id == id))
        return row.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        row = await self.session.execute(select(User).where(User.email == email))
        return row.scalars().first()

    async def update_user(
        self,
        id: UUID,
        email: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[User]:
        row = await self.session.execute(select(User).where(User.id == id))
        user = row.scalars().first()
        if not user:
            return None
        if email is not None:
            user.email = email
        if is_active is not None:
            user.is_active = is_active
        await self.session.flush()
        return user

    async def delete_user(self, id: UUID) -> bool:
        row = await self.session.execute(select(User).where(User.id == id))
        user = row.scalars().first()
        if not user:
            return False
        if hasattr(user, "soft_delete"):
            user.soft_delete()
        else:
            setattr(user, "is_deleted", True)
        await self.session.flush()
        return True
