from celery import Celery

from app.core.config import settings

celery = Celery(
    "synergy_way",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.services.tasks.users",
        "app.services.tasks.posts",
        "app.services.tasks.comments",
    ],
)

celery.conf.update(
    timezone="UTC",
    enable_utc=True,
)

celery.conf.beat_schedule = {
    "sync-users-every-minute": {
        "task": "app.services.tasks.users.sync_users",
        "schedule": 60.0,
    },
    "sync-posts-every-2-minutes": {
        "task": "app.services.tasks.posts.sync_posts",
        "schedule": 120.0,
        "args": (10, 0),
    },
    "sync-comments-every-3-minutes": {
        "task": "app.services.tasks.comments.sync_comments",
        "schedule": 180.0,
        "args": (20, 0),
    },
}
