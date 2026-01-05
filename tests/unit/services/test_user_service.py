from unittest.mock import MagicMock
from app.services.user_service import UserService
from app.models.user import User

def test_sync_users_creates_new_users(session):
    client = MagicMock()
    client.get.return_value = [
        {"id": 1, "name": "Alice", "email": "alice@test.com"},
        {"id": 2, "name": "Bob", "email": "bob@test.com"},
    ]

    service = UserService(session, client)
    new_users = service.sync_users()

    assert len(new_users) == 2
    assert session.query(User).count() == 2
    assert new_users[0].name == "Alice"

def test_sync_users_skips_existing(session):
    existing_user = User(external_id=1, name="Alice", email="alice@test.com")
    session.add(existing_user)
    session.commit()

    client = MagicMock()
    client.get.return_value = [
        {"id": 1, "name": "Alice", "email": "alice@test.com"},
        {"id": 2, "name": "Bob", "email": "bob@test.com"},
    ]

    service = UserService(session, client)
    new_users = service.sync_users()

    assert len(new_users) == 1
    assert session.query(User).count() == 2
