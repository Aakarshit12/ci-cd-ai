# Phase 2 - Service Registry + Load Balancing

## Overview
Implement a service registry and round-robin load balancer within the existing API Gateway. The registry will store service definitions in PostgreSQL, expose a CRUD API for management, and use a Redis-backed round-robin algorithm for routing requests across upstream URLs. A background task will continually check the health of registered services and update their status.

## Project Type
BACKEND

## Success Criteria
- [ ] PostgreSQL table `registered_services` created via Alembic migration.
- [ ] CRUD API for services available under `/gateway/services`.
- [ ] Round-robin load balancing correctly distributes traffic across active, healthy `upstream_urls`.
- [ ] Background health check runs every 30 seconds and marks unhealthy instances.
- [ ] Existing `middleware.py`, `auth.py`, and `rate_limiter.py` remain untouched.

## Tech Stack
- **Database**: PostgreSQL with SQLAlchemy async ORM (using existing setup in `database.py`).
- **Migrations**: Alembic (initialized strictly inside `backend/`).
- **Cache / LB State**: Redis for atomic increments (`INCR`) and health status.
- **Web Framework**: FastAPI.

## Important Constraints
- **Existing Setup**: Use the existing `Base` and async session from `backend/app/core/database.py`. Do NOT create new ones.
- **File Restrictions**: Do NOT modify any existing files outside of `main.py` and the new Alembic setup files.
- **Alembic Init**: Must be initialized inside the `backend/` directory.
- **Environment**: Ignore `test.db` in `backend/` as PostgreSQL is the target database.

## File Structure
```
backend/gateway/
├── router.py        ← [NEW] FastAPI routes for service registry
├── models.py        ← [NEW] SQLAlchemy models
├── load_balancer.py ← [NEW] round robin logic
└── health_check.py  ← [NEW] background health check task
```

## Task Breakdown

### Task 1: Alembic Initialization & Environment Setup
- **Agent**: `database-architect`
- **Skill**: `database-design`
- **Priority**: P0
- **Dependencies**: None
- **INPUT**: Existing `app.core.database` and `app.models` (user, request).
- **OUTPUT**: Run `alembic init alembic` (or inside `/backend`). Edit `alembic/env.py` to import `app.core.database.Base`, `app.models.user.User`, `app.models.request.Request`, and `gateway.models.RegisteredService`. Point `target_metadata` to `Base.metadata`. Configure sqlalchemy.url in `alembic.ini`.
- **VERIFY**: Alembic is initialized successfully without modifying `database.py` or existing models.

### Task 2: Database Schema & Migration
- **Agent**: `database-architect`
- **Skill**: `database-design`
- **Priority**: P0
- **Dependencies**: Task 1
- **INPUT**: Alembic setup.
- **OUTPUT**: Add `RegisteredService` model in `gateway/models.py`. Generate Alembic migration (`alembic revision --autogenerate -m "Initial schema"`).
- **VERIFY**: Alembic migration file generates successfully and correctly includes BOTH existing models and the new `RegisteredService` model. Upgrade applies successfully.

### Task 3: Service Registry CRUD API
- **Agent**: `backend-specialist`
- **Skill**: `api-patterns`
- **Priority**: P1
- **Dependencies**: Task 2
- **INPUT**: `RegisteredService` model.
- **OUTPUT**: `router.py` with FastAPI endpoints (GET, POST, PATCH, DELETE) under `/gateway/services` prefix. Registration of routes in `main.py`.
- **VERIFY**: API endpoints return 200 OK and correctly interact with the database.

### Task 4: Background Health Check Task
- **Agent**: `backend-specialist`
- **Skill**: `server-management`
- **Priority**: P1
- **Dependencies**: Task 2
- **INPUT**: `RegisteredService` records.
- **OUTPUT**: `health_check.py` with a repeating background task (running every 30s) testing `/health` on upstreams, storing state in Redis.
- **VERIFY**: Redis correctly reflects unhealthy states when an upstream URL returns non-200. Task runs inside FastAPI startup events.

### Task 5: Round-Robin Load Balancer logic
- **Agent**: `backend-specialist`
- **Skill**: `clean-code`
- **Priority**: P1
- **Dependencies**: Task 3, Task 4
- **INPUT**: Registry data, health check states from Redis.
- **OUTPUT**: `load_balancer.py` that implements round-robin routing logic using Redis `INCR` at `gateway:lb:{service_id}:index`, skipping unhealthy instances.
- **VERIFY**: Calling the gateway routes correctly proxies requests in a round-robin sequence to the available healthy upstreams.

## ✅ Phase X: Verification
- [ ] Code Linting (flake8/black)
- [ ] Type Checking (mypy)
- [ ] Ensure `middleware.py`, `auth.py`, `rate_limiter.py` are unchanged
- [ ] Run test suite with mocked Redis
- [ ] Test API registration and load distribution manually
