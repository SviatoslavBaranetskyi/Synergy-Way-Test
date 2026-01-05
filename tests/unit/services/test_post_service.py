from unittest.mock import MagicMock
from app.services.post_service import PostService
from app.models.user import User
from app.models.post import Post

def test_sync_posts_creates_posts_with_user(session):
    user = User(external_id=1, name="Alice", email="alice@test.com")
    session.add(user)
    session.commit()

    client = MagicMock()
    client.get.return_value = {
        "posts": [
            {"id": 1, "userId": 1, "title": "Post 1", "body": "Body 1"},
            {"id": 2, "userId": 1, "title": "Post 2", "body": "Body 2"},
        ]
    }

    service = PostService(session, client)
    posts = service.sync_posts()

    assert len(posts) == 2
    assert session.query(Post).count() == 2
    assert posts[0].title == "Post 1"

def test_sync_posts_skips_existing(session):
    user = User(external_id=1, name="Alice", email="alice@test.com")
    session.add(user)
    session.commit()

    from app.models.post import Post
    existing_post = Post(external_id=1, title="Old", body="Old", external_user_id=1, user_id=user.id)
    session.add(existing_post)
    session.commit()

    client = MagicMock()
    client.get.return_value = {
        "posts": [
            {"id": 1, "userId": 1, "title": "Post 1", "body": "Body 1"},
            {"id": 2, "userId": 1, "title": "Post 2", "body": "Body 2"},
        ]
    }

    service = PostService(session, client)
    posts = service.sync_posts()

    assert len(posts) == 1
    assert session.query(Post).count() == 2
