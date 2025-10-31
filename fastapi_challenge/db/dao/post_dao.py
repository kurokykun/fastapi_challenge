from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_challenge.db.dependencies import get_db_session
from fastapi_challenge.db.models.post import Post


class PostDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_post(self, title: str, content: str, author_id: UUID) -> None:
        self.session.add(Post(title=title, content=content, author_id=author_id))

    async def get_all_posts(self, limit: int, offset: int) -> List[Post]:
        raw = await self.session.execute(select(Post).limit(limit).offset(offset))
        return list(raw.scalars().fetchall())

    async def filter(self, title: Optional[str] = None, author_id: Optional[UUID] = None) -> List[Post]:
        query = select(Post)
        if title:
            query = query.where(Post.title == title)
        if author_id:
            query = query.where(Post.author_id == author_id)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_by_id(self, id: UUID) -> Optional[Post]:
        row = await self.session.execute(select(Post).where(Post.id == id))
        return row.scalars().first()

    async def update_post(
        self,
        id: UUID,
        title: Optional[str] = None,
        content: Optional[str] = None,
    ) -> Optional[Post]:
        row = await self.session.execute(select(Post).where(Post.id == id))
        post = row.scalars().first()
        if not post:
            return None
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        await self.session.flush()
        return post

    async def delete_post(self, id: UUID) -> bool:
        row = await self.session.execute(select(Post).where(Post.id == id))
        post = row.scalars().first()
        if not post:
            return False
        if hasattr(post, "soft_delete"):
            post.soft_delete()
        else:
            setattr(post, "is_deleted", True)
        await self.session.flush()
        return True
