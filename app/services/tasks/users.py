from celery import shared_task

from app.core.db.session import SessionLocal
from app.services.http_client import HttpClient
from app.services.user_service import UserService


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def sync_users(self) -> int:
    session = SessionLocal()
    try:
        client = HttpClient(base_url="https://jsonplaceholder.typicode.com")
        service = UserService(session=session, client=client)

        users = service.sync_users()
        return len(users)

    finally:
        session.close()
