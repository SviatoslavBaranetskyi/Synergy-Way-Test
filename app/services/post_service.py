from typing import List

from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.repositories.post_repo import PostRepository
from app.models.repositories.user_repo import UserRepository
from app.services.http_client import HttpClient


class PostService:
    def __init__(self, session: Session, client: HttpClient) -> None:
        self.post_repo = PostRepository(session)
        self.user_repo = UserRepository(session)
        self.client = client

    def sync_posts(self, limit: int = 10, skip: int = 0) -> List[Post]:
        response = self.client.get(
            "/posts",
            params={"limit": limit, "skip": skip},
        )

        posts_data = response.get("posts", [])

        new_posts: list[Post] = []

        for item in posts_data:
            external_id = item["id"]

            if self.post_repo.exists(external_id):
                continue

            external_user_id = item["userId"]
            user = self.user_repo.get_by_external_id(external_user_id)

            post = Post(
                external_id=external_id,
                title=item["title"],
                body=item["body"],
                external_user_id=external_user_id,
                user_id=user.id if user else None,
            )
            new_posts.append(post)

        if new_posts:
            self.post_repo.bulk_create(new_posts)

        return new_posts
