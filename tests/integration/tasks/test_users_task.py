import pytest
from unittest.mock import patch
from app.services.tasks.users import sync_users
from app.models.user import User

def fake_users_response():
    return [
        {"id": 1, "name": "Alice", "email": "alice@test.com"},
        {"id": 2, "name": "Bob", "email": "bob@test.com"},
    ]


@pytest.mark.parametrize("expected_count", [2])
def test_sync_users_task(session, expected_count):
    with patch("app.services.tasks.users.HttpClient") as mock_client_class:
        mock_client_instance = mock_client_class.return_value
        mock_client_instance.get.return_value = fake_users_response()

        with patch("app.services.tasks.users.SessionLocal", return_value=session):
            result = sync_users()

    assert result == expected_count

    users_in_db = session.query(User).all()
    assert len(users_in_db) == expected_count
    assert users_in_db[0].name == "Alice"
