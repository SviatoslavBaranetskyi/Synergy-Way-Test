from fastapi import APIRouter, Query
from celery.result import AsyncResult
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db.session import SessionLocal
from app.models.user import User
from app.services.tasks.users import sync_users
from app.core.celery_app import celery

router = APIRouter()


@router.get("/")
def list_users(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    session: Session = SessionLocal()
    try:
        items = session.execute(
            select(User).offset(offset).limit(limit)
        ).scalars().all()

        total = session.execute(select(User)).scalars().all()

        return {
            "items": [
                {
                    "id": u.id,
                    "external_id": u.external_id,
                    "name": u.name,
                    "email": u.email,
                    "created_at": u.created_at.isoformat(),
                }
                for u in items
            ],
            "count": len(items),
            "total": len(total),
            "offset": offset,
            "limit": limit,
        }
    finally:
        session.close()


@router.post("/sync")
def run_users_sync():
    task = sync_users.delay()
    return {"task_id": task.id}


@router.get("/sync/{task_id}")
def get_sync_status(task_id: str):
    result = AsyncResult(task_id, app=celery)
    return {
        "task_id": task_id,
        "state": result.state,
        "result": result.result,
    }
