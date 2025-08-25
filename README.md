# Storefront (Django Demo)

A compact Django e‑commerce demo I used for myself to teach **ORM basics**, **Admin customization**, **generic relations (tags)**, and **PostgreSQL**. Deep tutorials can be found in [django-part1](https://github.com/pritom169/django-an-introduction/blob/main/django-part1/README.md)

## Features

### Django Part 1

- **Apps**: `store` (products, orders, customers) and `tags` (generic tagging via `GenericForeignKey`).
- **Admin**:
  - Custom list pages (`list_display`, `list_filter`, `search_fields`, `actions`).
  - Inline editing (`OrderItemInline`) and **generic** inline (`GenericTabularInline` for `TaggedItem`).
  - Safe override of the base queryset (`get_queryset`) with annotations.
- **ORM**: examples of filtering, `Q`/`F` expressions, `select_related`/`prefetch_related`, aggregation & annotation, and raw SQL when needed.
- **Dev tooling**: optional Django Debug Toolbar.

## Entity Diagram

<img src="images-and-diagrams/er-diagram.png" alt="ER Diagram" width="75%" />

## Quick Setup

```
# 1) Create a local virtualenv and install deps
export PIPENV_VENV_IN_PROJECT=1
pipenv install django psycopg2-binary django-debug-toolbar

# 2) Activate the env
pipenv shell

# 3) Run DB migrations & create admin
python manage.py migrate
python manage.py createsuperuser

# 4) Start the dev server
python manage.py startapp playground
```

# Storefront (Django Demo)

A compact Django e‑commerce demo used to teach **ORM basics**, **Admin customization**, **generic relations (tags)**, and **PostgreSQL**.

For the full, step‑by‑step tutorial, see **[`django-part1/README.md`](./django-part1/README.md)**.

---

## Repo layout

```
.
├─ django-part1/           # The actual Django project (manage.py lives here)
│  └─ README.md            # In-depth guide (setup, ORM, Admin, migrations, etc.)
└─ README.md               # You are here (high-level overview)
```

## Features

- **Apps:** `store` (products, orders, customers) and `tags` (generic tagging via `GenericForeignKey`)
- **Admin:** custom list pages, filters, search, actions, inlines (incl. `GenericTabularInline`)
- **ORM:** filtering, `Q`/`F`, `select_related`/`prefetch_related`, aggregation/annotation, raw SQL
- **Dev tooling:** Django Debug Toolbar (development only)

## Tech stack

- Python ≥ 3.12
- Django ≥ 5.x
- SQLite (default) or PostgreSQL locally
- DB driver (Postgres): `psycopg` v3 (`psycopg[binary]`)
- Environment & deps: Pipenv

## Quick start

> The Django project lives in **`django-part1/`**.

```bash
# 1) Clone and enter the repo
git clone <your-repo-url>
cd django-an-introduction

# 2) Create a local virtualenv & install dependencies
export PIPENV_VENV_IN_PROJECT=1
pipenv install "django>=5.0" "psycopg[binary]>=3.1" django-debug-toolbar

# 3) Activate the environment
pipenv shell

# 4) Apply migrations & create an admin user (inside the project folder)
cd django-part1
python manage.py migrate
python manage.py createsuperuser

# 5) Run the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** and the admin at **/admin/**.

> Use the Debug Toolbar only in development. Do **not** enable it in production.

## Entity diagram

<img src="django-part1/images-and-diagrams/er-diagram.png" alt="ER Diagram" width="75%" />

## Learn more

- Full guide: [`django-part1/README.md`](./django-part1/README.md)
- Topics covered: project setup, templates, ORM patterns, migrations, admin patterns, Debug Toolbar, PostgreSQL config

## Contributing

PRs and issues are welcome. Please keep examples minimal and focused on teaching value.
