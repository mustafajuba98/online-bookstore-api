# Online Book Store API

Django REST API for a virtual bookstore: users can register, browse books, and submit reviews.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Swagger UI: `http://127.0.0.1:8000/api/docs/`

Auth (public):

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`

Send `Authorization: Bearer <access>` on every other API request.

Books:

- `GET /api/books/` — paginated list (`page`, optional `search`)
- `GET /api/books/<id>/` — details and full content
