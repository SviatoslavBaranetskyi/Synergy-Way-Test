# Synergy Way Test

Backend service for synchronizing data from external APIs using FastAPI and Celery.  
The project demonstrates a clean, production-oriented backend architecture with background processing, external integrations, and automated tests.

---

## Tech Stack

- Python 3.10  
- FastAPI  
- Celery + Celery Beat  
- Redis  
- PostgreSQL  
- SQLAlchemy 2.0  
- Alembic  
- Docker & Docker Compose  
- Pytest  

---

## Architecture Overview

The application follows a layered architecture with clear separation of responsibilities:

- **API layer** – FastAPI application and HTTP endpoints  
- **Service layer** – business logic and orchestration  
- **Repository layer** – database access and persistence  
- **HTTP clients** – communication with external APIs  
- **Celery workers** – background task execution  
- **Celery Beat** – scheduled background jobs  

This approach improves maintainability, testability, and scalability of the system.

---

## Running the Project

Start all services using Docker Compose:

```bash
docker-compose up --build
```

Once started, the API will be available at:

- http://localhost:8000
- Swagger UI: http://localhost:8000/docs

Celery workers and Celery Beat are started automatically.

## Background Jobs
The project uses Celery for asynchronous and scheduled tasks.

Examples of background jobs:
- Synchronization of users
- Synchronization of posts
- Synchronization of comments

Tasks can be triggered manually via API or executed automatically on schedule via Celery Beat.

## Tests
Run tests locally with:
```
docker compose exec web pytest -q
```

## What This Project Demonstrates
- Clean backend architecture
- Clear separation of concerns
- Background processing with Celery and Celery Beat
- External API integration
- Dockerized infrastructure
- Production-like project structure
- Automated testing

## Deployment (AWS – optional)

The project can be deployed to AWS using the following services:

- EC2 for application and Celery workers
- RDS for PostgreSQL
- ElastiCache (Redis) for Celery broker and backend
- S3 (optional) for data or artifacts storage

Deployment configuration is not included and can be added as a next step.

## Developer
Sviatoslav Baranetskyi

Email: svyatoslav.baranetskiy738@gmail.com