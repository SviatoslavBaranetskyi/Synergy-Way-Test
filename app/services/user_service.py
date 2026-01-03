from typing import List

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.repositories.user_repo import UserRepository
from app.services.http_client import HttpClient


class UserService:
    def __init__(self, session: Session, client: HttpClient) -> None:
        self.repo = UserRepository(session)
        self.client = client

    def sync_users(self) -> list[User]:
        data = self.client.get("/users")

        new_users: list[User] = []

        for item in data:
            external_id = item["id"]

            if self.repo.exists(external_id):
                continue

            user = User(
                external_id=external_id,
                name=item["name"],
                email=item["email"],
            )
            new_users.append(user)

        if new_users:
            self.repo.bulk_create(new_users)

        return new_users