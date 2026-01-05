from app.models.repositories.comment_repo import CommentRepository
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment

def test_comment_repo_bulk_create_and_list(session):
    repo = CommentRepository(session)

    user = User(external_id=1, name="Alice", email="alice@gmail.com")
    session.add(user)
    session.commit()

    post = Post(
        external_id=101,
        user_id=user.id,
        external_user_id=user.external_id,
        title="Post 1",
        body="Content 1"
    )
    session.add(post)
    session.commit()

    comments = [
        Comment(
            external_id=1001,
            post_id=post.id,
            user_id=user.id,
            body="Comment 1"
        ),
        Comment(
            external_id=1002,
            post_id=post.id,
            user_id=user.id,
            body="Comment 2"
        ),
    ]
    created = repo.bulk_create(comments)

    assert len(created) == 2
    assert created[0].body == "Comment 1"

    all_comments = repo.list_by_post_id(post.id)
    assert len(all_comments) == 2
    assert {c.body for c in all_comments} == {"Comment 1", "Comment 2"}

def test_comment_repo_get_by_external_id_and_exists(session):
    repo = CommentRepository(session)

    user = User(external_id=2, name="Bob", email="bob@gmail.com")
    session.add(user)
    session.commit()

    post = Post(
        external_id=201,
        user_id=user.id,
        external_user_id=user.external_id,
        title="Bob's Post",
        body="Post content"
    )
    session.add(post)
    session.commit()

    comment = Comment(
        external_id=2001,
        post_id=post.id,
        user_id=user.id,
        body="Bob's comment"
    )
    session.add(comment)
    session.commit()

    assert repo.exists(2001) is True
    assert repo.exists(9999) is False

    got = repo.get_by_external_id(2001)
    assert got is not None
    assert got.body == "Bob's comment"

    assert repo.get_by_external_id(9999) is None