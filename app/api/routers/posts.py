from fastapi import APIRouter, Query
from celery.result import AsyncResult
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db.session import SessionLocal
from app.models.post import Post
from app.services.tasks.posts import sync_posts
from app.core.celery_app import celery

router = APIRouter()


@router.get("/")
def list_posts(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    session: Session = SessionLocal()
    try:
        items = session.execute(
            select(Post).offset(offset).limit(limit)
        ).scalars().all()

        total = session.execute(select(Post)).scalars().all()

        return {
            "items": [
                {
                    "id": p.id,
                    "external_id": p.external_id,
                    "title": p.title,
                    "user_id": p.user_id,
                }
                for p in items
            ],
            "count": len(items),
            "total": len(total),
            "offset": offset,
            "limit": limit,
        }
    finally:
        session.close()


@router.post("/sync")
def run_posts_sync(limit: int = 10, skip: int = 0):
    task = sync_posts.delay(limit, skip)
    return {"task_id": task.id}


@router.get("/sync/{task_id}")
def get_sync_status(task_id: str):
    result = AsyncResult(task_id, app=celery)
    return {
        "task_id": task_id,
        "state": result.state,
        "result": result.result,
    }
