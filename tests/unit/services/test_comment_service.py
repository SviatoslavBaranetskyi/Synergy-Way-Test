from unittest.mock import MagicMock
from app.services.comment_service import CommentService
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment

def test_sync_comments_creates_comments(session):
    user = User(external_id=1, name="Alice", email="alice@test.com")
    session.add(user)
    session.commit()

    post = Post(external_id=10, title="Post", body="Body", external_user_id=1, user_id=user.id)
    session.add(post)
    session.commit()

    client = MagicMock()
    client.get.return_value = {
        "comments": [
            {"id": 1, "postId": 10, "body": "Comment 1", "user": {"id": 1}},
            {"id": 2, "postId": 10, "body": "Comment 2", "user": {"id": 1}},
        ]
    }

    service = CommentService(session, client)
    comments = service.sync_comments()

    assert len(comments) == 2
    assert session.query(Comment).count() == 2
    assert comments[0].body == "Comment 1"

def test_sync_comments_skips_missing_post(session):
    client = MagicMock()
    client.get.return_value = {
        "comments": [
            {"id": 1, "postId": 999, "body": "Comment 1", "user": {"id": 1}}
        ]
    }

    service = CommentService(session, client)
    comments = service.sync_comments()

    assert len(comments) == 0
