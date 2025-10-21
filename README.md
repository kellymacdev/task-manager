# RESTful Task Manager API

A Django-based REST API for authenticated task management. Users can register, log in, and perform CRUD operations on their own tasks. JSON responses only; no front-end required.

---

## Tech Stack

- Python 3, Django
- PostgreSQL (or SQLite for local)
- Session-based authentication
- JSON API

---

## Installation

```bash
git clone https://github.com/kellymacdev/task-manager.git
cd task-manager
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
----------------
## API Endpoints

### Authentication

POST /register/ — create user

POST /login/ — log in, returns session cookie

POST /logout/ — log out

### Tasks (authenticated)

GET /tasks/ — list tasks

POST /tasks/ — create task

GET /tasks/<id>/ — retrieve single task

PUT /tasks/<id>/ — update task

DELETE /tasks/<id>/ — delete task

Include session cookie from login for all task operations.
