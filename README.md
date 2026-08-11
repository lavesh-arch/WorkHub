# WorkHub - Team Collaboration Platform

WorkHub is a backend Team Collaboration Platform built with Python and FastAPI.

The project is designed to provide REST APIs for managing users, projects, tasks, comments, and collaboration workflows.

## Tech Stack

- **Language** — Python
- **Framework** — FastAPI
- **Database** — PostgreSQL
- **ORM** — SQLAlchemy
- **Migration Tool** — Alembic
- **Validation** — Pydantic
- **Authentication** — JWT
- **Testing** — Pytest

## Current Project Structure

At this stage, only the basic folder structure has been created.

```text
WORKHUB/
│
├── .venv/
│
├── src/
│   └── workhub/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── middleware/
│       ├── models/
│       ├── repositories/
│       ├── schemas/
│       ├── services/
│       │
│       ├── __init__.py
│       └── main.py
│
├── tests/
│
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

## Folder Responsibilities

### `src/workhub/api/`

Contains API routes/endpoints. This layer handles HTTP requests and responses and connects routes with the service layer.

### `src/workhub/core/`

Contains application-wide configuration and common functionality such as settings, security, and custom exceptions.

### `src/workhub/db/`

Contains database-related functionality such as database connection, sessions, and dependencies.

### `src/workhub/middleware/`

Contains middleware for common request/response processing such as logging, request timing, and exception handling.

### `src/workhub/models/`

Contains SQLAlchemy database models representing database tables.

Expected entities include:

- Users
- User Profiles
- Projects
- Project Members
- Tasks
- Comments

### `src/workhub/repositories/`

Contains database access logic and queries. Repositories communicate with the database instead of putting database queries directly inside API routes.

### `src/workhub/schemas/`

Contains Pydantic schemas used for API request validation and response structures.

### `src/workhub/services/`

Contains the application's business logic for authentication, users, projects, tasks, comments, and permissions.

### `src/workhub/main.py`

Application entry point. This file will create and configure the FastAPI application and register API routers.

### `tests/`

Contains automated tests for authentication, business logic, API endpoints, and other important functionality.

## Architecture

The application will follow a modular layered architecture:

```text
Client
   │
   ▼
API / Routes
   │
   ▼
Schemas / Validation
   │
   ▼
Services
   │
   ▼
Repositories
   │
   ▼
Database
```

The main goal is to keep API routing logic, business logic, and database access separate.

## Planned Modules

### Authentication

- User Registration
- User Login
- Refresh Token
- Logout
- Change Password
- Forgot Password

### User Management

- Create User
- View User
- Update User
- Delete User
- Activate / Deactivate User
- Update Profile

### Role Based Access Control

The system will support:

- Administrator
- Manager
- Employee

Each role will have different permissions.

### Project Management

- Create Project
- Update Project
- Delete Project
- View Project
- List Projects
- Search Projects

### Task Management

Tasks will support:

- Status
- Priority
- Assignee
- Due Date
- Create Task
- Update Task
- Delete Task
- Assign Task
- Change Status
- Search Tasks

### Comments

- Add Comment
- Update Comment
- Delete Comment
- View Comments

### Future Modules

- Document Management
- Search
- Dashboard
- Audit Logs
- AI Assistant (Phase 2)

## Development Order

The project will be built step-by-step:

```text
1. Project Structure
2. Database Setup
3. SQLAlchemy Models
4. Alembic Migrations
5. Pydantic Schemas
6. Repository Layer
7. Service Layer
8. API Routes
9. Authentication
10. RBAC
11. Testing
12. Additional Modules
```

## Development Status

- [x] Basic project structure
- [ ] Database connection
- [ ] SQLAlchemy models
- [ ] Alembic setup
- [ ] Pydantic schemas
- [ ] Repository layer
- [ ] Service layer
- [ ] API routes
- [ ] Authentication
- [ ] RBAC
- [ ] Project management
- [ ] Task management
- [ ] Comments
- [ ] Documents
- [ ] Search
- [ ] Dashboard
- [ ] Audit logs
- [ ] Automated tests
- [ ] AI Assistant (Phase 2)

## Running the Project

Dependencies will be managed using `uv`.

Once the application is implemented, it will be started with:

```bash
uv run uvicorn workhub.main:app --reload
```

The database and migration setup will be added during implementation.

## Note

This README describes the current project structure and planned architecture. The folders are currently placeholders and will be implemented step-by-step.