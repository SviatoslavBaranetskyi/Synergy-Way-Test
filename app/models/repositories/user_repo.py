from typing import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_external_id(self, external_id: int) -> User | None:
        stmt = select(User).where(User.external_id == external_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def exists(self, external_id: int) -> bool:
        stmt = select(User.id).where(User.external_id == external_id)
        return self.session.execute(stmt).first() is not None

    def bulk_create(self, users: Iterable[User]) -> Sequence[User]:
        self.session.add_all(users)
        self.session.commit()
        return users

    def list_all(self) -> Sequence[User]:
        stmt = select(User)
        return self.session.execute(stmt).scalars().all()
