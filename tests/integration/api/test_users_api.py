import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import User


@pytest.mark.integration
def test_list_users():
    with patch("app.main.init_db_with_retry"):
        with patch("app.api.routers.users.SessionLocal") as mock_session_class:
            mock_session = MagicMock()
            mock_session_class.return_value = mock_session

            now = datetime.utcnow()
            user1 = User(id=1, external_id=1, name="User1", email="u1@example.com")
            user1.created_at = now
            user2 = User(id=2, external_id=2, name="User2", email="u2@example.com")
            user2.created_at = now

            mock_session.execute.return_value.scalars.return_value.all.side_effect = [
                [user1, user2],
                [user1, user2],
            ]

            client = TestClient(app)
            response = client.get("/users/")
            data = response.json()

            assert response.status_code == 200
            assert data["count"] == 2
            assert data["total"] == 2
            assert data["items"][0]["name"] == "User1"
            assert data["items"][1]["name"] == "User2"


@pytest.mark.integration
def test_run_users_sync():
    with patch("app.main.init_db_with_retry"):
        with patch("app.api.routers.users.sync_users") as mock_task:
            mock_task.delay.return_value = MagicMock(id="fake_task_id")

            client = TestClient(app)
            response = client.post("/users/sync")
            data = response.json()

            assert response.status_code == 200
            assert data["task_id"] == "fake_task_id"


@pytest.mark.integration
def test_get_sync_status():
    with patch("app.main.init_db_with_retry"):
        task_id = "fake_task_id"

        with patch("app.api.routers.users.AsyncResult") as mock_async:
            mock_instance = mock_async.return_value
            mock_instance.state = "SUCCESS"
            mock_instance.result = 5

            client = TestClient(app)
            response = client.get(f"/users/sync/{task_id}")
            data = response.json()

            assert response.status_code == 200
            assert data["task_id"] == task_id
            assert data["state"] == "SUCCESS"
            assert data["result"] == 5
