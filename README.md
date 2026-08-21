# Online Book Store API

Django REST API for a virtual bookstore: users can register, browse books, and submit reviews.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_bookstore
python manage.py runserver
```

Swagger UI: http://127.0.0.1:8000/api/docs/

After seeding, log in as `maya@bookstore.local` with password `Bookstore123!`.
Admin panel: http://127.0.0.1:8000/admin/ — `admin@bookstore.local` / `Bookstore123!`.

All seed users share that password. Re-running `seed_bookstore` does not duplicate rows.

## API

Auth (public):

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`

Send `Authorization: Bearer <access>` on every other request. In Swagger, use **Authorize**.

Books:

- `GET /api/books/` — paginated list (`page`, optional `search`)
- `GET /api/books/<id>/` — details and full content

Reviews:

- `GET /api/books/<id>/reviews/` — other users' reviews
- `POST /api/books/<id>/reviews/` — submit a review (400 if you already reviewed that book)

## Tests

```powershell
pytest
pytest --cov=apps --cov-report=term-missing
```
