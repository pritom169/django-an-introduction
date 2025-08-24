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
