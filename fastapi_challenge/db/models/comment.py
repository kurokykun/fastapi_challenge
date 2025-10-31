import uuid

from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from fastapi_challenge.db.base import Base
from fastapi_challenge.db.models.mixins.time_stamp_mixin import TimeStampMixin
from fastapi_challenge.db.models.mixins.soft_delete_mixin import SoftDeleteMixin


class Comment(TimeStampMixin, SoftDeleteMixin, Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    post_id = Column(
        UUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
    )

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
