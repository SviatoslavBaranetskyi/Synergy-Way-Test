from fastapi import APIRouter, Query
from celery.result import AsyncResult
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db.session import SessionLocal
from app.models.comment import Comment
from app.services.tasks.comments import sync_comments
from app.core.celery_app import celery

router = APIRouter()


@router.get("/")
def list_comments(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    session: Session = SessionLocal()
    try:
        items = session.execute(
            select(Comment).offset(offset).limit(limit)
        ).scalars().all()

        total = session.execute(select(Comment)).scalars().all()

        return {
            "items": [
                {
                    "id": c.id,
                    "external_id": c.external_id,
                    "post_id": c.post_id,
                    "user_id": c.user_id,
                }
                for c in items
            ],
            "count": len(items),
            "total": len(total),
            "offset": offset,
            "limit": limit,
        }
    finally:
        session.close()


@router.post("/sync")
def run_comments_sync(limit: int = 20, skip: int = 0):
    task = sync_comments.delay(limit, skip)
    return {"task_id": task.id}


@router.get("/sync/{task_id}")
def get_sync_status(task_id: str):
    result = AsyncResult(task_id, app=celery)
    return {
        "task_id": task_id,
        "state": result.state,
        "result": result.result,
    }
