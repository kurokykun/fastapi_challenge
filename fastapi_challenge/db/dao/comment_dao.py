from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_challenge.db.dependencies import get_db_session
from fastapi_challenge.db.models.comment import Comment


class CommentDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_comment(self, content: str, post_id: UUID, author_id: Optional[UUID] = None) -> None:
        self.session.add(Comment(content=content, post_id=post_id, author_id=author_id))

    async def get_all_comments(self, limit: int, offset: int) -> List[Comment]:
        query = await self.session.execute(
            select(Comment).where(Comment.is_deleted.is_(False)).limit(limit).offset(offset)
        )
        return list(query.scalars().fetchall())

    async def filter(self, post_id: Optional[UUID] = None, author_id: Optional[UUID] = None) -> List[Comment]:
        query = select(Comment).where(Comment.is_deleted.is_(False))
        if post_id:
            query = query.where(Comment.post_id == post_id)
        if author_id:
            query = query.where(Comment.author_id == author_id)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_by_id(self, id: UUID) -> Optional[Comment]:
        row = await self.session.execute(select(Comment).where(Comment.id == id))
        return row.scalars().first()

    async def update_comment(self, id: UUID, content: Optional[str] = None) -> Optional[Comment]:
        row = await self.session.execute(select(Comment).where(Comment.id == id))
        comment = row.scalars().first()
        if not comment:
            return None
        if content is not None:
            comment.content = content
        await self.session.flush()
        return comment

    async def delete_comment(self, id: UUID) -> bool:
        row = await self.session.execute(select(Comment).where(Comment.id == id))
        comment = row.scalars().first()
        if not comment:
            return False
        if hasattr(comment, "soft_delete"):
            comment.soft_delete()
        else:
            setattr(comment, "is_deleted", True)
        await self.session.flush()
        return True
