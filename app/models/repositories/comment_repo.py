from typing import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comment import Comment


class CommentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_external_id(self, external_id: int) -> Comment | None:
        stmt = select(Comment).where(Comment.external_id == external_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def exists(self, external_id: int) -> bool:
        stmt = select(Comment.id).where(Comment.external_id == external_id)
        return self.session.execute(stmt).first() is not None

    def bulk_create(self, comments: Iterable[Comment]) -> Sequence[Comment]:
        self.session.add_all(comments)
        self.session.commit()
        return comments

    def list_by_post_id(self, post_id: int) -> Sequence[Comment]:
        stmt = select(Comment).where(Comment.post_id == post_id)
        return self.session.execute(stmt).scalars().all()
