from app.models.repositories.user_repo import UserRepository
from app.models.user import User

def test_user_repo_bulk_create_and_list(session):
    repo = UserRepository(session)

    users = [
        User(external_id=1, name="Alice", email="alice@gmail.com"),
        User(external_id=2, name="Bob", email="bob@gmail.com")
    ]
    created = repo.bulk_create(users)

    assert len(created) == 2
    assert created[0].email == "alice@gmail.com"

    all_users = repo.list_all()
    assert len(all_users) == 2
    assert {u.name for u in all_users} == {"Alice", "Bob"}

def test_user_repo_get_by_external_id_and_exists(session):
    repo = UserRepository(session)
    user = User(external_id=10, name="Charlie", email="charlie@gmail.com")
    session.add(user)
    session.commit()

    assert repo.exists(10) is True
    assert repo.exists(999) is False

    got = repo.get_by_external_id(10)
    assert got is not None
    assert got.name == "Charlie"
    assert got.email == "charlie@gmail.com"

    assert repo.get_by_external_id(999) is None