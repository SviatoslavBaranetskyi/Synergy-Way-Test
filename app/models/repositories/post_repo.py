from typing import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.post import Post


class PostRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_external_id(self, external_id: int) -> Post | None:
        stmt = select(Post).where(Post.external_id == external_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def exists(self, external_id: int) -> bool:
        stmt = select(Post.id).where(Post.external_id == external_id)
        return self.session.execute(stmt).first() is not None

    def bulk_create(self, posts: Iterable[Post]) -> Sequence[Post]:
        self.session.add_all(posts)
        self.session.commit()
        return posts

    def list_by_user_id(self, user_id: int) -> Sequence[Post]:
        stmt = select(Post).where(Post.user_id == user_id)
        return self.session.execute(stmt).scalars().all()
