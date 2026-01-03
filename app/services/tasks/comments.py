from celery import shared_task

from app.core.db.session import SessionLocal
from app.services.http_client import HttpClient
from app.services.comment_service import CommentService


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def sync_comments(self, limit: int = 20, skip: int = 0) -> int:
    session = SessionLocal()
    try:
        client = HttpClient(base_url="https://dummyjson.com")
        service = CommentService(session=session, client=client)

        comments = service.sync_comments(limit=limit, skip=skip)
        return len(comments)

    finally:
        session.close()
