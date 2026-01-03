from celery import shared_task

from app.core.db.session import SessionLocal
from app.services.http_client import HttpClient
from app.services.post_service import PostService


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def sync_posts(self, limit: int = 10, skip: int = 0) -> int:
    session = SessionLocal()
    try:
        client = HttpClient(base_url="https://dummyjson.com")
        service = PostService(session=session, client=client)

        posts = service.sync_posts(limit=limit, skip=skip)
        return len(posts)

    finally:
        session.close()
