
from app.models.repositories.post_repo import PostRepository
from app.models.user import User
from app.models.post import Post

def test_post_repo_bulk_create_and_list(session):
    repo = PostRepository(session)

    user = User(external_id=1, name="Alice", email="alice@gmail.com")
    session.add(user)
    session.commit()

    posts = [
        Post(
            external_id=101,
            user_id=user.id,
            external_user_id=user.external_id,
            title="Post 1",
            body="Content 1",
        ),
        Post(
            external_id=102,
            user_id=user.id,
            external_user_id=user.external_id,
            title="Post 2",
            body="Content 2",
        ),
    ]
    created = repo.bulk_create(posts)

    assert len(created) == 2
    assert created[0].title == "Post 1"

    all_posts = repo.list_by_user_id(user.id)
    assert len(all_posts) == 2
    assert {p.title for p in all_posts} == {"Post 1", "Post 2"}

def test_post_repo_get_by_external_id_and_exists(session):
    repo = PostRepository(session)

    user = User(external_id=2, name="Bob", email="bob@gmail.com")
    session.add(user)
    session.commit()

    post = Post(
        external_id=201,
        user_id=user.id,
        external_user_id=user.external_id,
        title="Bob's post",
        body="Something",
    )
    session.add(post)
    session.commit()

    assert repo.exists(201) is True
    assert repo.exists(999) is False

    got = repo.get_by_external_id(201)
    assert got is not None
    assert got.title == "Bob's post"

    assert repo.get_by_external_id(999) is None
