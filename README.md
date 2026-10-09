# Blog

A full-stack blog platform with a REST API backend and a single-page Vue frontend.
Users can register, sign in, write and manage posts, browse by category, and
discuss posts through threaded comments.

- **Backend:** Django + Django REST Framework (JWT authentication, SQLite)
- **Frontend:** Vue 3 + Vite (Pinia, Vue Router, Tailwind CSS)

---

## Tech stack

| Layer      | Technologies                                                                 |
| ---------- | ---------------------------------------------------------------------------- |
| Backend    | Django 6, Django REST Framework, SimpleJWT, django-filter, django-cors-headers, Pillow, python-decouple |
| Frontend   | Vue 3, Vite 7, Pinia, Vue Router 5, Axios, Tailwind CSS 4, vue-toastification, js-cookie, Heroicons |
| Database   | SQLite (`backend/my_db.sqlite3`)                                             |

---

## Features

- Email-based authentication with JWT access/refresh tokens
- Custom user profiles (avatar, bio, name) and password change
- Categories with automatic slugs
- Posts with draft/published status, cover image, view counter, and search/ordering
- Threaded comments (replies) with soft delete
- Role checks: only authors can edit or delete their own content
- Modern responsive SPA with toast notifications and route guards

> **Not yet enabled:** subscription and payment apps exist in the code plan but are
> commented out in `backend/config/settings.py` and are not routed. The corresponding
> API endpoints are not available.

---

## Project structure

```
blog/
├── backend/
│   ├── apps/
│   │   ├── accounts/     # Custom user model, auth & profile
│   │   ├── main/         # Categories & posts
│   │   └── comments/     # Comments & replies
│   ├── config/           # Django settings, URLs, WSGI/ASGI
│   ├── media/            # Uploaded files (avatars, post images)
│   ├── manage.py
│   ├── my_db.sqlite3
│   ├── requirements.txt
│   └── .env              # Local secrets (not committed)
└── frontend/
    ├── src/
    │   ├── components/   # Reusable UI components
    │   ├── router/       # Route definitions & guards
    │   ├── services/     # Axios API client
    │   ├── stores/       # Pinia stores (auth, posts, comments)
    │   └── views/        # Page components
    ├── vite.config.js
    └── package.json
```

---

## Getting started

### Prerequisites

- Python 3.11+ (tested with 3.13)
- Node.js `^20.19.0` or `>=22.12.0`

### 1. Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create the .env file (see Environment variables below)
# then apply migrations
python manage.py migrate

# Optional: create an admin account for /admin/
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

The API is served at **http://127.0.0.1:8000**.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The SPA is served at **http://localhost:5173**. It talks to the backend at
`http://localhost:8000` (configured in `src/services/api.js`).

### Other useful commands

| Command              | Description                                |
| -------------------- | ------------------------------------------ |
| `python manage.py check` | Validate the Django project            |
| `python manage.py makemigrations` | Create new migrations         |
| `python manage.py migrate` | Apply migrations                    |
| `npm run build`      | Production build of the frontend           |
| `npm run preview`    | Preview the production build               |
| `npm run lint`       | Lint the frontend (auto-fixes)             |
| `npm run format`     | Format the frontend with Prettier          |

---

## Environment variables

Create `backend/.env` (it is git-ignored). `SECRET_KEY` is required.

```env
SECRET_KEY=replace-with-a-long-random-string
DEBUG=True
FRONTEND_URL=http://localhost:5173

# Optional (Stripe / email integrations)
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@example.com
```

---

## API reference

Base URL: `http://127.0.0.1:8000/api/v1`. Authenticated requests use a
`Authorization: Bearer <access_token>` header.

### Authentication — `/auth/`

| Method             | Endpoint             | Description                          | Auth |
| ------------------ | -------------------- | ------------------------------------ | ---- |
| POST               | `/auth/register/`    | Register and receive tokens          | No   |
| POST               | `/auth/login/`       | Login and receive tokens             | No   |
| POST               | `/auth/logout/`      | Blacklist the refresh token          | Yes  |
| GET / PUT / PATCH  | `/auth/profile/`     | Retrieve or update own profile       | Yes  |
| PUT                | `/auth/change-password/` | Change own password              | Yes  |
| POST               | `/auth/token/refresh/` | Refresh an access token            | No   |

### Posts & categories — `/posts/`

| Method                       | Endpoint                              | Description                       | Auth  |
| ---------------------------- | ------------------------------------- | --------------------------------- | ----- |
| GET / POST                   | `/posts/`                             | List / create posts               | Read: No |
| GET / PUT / PATCH / DELETE   | `/posts/{slug}/`                      | Retrieve / update / delete a post | Write: author |
| GET                          | `/posts/my-posts/`                    | Current user's posts              | Yes   |
| GET                          | `/posts/popular/`                     | 10 most viewed published posts    | No    |
| GET                          | `/posts/recent/`                      | 10 latest published posts         | No    |
| GET                          | `/posts/featured/`                    | Popular posts from the last week  | No    |
| GET / POST                   | `/posts/categories/`                  | List / create categories          | Read: No |
| GET / PUT / PATCH / DELETE   | `/posts/categories/{slug}/`           | Retrieve / update / delete        | Write: auth |
| GET                          | `/posts/categories/{slug}/posts/`     | Published posts in a category     | No    |

Supported post filters: `?category=`, `?author=`, `?status=`, `?search=`,
`?ordering=` (`created_at`, `updated_at`, `views_count`, `title`), `?page=`,
`?page_size=`.

### Comments — `/comments/`

| Method                       | Endpoint                        | Description                         | Auth       |
| ---------------------------- | ------------------------------- | ----------------------------------- | ---------- |
| GET / POST                   | `/comments/`                    | List / create comments              | Read: No   |
| GET / PUT / PATCH / DELETE   | `/comments/{id}/`               | Retrieve / update / soft-delete     | Write: author |
| GET                          | `/comments/my-comments/`        | Current user's comments             | Yes        |
| GET                          | `/comments/post/{post_id}/`     | Comments (with replies) for a post  | No         |
| GET                          | `/comments/{comment_id}/replies/` | Replies to a comment              | No         |

Supported comment filters: `?post=`, `?author=`, `?parent=`, `?search=`,
`?ordering=`.

### Admin

Django admin is available at **http://127.0.0.1:8000/admin/**.

---

## Frontend routes

| Path                   | View                | Access        |
| ---------------------- | ------------------- | ------------- |
| `/`                    | Home                | Public        |
| `/login`               | Login               | Guests only   |
| `/register`            | Register            | Guests only   |
| `/profile`             | Profile             | Authenticated |
| `/change-password`     | Change password     | Authenticated |
| `/posts`               | Posts list          | Public        |
| `/posts/create`        | Create post         | Authenticated |
| `/posts/my`            | My posts            | Authenticated |
| `/posts/:slug`         | Post detail         | Public        |
| `/posts/:slug/edit`    | Edit post           | Authenticated |
| `/categories`          | Categories          | Public        |
| `/categories/:slug`    | Category posts      | Public        |
| `/comments/my`         | My comments         | Authenticated |
| `/*`                   | Not found           | Public        |

---

## Data model

- **User** — extends Django's `AbstractUser`; login by `email`, with `username`,
  `avatar`, `bio`, and timestamps (`users` table).
- **Category** — unique name and auto-generated slug (`categories` table).
- **Post** — belongs to an author and optional category; has `title`, `slug`,
  `content`, `image`, `status` (`draft`/`published`), `views_count` (`posts` table).
- **Comment** — belongs to a post and author, with optional `parent` for threaded
  replies and `is_active` for soft deletion (`comments` table).
