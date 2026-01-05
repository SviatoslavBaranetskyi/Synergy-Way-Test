from unittest.mock import patch
from app.services.tasks.posts import sync_posts
from app.models.post import Post

def fake_posts_response():
    return [
        {"id": 1, "title": "Post 1", "body": "Body 1", "userId": 1},
        {"id": 2, "title": "Post 2", "body": "Body 2", "userId": 1},
    ]

def test_sync_posts_task(session):
    with patch("app.services.tasks.posts.HttpClient") as mock_client_class:
        mock_client_instance = mock_client_class.return_value
        mock_client_instance.get.return_value = {"posts": fake_posts_response()}

        with patch("app.services.tasks.posts.SessionLocal", return_value=session):
            result = sync_posts(limit=2, skip=0)

    assert result == 2
    posts_in_db = session.query(Post).all()
    assert len(posts_in_db) == 2
    assert posts_in_db[0].title == "Post 1"
