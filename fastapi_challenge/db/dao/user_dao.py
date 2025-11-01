from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_challenge.db.dependencies import get_db_session
from fastapi_challenge.db.models.users import User
from fastapi_users.password import PasswordHelper


class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session
        self._password_helper = PasswordHelper()

    async def get_all_users(self, limit: int, offset: int) -> List[User]:
        query = select(User)
        is_deleted_col = getattr(User, "is_deleted", None)
        if is_deleted_col is not None:
            query = query.where(is_deleted_col.is_(False))
        raw = await self.session.execute(query.limit(limit).offset(offset))
        return list(raw.scalars().fetchall())

    async def filter(self, email: Optional[str] = None, is_active: Optional[bool] = None) -> List[User]:
        query = select(User)
        is_deleted_col = getattr(User, "is_deleted", None)
        if is_deleted_col is not None:
            query = query.where(is_deleted_col.is_(False))
        if email:
            query = query.where(User.email == email.lower())
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_by_id(self, id: UUID) -> Optional[User]:
        row = await self.session.execute(select(User).where(User.id == id))
        return row.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        row = await self.session.execute(select(User).where(User.email == email.lower()))
        return row.scalars().first()

    async def create_user(
        self,
        email: str,
        password: str,
        *,
        is_active: bool = True,
        is_superuser: bool = False,
        is_verified: bool = False,
    ) -> User:
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        normalized_email = email.lower()
        hashed_password = self._password_helper.hash(password)
        user = User(
            email=normalized_email,
            hashed_password=hashed_password,
            is_active=is_active,
            is_superuser=is_superuser,
            is_verified=is_verified,
        )
        self.session.add(user)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            raise ValueError("Email already registered") from exc
        await self.session.refresh(user)
        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        if not email or not password:
            return None
        row = await self.session.execute(select(User).where(User.email == email.lower()))
        user = row.scalars().first()
        if not user or not getattr(user, "is_active", False):
            return None
        if getattr(user, "is_deleted", False):
            return None
        verified, updated_hash = self._password_helper.verify_and_update(
            password,
            user.hashed_password,
        )
        if not verified:
            return None
        if updated_hash:
            user.hashed_password = updated_hash
            await self.session.flush()
        return user

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
            user.email = email.lower()
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
