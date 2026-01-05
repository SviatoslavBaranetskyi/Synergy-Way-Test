import pytest
from unittest.mock import patch

from app.models.comment import Comment
from app.models.post import Post
from app.services.tasks.comments import sync_comments

def fake_comments_response():
    return {
        "comments": [
            {"id": 1, "postId": 1, "body": "Comment 1", "user": {"id": 1}},
            {"id": 2, "postId": 1, "body": "Comment 2", "user": {"id": 2}},
        ]
    }

@pytest.mark.integration
def test_sync_comments_task(session):
    post = Post(
        id=1,
        external_id=1,
        title="Dummy Post",
        body="Some body",
        external_user_id=1,
        user_id=None,
    )
    session.add(post)
    session.commit()

    with patch("app.services.tasks.comments.HttpClient") as mock_client_class:
        mock_client_instance = mock_client_class.return_value
        mock_client_instance.get.return_value = fake_comments_response()

        with patch("app.services.tasks.comments.SessionLocal", return_value=session):
            result = sync_comments(limit=2, skip=0)

    assert result == 2

    comments_in_db = session.query(Comment).all()
    assert len(comments_in_db) == 2
    assert comments_in_db[0].body == "Comment 1"
    assert comments_in_db[1].body == "Comment 2"
