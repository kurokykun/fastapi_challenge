import uuid

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from fastapi_challenge.db.base import Base
from fastapi_challenge.db.models.mixins.time_stamp_mixin import TimeStampMixin
from fastapi_challenge.db.models.mixins.soft_delete_mixin import SoftDeleteMixin


class Post(TimeStampMixin, SoftDeleteMixin, Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    author = relationship("User", back_populates="posts")
    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
    )
