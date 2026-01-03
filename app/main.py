from time import sleep

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.core.db.session import Base, engine
from app.api.routers import users, posts, comments

app = FastAPI(
    title="Synergy Way Test Task",
    version="1.0.0",
)


def init_db_with_retry(max_attempts: int = 30, delay_seconds: float = 2.0) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError as exc:
            print(f"[startup] DB not ready ({attempt}/{max_attempts}): {exc}")
            sleep(delay_seconds)

    raise RuntimeError("Database is not ready")


@app.on_event("startup")
def on_startup() -> None:
    init_db_with_retry()


@app.get("/health", tags=["health"])
def health() -> dict:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
