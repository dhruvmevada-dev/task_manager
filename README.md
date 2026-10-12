# Task Manager API

Django REST Framework API with JWT authentication. Each user only sees and manages their own tasks.

## Run

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Test

```bash
python manage.py test
```

## Endpoints

| Method | URL | Description |
|---|---|---|
| POST | /register/ | register (username, email, password) |
| POST | /login/ | get access + refresh JWT |
| POST | /token/refresh/ | refresh access token |
| GET | /tasks/ | list your tasks |
| POST | /tasks/ | create a task |
| PUT | /tasks/<id>/ | update a task |
| DELETE | /tasks/<id>/ | delete a task |

Send the token as `Authorization: Bearer <access>`.

Task fields: `title`, `description`, `due_date`, `priority` (low/medium/high), `status` (pending/in_progress/completed).

## Structure

```
config/            project settings and root urls
tasks/             models, serializers, views, urls, tests
```

## Tech

Python, Django, Django REST Framework, SimpleJWT
