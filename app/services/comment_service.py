from typing import List

from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.models.repositories.comment_repo import CommentRepository
from app.models.repositories.post_repo import PostRepository
from app.models.repositories.user_repo import UserRepository
from app.services.http_client import HttpClient


class CommentService:
    def __init__(self, session: Session, client: HttpClient) -> None:
        self.comment_repo = CommentRepository(session)
        self.post_repo = PostRepository(session)
        self.user_repo = UserRepository(session)
        self.client = client

    def sync_comments(self, limit: int = 20, skip: int = 0) -> List[Comment]:
        response = self.client.get(
            "/comments",
            params={"limit": limit, "skip": skip},
        )

        comments_data = response.get("comments", [])

        new_comments: list[Comment] = []

        for item in comments_data:
            external_id = item["id"]

            if self.comment_repo.exists(external_id):
                continue

            post = self.post_repo.get_by_external_id(item["postId"])
            if not post:
                continue
            
            user = self.user_repo.get_by_external_id(item["user"]["id"])

            comment = Comment(
                external_id=external_id,
                body=item["body"],
                post_id=post.id,
                user_id=user.id if user else None,
            )
            new_comments.append(comment)

        if new_comments:
            self.comment_repo.bulk_create(new_comments)

        return new_comments
