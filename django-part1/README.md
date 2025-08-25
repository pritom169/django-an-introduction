## Table of contents

- [Final project structure](#final-project-structure)
- [Project Setup](#project-setup)
  - [Set up a project-local virtual environment and install Django](#set-up-a-project-local-virtual-environment-and-install-django)
  - [Create the project](#create-the-project)
  - [Opening the Shell](#opening-the-shell)
  - [Running the development server](#running-the-development-server)
- [Create the first app](#create-the-first-app)
- [Views](#views)
  - [URL configuration](#url-configuration)
- [Templates](#templates)
  - [Where to put templates](#where-to-put-templates)
  - [Minimal example](#minimal-example)
- [Django Debug Toolbar](#django-debug-toolbar)
  - [Install](#install)
  - [Configure (settings.py)](#configure-settingspy)
  - [URLs (storefront/urls.py)](#urls-storefronturlspy)
- [Entity diagram](#entity-diagram)
- [Organizing the project](#organizing-the-project)
- [Models](#models)
  - [Choice fields](#choice-fields)
  - [Defining relationships](#defining-relationships)
    - [One-to-one](#one-to-one)
    - [One-to-many](#one-to-many)
    - [Many-to-many](#many-to-many)
    - [Avoiding circular dependencies](#avoiding-circular-dependencies)
    - [Generic relations (contenttypes)](#generic-relations-contenttypes)
  - [Migrations](#migrations)
    - [Create migration files](#create-migration-files)
    - [Apply migrations](#apply-migrations)
    - [Example: table name & composite index](#example-table-name--composite-index)
    - [Revert / roll back](#revert--roll-back)
  - [Connecting to PostgreSQL](#connecting-to-postgresql)
    - [Install & start (macOS/Homebrew)](#install--start-macoshomebrew)
    - [Create role and database](#create-role-and-database)
  - [Using PostgreSQL in Django](#using-postgresql-in-django)
  - [Running custom SQL via migrations](#running-custom-sql-via-migrations)
- [7. Django ORM](#7-django-orm)
  - [1. Managers and QuerySets](#1-managers-and-querysets)
  - [2. Retrieving Objects](#2-retrieving-objects)
  - [3. Filtering objects](#3-filtering-objects)
  - [4. Complex lookups with Q](#4-complex-lookups-with-q)
  - [5. Field-to-field comparisons with F](#5-field-to-field-comparisons-with-f)
  - [6. Ordering](#6-ordering)
  - [7. Limiting results](#7-limiting-results)
  - [8. Selecting specific fields](#8-selecting-specific-fields)
  - [9. Deferring fields](#9-deferring-fields)
  - [10. Selecting related objects efficiently](#10-selecting-related-objects-efficiently)
  - [11. Aggregations](#11-aggregations)
  - [12. Annotations](#12-annotations)
  - [13. Calling database functions](#13-calling-database-functions)
  - [14. Grouping data](#14-grouping-data)
  - [15. Expressions](#15-expressions)
  - [16. Querying generic relations](#16-querying-generic-relations)
  - [17. Custom managers](#17-custom-managers)
  - [18. Query caching](#18-query-caching)
  - [Creating objects](#creating-objects)
  - [Deleting objects](#deleting-objects)
  - [Transactions](#transactions)
  - [Executing RAW SQL queries](#executing-raw-sql-queries)
    - [Option 1 — Model.objects.raw()](#option-1--modelobjectsraw)
    - [Option 2 — connection.cursor()](#option-2--connectioncursor)
- [Making an Admin Site](#making-an-admin-site)
  - [Access](#access)
  - [Basic branding](#basic-branding)
  - [Registering models](#registering-models)
  - [Customizing list pages](#customizing-list-pages)
  - [Adding a computed column](#adding-a-computed-column)
  - [Selecting related objects](#selecting-related-objects)
  - [Overriding the base queryset](#overriding-the-base-queryset)
  - [Adding drill-down links from admin columns](#adding-drill-down-links-from-admin-columns)
  - [Adding search to the list page](#adding-search-to-the-list-page)
  - [Adding filtering to the list page](#adding-filtering-to-the-list-page)
  - [Creating custom actions](#creating-custom-actions)
  - [Customizing Forms](#customizing-forms)
  - [Adding Data Validation](#adding-data-validation)
  - [Editing Children Using Inlines](#editing-children-using-inlines)
  - [Using Generic Relationship](#using-generic-relationship)
  - [Extending Pluggable Apps](#extending-pluggable-apps)

## Final project structure

```
django-part1/
├─ README.md
├─ Pipfile
├─ Pipfile.lock
├─ manage.py
├─ images-and-diagrams/
│  └─ er-diagram.png
├─ storefront/
│  ├─ __init__.py
│  ├─ admin.py            # site branding (site_title, site_header, index_title)
│  ├─ settings.py
│  ├─ urls.py             # includes admin/, playground/, and __debug__/ when DEBUG
│  ├─ asgi.py
│  └─ wsgi.py
├─ playground/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py             # path("hello/", views.say_hello, name="playground-hello")
│  └─ views.py            # say_hello → renders template with context
│     (templates/)
│       └─ playground/
│          └─ hello.html
├─ store/
│  ├─ __init__.py
│  ├─ admin.py            # ProductAdmin, CollectionAdmin, filters/actions, inlines
│  ├─ apps.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py           # Product, Collection, Customer, Order, OrderItem, etc.
│  ├─ tests.py
│  └─ views.py
├─ tags/
│  ├─ __init__.py
│  ├─ admin.py            # @admin.register(Tag)
│  ├─ apps.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py           # Tag, TaggedItem (GenericForeignKey via contenttypes)
│  ├─ tests.py
│  └─ views.py
└─ store_custom/
   ├─ __init__.py
   ├─ admin.py            # TagInline(GenericTabularInline), CustomProductAdmin,
   └─ apps.py             # unregister/register Product with CustomProductAdmin

```

## Project Setup

### Set up a project‑local virtual environment and install Django

Run:

```bash
# macOS/Linux
PIPENV_VENV_IN_PROJECT=1 pipenv install django
```

**What this does**

- Uses **Pipenv** to create/manage a virtual environment and lock dependencies.
- Sets `PIPENV_VENV_IN_PROJECT=1` so Pipenv creates the environment in `./.venv` (inside your project) instead of a global location.
- Installs **Django** and records it in your `Pipfile`, then locks versions in `Pipfile.lock`.

**Windows equivalents**

- PowerShell:
  ```powershell
  $env:PIPENV_VENV_IN_PROJECT = 1; pipenv install django
  ```
- Command Prompt:
  ```cmd
  set PIPENV_VENV_IN_PROJECT=1 && pipenv install django
  ```

### Create the project

Create the Django project in the current directory (so `manage.py` and the `storefront/` package are placed here, not in a nested folder):

```bash
pipenv run django-admin startproject storefront .
```

**Notes**

- `pipenv run …` runs the command inside your Pipenv-managed virtual environment.
- The trailing `.` tells `django-admin` to scaffold the project **in the current directory** rather than creating an outer `storefront/` folder.
  - If the dot is omitted, Django creates:
    ```
    storefront/
      manage.py
      storefront/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    ```

### Opening the Shell

Activate the project’s virtual environment in a dedicated subshell:

```bash
pipenv shell
```

To exit, type `exit`. For one‑off commands without activating a subshell, use `pipenv run <command>`.

### Running the development server

Use the project’s `manage.py` to start Django so it knows which settings to load.

```bash
python manage.py runserver
```

By default this serves at http://127.0.0.1:8000/ (press Ctrl+C to stop). To bind to all interfaces or a different port:

```bash
python manage.py runserver 0.0.0.0:8000
```

If you’re using Pipenv without activating a subshell, prefix commands with `pipenv run`:

```bash
pipenv run python manage.py runserver
```

## Create the first app

From the project root, create a new Django app named `playground`:

```bash
python manage.py startapp playground
```

This scaffolds the `playground/` package with these key modules:

1. `migrations/` — auto‑generated files that track schema changes and create/update database tables.
2. `admin.py` — configuration for how this app’s models appear and behave in the Django admin.
3. `apps.py` — app configuration (metadata, ready hooks, etc.).
4. `models.py` — model classes that define the database schema and ORM behavior.
5. `tests.py` — automated tests for the app.
6. `views.py` — request handlers (function‑based or class‑based views) that return responses.

## Views

HTTP is a request–response protocol. In Django, a _view_ is a callable (function‑based or class‑based) that takes an `HttpRequest` and returns an `HttpResponse` (or raises an exception such as `Http404`). In other words, it’s the request handler that contains your application logic and decides what to render, redirect, or return as JSON.

### URL configuration

Defining app‑level routes in `playground/urls.py` and including them from the project’s root `urls.py`.

**playground/urls.py**

```python
from django.urls import path
from . import views

urlpatterns = [
    # Pass the view callable itself—no parentheses.
    path("hello/", views.say_hello, name="playground-hello"),
]
```

**storefront/urls.py**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("playground/", include("playground.urls")),
]
```

With this setup, a request to `/playground/hello/` is dispatched to `views.say_hello`.

By convention, Django projects use trailing slashes (e.g., `"hello/"`). If slash is omitted, we have to be aware the default `APPEND_SLASH` behavior may redirect `/hello` to `/hello/` via `CommonMiddleware`.

## Templates

Django uses the template system to generate HTML (or any text) from your view logic.

### Where to put templates

Use either app‑local templates or a project‑level templates directory:

- **App‑local (recommended & self‑contained):** `playground/templates/playground/hello.html`
- **Project‑level:** `templates/hello.html` (enable `TEMPLATES[0]["DIRS"]` in `settings.py`)

With the default `APP_DIRS=True`, Django automatically finds templates inside each app’s `templates/` folder.

**settings.py (optional project‑level directory)**

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # project‑level templates
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [...]},
    },
]
```

### Minimal example

**playground/views.py**

```python
from django.shortcuts import render

def say_hello(request):
    return render(request, "playground/hello.html", {"name": "World"})
```

**playground/templates/playground/hello.html**

```html
<h1>Hello {{ name }}!</h1>
```

When you visit `/playground/hello/`, Django renders `playground/hello.html` with the provided context.

> Note: Do **not** put templates inside the `migrations/` folder.

## Django Debug Toolbar

The Django Debug Toolbar is a development-only panel that surfaces SQL queries, cache usage, and request/response details. In order to add django-toolbar to VS code project, hop into this [link](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

### Install

```bash
pipenv install django-debug-toolbar
```

### Configure (settings.py)

```python
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third‑party
    "debug_toolbar",
    # Our apps
    "playground",
    "store",
    "tags",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]  # required for the toolbar in DEBUG
```

### URLs (storefront/urls.py)

```python
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("playground/", include("playground.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
```

> Use the toolbar only in development. Do not enable it in production.

## Entity diagram

For the e‑commerce example used throughout this guide, the high‑level entity relationships are shown below.

<img src="images-and-diagrams/er-diagram.png" alt="E‑commerce ER diagram" width="80%">

## Organizing the project

A Django **project** is composed of multiple **apps**. There are two common approaches to structuring them:

- **Single “store” monolith:** All models in one app. Simple to install and reuse, but can become bloated as the domain grows.
- **Many micro‑apps:** Very focused apps (Products, Customers, Carts, Orders). High focus, but introduces cross‑app dependencies and migration coupling.

A pragmatic middle ground is:

- **store** — `Product`, `Collection`, `Customer`, `Cart`, `CartItem`, `Order`, `OrderItem`
- **tags** — `Tag`, `TaggedItem` (generic tagging via `contenttypes`)

This balances **high cohesion** (each app has a clear purpose) with **low coupling** (minimal cross‑app references).

Create the apps:

```bash
python manage.py startapp store
python manage.py startapp tags
```

Add them to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third‑party
    "debug_toolbar",
    # Our apps
    "playground",
    "store",
    "tags",
]
```

Note that Django’s migration framework tracks inter‑app dependencies automatically; you don’t need to “install” apps in a strict order, but you should keep related models together to avoid unnecessary coupling.

## Models

When defining Django models, think about two things:

1. **Field types** Comes after the `=` sign (e.g., `CharField`, `DecimalField`, `DateTimeField`).
2. **Field options** Comes the parenthesis `()` (arguments like `max_length`, `null`, `blank`, `choices`, and `validators`).

Example `Product` model:

```python
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # optional in forms/admin
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)  # updated on each save
```

### Choice fields

We use `choices` when a field should accept only a finite set of values. In Django, `choices` is an **iterable of `(value, label)` pairs** (not a dict). Prefer `TextChoices`/`IntegerChoices` enums for readability and type‑safety, and set a sensible `default`.

```python
from django.db import models

class Customer(models.Model):
    class Membership(models.TextChoices):
        BRONZE = "B", "Bronze"
        SILVER = "S", "Silver"
        GOLD   = "G", "Gold"

    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    email      = models.EmailField(unique=True)
    # Keep phone as text; numbers can include +, spaces, parentheses, etc.
    phone      = models.CharField(max_length=32, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1,
        choices=Membership.choices,
        default=Membership.BRONZE,
    )
```

### Defining relationships

#### One-to-one

Use a `OneToOneField` when each record in one table relates to exactly one record in another. Example: each `Customer` has a single `Address`.

```python
from django.db import models

class Address(models.Model):
    street   = models.CharField(max_length=255)
    city     = models.CharField(max_length=255)
    customer = models.OneToOneField(
        'Customer',
        on_delete=models.CASCADE,
        related_name='address',
        primary_key=True,  # Address PK equals the Customer PK
    )
```

- The reverse accessor is `customer.address` (because of `related_name`).
- `CASCADE` removes the address when its customer is deleted.

#### One-to-many

Put the `ForeignKey` on the "many" side. Example: a `Customer` can have many `Address` rows.

```python
class Address(models.Model):
    street   = models.CharField(max_length=255)
    city     = models.CharField(max_length=255)
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='addresses',
    )
```

- Use `PROTECT` if you want to prevent deleting a customer that still has addresses.

#### Many-to-many

Use `ManyToManyField` for symmetric N↔N relations. Django creates the join table automatically (or you can specify `through=` for a custom one).

```python
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount    = models.FloatField()

class Product(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit_price  = models.DecimalField(max_digits=6, decimal_places=2)
    inventory   = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection  = models.ForeignKey('Collection', on_delete=models.PROTECT, related_name='products')
    promotions  = models.ManyToManyField(Promotion, blank=True)
```

#### Avoiding circular dependencies

If two models reference each other, use a _string_ model reference and consider disabling the reverse relation when it isn’t useful.

```python
class Collection(models.Model):
    label = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',  # do not create a reverse relation on Product
    )

class Product(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit_price  = models.DecimalField(max_digits=6, decimal_places=2)
    inventory   = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection  = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
```

- `SET_NULL` keeps the collection when the featured product is deleted.
- `related_name='+'` prevents creating an unnecessary reverse relation on `Product`.
- A _featured product_ is a single pointer, not a membership—so it is **not** a many‑to‑many.

#### Generic relations (contenttypes)

Use generic relations to attach a model to arbitrary targets without tight coupling. This relies on Django’s `contenttypes` framework.

```python
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

- `tag`: the tag record (e.g., “sale”).
- `content_type`: which model the tag applies to (e.g., `Product`).
- `object_id`: the primary key of the target row.
- `content_object`: direct access to the target instance.

```python
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class LinkedItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

#### Migrations

Migrations are version‑controlled schema changes generated from your models.

##### Create migration files

```bash
python manage.py makemigrations            # all apps with changes
python manage.py makemigrations store      # a specific app
python manage.py makemigrations store --name add_customer_index
```

Django writes migration files into each app’s `migrations/` directory.

##### Apply migrations

```bash
python manage.py migrate                   # apply all unapplied migrations
python manage.py migrate store             # apply only the 'store' app
```

##### Example: table name & composite index

If you rename the table and add an index, put that in the model’s `Meta`:

```python
from django.db import models

class Customer(models.Model):
    ...
    class Meta:
        db_table = "store_customers"
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
        ]
```

Then create and apply a migration:

```bash
python manage.py makemigrations store --name customer_table_and_index
python manage.py migrate
```

Keep migrations small and focused (ideally one logical change per migration) to make reviews and rollbacks easier.

##### Revert / roll back

List migrations and their state:

```bash
python manage.py showmigrations store
```

Migrate to a specific migration (by number or name), or unapply all with `zero`:

```bash
python manage.py migrate store 0003
python manage.py migrate store zero
```

Use `--plan` to preview changes, and `--fake` only for exceptional cases when the database already matches the desired state.

### Connecting to PostgreSQL

Set up a local PostgreSQL instance and create a database/user for the project.

#### Install & start (macOS/Homebrew)

```bash
brew install postgresql@16
brew services start postgresql@16
```

> If you already have PostgreSQL installed, you can skip the install step. On Linux, use your package manager (e.g., `apt install postgresql`) and on Windows use the official installer.

#### Create role and database

Open the PostgreSQL shell and create a user and database:

```bash
psql -d postgres
```

Then run:

```sql
CREATE ROLE myuser WITH LOGIN PASSWORD 'mypassword';
ALTER ROLE myuser CREATEDB;
CREATE DATABASE storefront OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE storefront TO myuser;
```

Exit with `\q`.

> Optional GUI: connect with pgAdmin/TablePlus using: **Host** `localhost`, **Port** `5432`, **Database** `storefront`, **User** `myuser`, **Password** `mypassword`.

### Using PostgreSQL in Django

Install the PostgreSQL driver (psycopg 3):

```bash
pipenv install "psycopg[binary]>=3.1"
```

Configure `DATABASES` in `settings.py` (reading from environment variables is recommended):

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "storefront",
        "HOST": "localhost",
        "USER": "myuser",
        "PASSWORD": "mypassword",
        "PORT": 5432
    }
}
```

Apply migrations to create tables in PostgreSQL:

```bash
python manage.py migrate
```

### Running custom SQL via migrations

Create an empty migration and add SQL to it:

```bash
python manage.py makemigrations store --empty --name seed_initial_collection
```

In the generated file, add a `RunSQL` operation with forward and reverse SQL:

```python
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                INSERT INTO store_collection (label)
                VALUES ('collection1');
            """,
            reverse_sql="""
                DELETE FROM store_collection
                WHERE label = 'collection1';
            """,
        ),
    ]
```

Run it:

```bash
python manage.py migrate
```

The forward SQL runs on migrate; the `reverse_sql` runs if you roll back the migration.

## 7. Django ORM

### 1. Managers and QuerySets

Every attribute in Django has an object. It is also called manager object. It is sort of like a remote control which comes with lot of buttons which we can use to talk to our database.

In `playground/views.py` we can look into the `say_hello` function. Inside it we can see the following code:

```python
def say_hello(request):
    query_set = Product.objects.all()
    for product in query_set:
        print(product)

    return render(request, 'hello.html', { 'name': 'Pritom'})
```

The query set `query_set = Product.objects.all()` is a lazy, chainable collection of database rows mapped to model instances (or dicts/tuples if your use values/values_list).

By `Lazy` means, it does not hit the DB. I turn when you evaluate it by: - iterating over it (for p in qs:), - casting to list(qs), - calling len(qs), bool(qs), - slicing it (qs[:10]), - exists(), count(), first(), etc.

### 2. Retrieving Objects

Let's come to retrieving objects. Now let's assume we want to get only one product. That would be a single object.

Let's assume we want to get the product with product id 1.

```python
product = Product.objects.get(pk=1)
```

Now, what if product_id with 1 does not exist. It will throw an exception. We can handle it using the classis try and catch block.

```python
try:
    product = Product.objects.get(pk=0)
except ObjectDoesNotExist:
    pass
```

If we debug the application and look what sql code django ORM is typing for us we can find it is also doing some sql query for us.

```sql
SELECT "store_product"."id",
       "store_product"."title",
       "store_product"."slug",
       "store_product"."description",
       "store_product"."unit_price",
       "store_product"."inventory",
       "store_product"."last_update",
       "store_product"."collection_id"
  FROM "store_product"
 WHERE "store_product"."id" = 0
 LIMIT 21
```

As usual try catch block looks ugly. However, we can avoid them by using `filter()` and chaining it with `first()`. P.S. First can be none.

```python
product = Product.objects.filter(pk=0).first()
```

If we want to see, if a product exists or not, we can simply do it by using `exists()` in the place of `first()`.

```python
product_exists = Product.objects.filter(pk=0).exits()
```

### 3. Filtering objects

Use **field lookups** in `filter()` to express conditions. Common operators:

- `__gt`, `__gte`, `__lt`, `__lte` — greater/less than
- `__range` — inclusive range
- `__contains` / `__icontains` — substring (case‑sensitive/insensitive)

```python
# Price > 20
qs = Product.objects.filter(unit_price__gt=20)

# 20 ≤ price ≤ 30
qs = Product.objects.filter(unit_price__range=(20, 30))

# Title contains "coffee" (case‑insensitive)
qs = Product.objects.filter(title__icontains="coffee")
```

See the official docs for all lookups.

#### Combining conditions

Multiple conditions can be combined in one `filter()` or chained; both are ANDed:

```python
qs = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
qs = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
```

### 4. Complex lookups with `Q`

Use `Q` objects for OR and NOT logic.

```python
from django.db.models import Q

# inventory < 10 OR unit_price < 20
qs = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

# inventory < 10 AND NOT (unit_price < 20)
qs = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))
```

### 5. Field‑to‑field comparisons with `F`

Use `F` expressions to compare/update using other field values at the database level.

```python
from django.db.models import F

# Example: inventory equals the rounded unit price (illustrative)
qs = Product.objects.filter(inventory=F("inventory"))
```

### 6. Ordering

Use `order_by()`; a leading `-` sorts descending. `reverse()` flips the current ordering.

```python
qs = Product.objects.order_by("unit_price")
qs = Product.objects.order_by("unit_price", "-title")
qs = Product.objects.order_by("unit_price", "-title").reverse()
```

### 7. Limiting results

Slice the QuerySet (SQL `LIMIT`/`OFFSET`):

```python
qs = Product.objects.order_by("unit_price", "-title")[:5]
```

### 8. Selecting specific fields

`values()` returns dicts; `values_list()` returns tuples. Use double‑underscore to traverse relations.

```python
# Dicts with id and title
qs = Product.objects.values("id", "title")

# Include a related field from Collection
qs = Product.objects.values("id", "title", "collection__title")

# Tuples
qs = Product.objects.values_list("id", "title")

# Single column as a flat list
ids = Product.objects.values_list("id", flat=True)
```

**Exercise:** products that appear in orders, sorted by title

```python
ids = OrderItem.objects.values_list("product_id", flat=True).distinct()
qs = Product.objects.filter(id__in=ids).order_by("title")
```

### 9. Deferring fields

Load only what you need with `only()` or exclude with `defer()`:

```python
qs = Product.objects.only("id", "title")
qs = Product.objects.defer("description")
```

Be careful: accessing a deferred field later triggers an extra query **per row** (N+1 behavior).

### 10. Selecting related objects efficiently

- Use `select_related()` for single‑valued relations (FK/OneToOne) — SQL join.
- Use `prefetch_related()` for multi‑valued relations (ManyToMany/reverse FK) — separate query + Python join.

```python
# Product with its Collection (FK) and Promotions (M2M)
qs = (
    Product.objects
    .select_related("collection")
    .prefetch_related("promotions")
)
```

Render example:

```html
<ul>
  {% for product in products %}
  <li>
    {{ product.title }} - {{ product.collection.title }}
    <ul>
      {% for promo in product.promotions.all %}
      <li>{{ promo.description }}</li>
      {% empty %}
      <li>No promotions</li>
      {% endfor %}
    </ul>
  </li>
  {% empty %}
  <li>No products</li>
  {% endfor %}
</ul>
```

**Exercise:** last 5 orders with their customer and items (including product)

```python
# If the reverse name is `orderitem_set`; adjust to your related_name if different
qs = (
    Order.objects
    .select_related("customer")
    .prefetch_related("orderitem_set__product")
    .order_by("-placed_at")[:5]
)
```

### 11. Aggregations

```python
from django.db.models import Count, Min, Max, Avg, Sum

result = Product.objects.aggregate(
    count=Count("id"),
    min_price=Min("unit_price"),
)
```

### 12. Annotations

Attach computed fields per row.

```python
from django.db.models import Value, BooleanField

qs = Customer.objects.annotate(is_new=Value(True, output_field=BooleanField()))
```

### 13. Calling database functions

```python
from django.db.models import F, Value
from django.db.models.functions import Concat

qs = Customer.objects.annotate(
    full_name=Concat("first_name", Value(" "), "last_name")
)
```

### 14. Grouping data

Count orders per customer (adjust relation name to your models):

```python
from django.db.models import Count

qs = Customer.objects.annotate(orders_count=Count("orders"))
```

### 15. Expressions

```python
from decimal import Decimal
from django.db.models import F, DecimalField, ExpressionWrapper

discounted_price = ExpressionWrapper(
    F("unit_price") * Decimal("0.80"),
    output_field=DecimalField(max_digits=6, decimal_places=2),
)

qs = Product.objects.annotate(discounted_price=discounted_price)
```

### 16. Querying generic relations

```python
from django.contrib.contenttypes.models import ContentType

ct = ContentType.objects.get_for_model(Product)
qs = TaggedItem.objects.select_related("tag").filter(
    content_type=ct,
    object_id=1,
)
# Alternatively, if you have the instance:
# qs = TaggedItem.objects.select_related("tag").filter(content_object=product)
```

### 17. Custom managers

```python
from django.contrib.contenttypes.models import ContentType

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        ct = ContentType.objects.get_for_model(obj_type)
        return (
            self.get_queryset()
            .select_related("tag")
            .filter(content_type=ct, object_id=obj_id)
        )

class TaggedItem(models.Model):
    objects = TaggedItemManager()
```

### 18. Query caching

QuerySets cache results **after evaluation**. Reusing the same evaluated QuerySet avoids a second trip to the database.

```python
qs = Product.objects.all()
list(qs)      # hits the DB and caches the result
qs[0]         # served from cache (no extra query)

qs = Product.objects.all()
qs[0]         # hits the DB (no cache yet)
list(qs)      # now hits the DB again to load the full result set
```

### Creating objects

Use the ORM to insert rows via one of these patterns:

- **Instance + `save()`**
- **Manager shortcut `Model.objects.create(...)`**
- **`bulk_create([...])`** for many rows
- **`get_or_create()`** to avoid duplicates under a unique constraint

**Example: create a `Collection` with a featured product**

```python
from django.shortcuts import render
from store.models import Collection, Product

def say_hello(request):
    # Load the product we want to feature
    product = Product.objects.get(pk=1)

    # Create the collection (use featured_product_id=1 to skip the extra query)
    collection = Collection.objects.create(
        label="Video Games",
        featured_product=product,
    )

    return render(request, "playground/hello.html", {"name": "Pritom"})
```

---

#### Updating a single field safely (avoid unintended overwrites)

Don’t instantiate a bare model with only a primary key and call `save()` without telling Django which fields changed—unspecified fields may be written with empty/default values. Use one of the safe patterns below.

**Option 1 — fetch, modify, and save only the changed fields**

```python
collection = Collection.objects.get(pk=11)
collection.featured_product = None
collection.save(update_fields=["featured_product"])  # writes just this column
```

**Option 2 — update via QuerySet (single SQL statement, no initial read)**

```python
Collection.objects.filter(pk=11).update(featured_product=None)
```

**Option 3 — save a stub instance with `update_fields`**

```python
c = Collection(pk=11)
# If you already know the FK id, you can set it directly:
# c.featured_product_id = None
c.featured_product = None
c.save(update_fields=["featured_product"])  # updates only this column
```

These approaches update just the targeted column and prevent accidental data loss.

### Deleting objects

Deleting rows is straightforward. You can delete a single instance or perform a bulk delete via a QuerySet.

**Delete a single row**

```python
# Fast path: delete by primary key without fetching the row first
Collection(pk=11).delete()

# Or fetch, then delete
collection = Collection.objects.get(pk=11)
collection.delete()
```

**Bulk delete**

```python
# Delete all collections with id > 5
deleted_count, _ = Collection.objects.filter(pk__gt=5).delete()
```

`QuerySet.delete()` executes a single SQL statement and returns a tuple `(count, details)`.

**Important considerations**

- Deleting follows each relation’s `on_delete` rule (e.g., `CASCADE`, `PROTECT`, `SET_NULL`). A `PROTECT` will raise an error if related rows exist.
- Bulk deletes **do not** call an overridden `Model.delete()` on each row. If you rely on custom cleanup logic, delete instances individually or move logic to signals.
- If permanent removal isn’t desired, consider a _soft delete_ (e.g., a `is_deleted = models.BooleanField(default=False)`) and filter it out at the Manager level.

### Transactions

Use transactions to ensure related writes either **all succeed** or **all roll back**. In Django, wrap write operations in `transaction.atomic()`.

**Example: create an `Order` and its `OrderItem` atomically**

```python
from django.db import transaction
from store.models import Order, OrderItem, Product

@transaction.atomic
def create_order(customer_id: int, product_id: int, qty: int = 1):
    # All DB writes in this function are atomic
    order = Order.objects.create(customer_id=customer_id)

    # Load the product (optionally lock it if you also adjust inventory)
    product = Product.objects.get(pk=product_id)
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=qty,
        unit_price=product.unit_price,
    )
```

**Block‑scoped transaction**

```python
from django.db import transaction

def say_hello(request):
    with transaction.atomic():
        order = Order.objects.create(customer_id=1)
        OrderItem.objects.create(order=order, product_id=1, quantity=1, unit_price=10)
```

**Good to know**

- Any **exception** raised inside an `atomic` block rolls back all queries in that block.
- The decorator form wraps the whole function; the context‑manager form lets you scope a smaller section.
- Nested `atomic()` blocks create **savepoints**; raising an exception rolls back to the **nearest** `atomic()`.
- If you need to run side effects **only after a successful commit** (e.g., send an email), use `transaction.on_commit`:

```python
from django.db import transaction

def create_and_notify(...):
    with transaction.atomic():
        order = Order.objects.create(...)
    transaction.on_commit(lambda: send_order_email(order.id))
```

### Executing RAW SQL queries

The ORM covers most use‑cases, but sometimes raw SQL is clearer or faster (e.g., complex joins, CTEs, window functions, vendor‑specific features). When you drop down to SQL, **always parameterize** inputs to avoid SQL injection.

#### Option 1 — `Model.objects.raw()`

Returns model instances from a raw SELECT. Your query **must include the primary key** column as `id` (or alias it to `id`).

```python
from django.shortcuts import render
from store.models import Product

def say_hello(request):
    products = Product.objects.raw(
        """
        SELECT id, title, description, unit_price, inventory, last_update, collection_id
        FROM store_product
        WHERE unit_price > %s
        ORDER BY unit_price DESC
        LIMIT 20
        """,
        [20],  # parameters are safely bound by the DB driver
    )
    return render(request, "playground/hello.html", {"name": "Pritom", "products": list(products)})
```

Notes:

- The result is a lazy iterable of **read‑only** model instances.
- Only `SELECT` is supported here (no INSERT/UPDATE/DELETE).

#### Option 2 — `connection.cursor()`

Use a DB cursor for arbitrary SQL and manual row handling.

```python
from decimal import Decimal
from django.db import connection

def expensive_products(min_price: Decimal = Decimal("20.00")):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, unit_price
            FROM store_product
            WHERE unit_price > %s
            ORDER BY unit_price DESC
            LIMIT 20
            """,
            [min_price],
        )
        rows = cursor.fetchall()
    # Map tuples to dicts for convenient use in templates/JSON
    return [{"id": r[0], "title": r[1], "unit_price": r[2]} for r in rows]
```

Tips:

- Wrap multiple write statements in `transaction.atomic()`.
- Prefer migrations for schema changes; raw SQL in code should be **data** queries, not DDL.
- Keep raw SQL localized (utility functions) and covered by tests to catch dialect changes.

## Making an Admin Site

### Access

Django includes a built‑in admin at `/admin/`. Create a superuser to sign in:

```bash
python manage.py createsuperuser
```

### Basic branding

Set the admin site's title and headers once at startup. It's clearer to keep this in an admin module (e.g., `storefront/admin.py`) so the branding lives next to the rest of your admin configuration:

```python
from django.contrib import admin

admin.site.site_title = "Storefront Admin"
administrator
admin.site.site_header = "Storefront Administration"
admin.site.index_title = "Dashboard"
```

> You can also set these in `storefront/urls.py`, but keeping them in `admin.py` is cleaner and avoids surprising side‑effects.

### Registering models

To make a model appear in the Django admin, register it in the app’s `admin.py`.

```python
from django.contrib import admin
from . import models

admin.site.register(models.Collection)
```

After registration, the changelist will show your `Collection` rows. By default, Django renders objects as generic labels like:

```
Collection object (10)
Collection object (9)
...
Collection object (1)
```

Provide a meaningful label by implementing `__str__` on the model:

```python
from django.db import models

class Collection(models.Model):
    title = models.CharField(max_length=255)
    # … other fields …

    def __str__(self) -> str:
        return self.title
```

Now the admin will display the collection title (e.g., `Grocery`, `Toys`, `Magazines`) instead of `Collection object (…)`.

Optionally, define a default sort order so items appear alphabetically:

```python
class Collection(models.Model):
    title = models.CharField(max_length=255)
    # … other fields …

    class Meta:
        ordering = ["title"]
```

**Notes**

- `__str__` defines the human‑readable representation across your project (admin lists, dropdowns, logs, etc.).
- `Meta.ordering` sets the default `ORDER BY` for queries. The admin respects it unless you specify `ordering` on a `ModelAdmin`.

**Alternative registration (decorator)**

```python
from django.contrib import admin
from . import models

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass
```

### Customizing list pages

Registering with the decorator lets you keep the model and its admin configuration together:

```python
from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price"]
    list_editable = ["unit_price"]  # must also appear in list_display and cannot be the first column
    list_per_page = 10
```

**What these options do**

- `@admin.register(models.Product)` — registers `Product` with this `ModelAdmin`. (Equivalent to `admin.site.register(Product, ProductAdmin)`.)
- `list_display` — columns to show in the changelist table. Defaults to just `__str__`; specify fields, callables, or model methods to add more.
- `list_editable` — makes selected columns editable directly in the list view. Fields must also be in `list_display` and **cannot** include the first column (the one that links to the detail page).
- `list_per_page` — paginates the changelist (defaults to 100).

Apply the same pattern to other models (e.g., `CustomerAdmin`) to keep your admin consistent.

> Reference: Django docs — [ModelAdmin options](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#modeladmin-options)

### Adding a computed column

You can add a derived/read‑only column to the changelist by defining a method on your `ModelAdmin` and including it in `list_display`.

```python
from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price", "inventory_status"]

    @admin.display(description="Inventory", ordering="inventory")
    def inventory_status(self, obj) -> str:
        """Show a simple stock indicator based on the inventory level."""
        return "Low" if obj.inventory < 10 else "OK"
```

**Notes**

- Methods used in `list_display` receive the model instance (`obj`) and must return a string, number, boolean, or HTML (use `format_html`).
- `@admin.display(description=..., ordering=...)` sets the column label and enables sorting by a real field (`inventory` here).
- For complex values (e.g., badges), return `format_html(...)`. For expensive calculations, annotate them in `get_queryset()` and read the annotated value in the display method.

### Selecting related objects

Avoid N+1 queries when showing related fields in the admin by joining single‑valued relations up front.

```python
from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "collection_title", "unit_price"]
    list_select_related = ["collection"]  # join Collection for one query

    @admin.display(description="Collection", ordering="collection__title")
    def collection_title(self, obj) -> str:
        return obj.collection.title
```

**Why this helps**

- `list_select_related` applies `select_related("collection")` to the admin queryset, preventing one extra query per row (the classic N+1 issue).
- `collection_title` renders a readable column from the related `Collection`.
- `ordering="collection__title"` enables sorting by the related field.

Use `list_select_related` for **ForeignKey/OneToOne** relations. For **ManyToMany** or reverse FK relations, prefer `prefetch_related()` (see the ORM section on selecting related objects efficiently).

### Overriding the base queryset

Use `get_queryset()` on a `ModelAdmin` to add annotations/joins or apply default filters for the changelist.

```python
from django.contrib import admin
from django.db.models import Count
from . import models

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["label", "products_count"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(products_count=Count("products"))  # reverse FK from Product.related_name='products'

    @admin.display(ordering="products_count", description="Products")
    def products_count(self, obj) -> int:
        return obj.products_count
```

**What’s happening**

- `super().get_queryset(request)` returns the base queryset (with admin-level filters/permissions applied).
- `.annotate(products_count=Count("products"))` adds a per‑row aggregate using the reverse relation from `Collection`→`Product` (via `related_name='products'`).
- `products_count()` reads the annotated value and makes it sortable via `ordering="products_count"`.

### Adding drill‑down links from admin columns

Make computed columns actionable by turning them into links that open a filtered changelist. Example: clicking the **Products** count on a `Collection` row should open the Product changelist filtered to that collection.

```python
from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from urllib.parse import urlencode
from . import models

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["label", "products_count_link"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(products_count=Count("products"))  # Product.related_name='products'

    @admin.display(description="Products", ordering="products_count")
    def products_count_link(self, obj) -> str:
        """Link to the Product changelist filtered by this collection."""
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": obj.id})  # use __exact if needed: collection__id__exact
        )
        return format_html('<a href="{}">{}</a>', url, obj.products_count)
```

**How it works**

- `reverse("admin:store_product_changelist")` builds the URL for the Product changelist. The pattern is `admin:<app_label>_<model_name>_changelist` (both lower‑case).
- `urlencode({...})` safely creates the query string. Admin understands field lookups in GET params; `collection__id` filters products where `collection_id = <id>` (you can also use `collection__id__exact`).
- `format_html(...)` returns a safe HTML anchor without disabling auto‑escaping.

**Tips**

- If your `Product` foreign key to `Collection` is named differently (e.g., `category`), change the filter key accordingly (e.g., `category__id`).
- To filter multiple values, pass a comma‑separated string to `__in`, e.g., `{"collection__id__in": "1,2,3"}`.
- Adding `list_filter = ["collection"]` to `ProductAdmin` will show the same filter pre‑selected in the sidebar when the page opens.

### Adding search to the list page

Enable the search box by declaring `search_fields` on the `ModelAdmin`.

```python
from django.contrib import admin
from . import models

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Default for strings is case‑insensitive containment (icontains)
    search_fields = [
        "^first_name",   # case‑insensitive prefix match (istartswith)
        "^last_name",
        "email",         # substring match anywhere (icontains)
    ]
    search_help_text = "Search by first/last name (prefix) or anywhere in email."
```

**How it works**

- Without a prefix, Django uses `__icontains` (substring, case‑insensitive).
- Prefix a field with:
  - `^` → use `istartswith` (fast prefix search; case‑insensitive).
  - `=` → use exact match.
  - `@` → use full‑text search (PostgreSQL only).
- You can traverse relations with double‑underscores, e.g., `order__customer__email`.

**Examples**

```python
# Customers whose first name starts with “m” (case‑insensitive)
search_fields = ["^first_name"]

# Search by phone or email anywhere in the string
search_fields = ["phone", "email"]

# Search orders by customer email prefix and order id exactly
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ["^customer__email", "=id"]
```

**Notes**

- If initial searches return too many results, prefer `^` to keep queries selective and add appropriate DB indexes.
- Use `search_help_text` to guide admins on what the search box matches.

### Adding filtering to the list page

Add sidebar filters with `list_filter`. For common field types, Django provides helpful built‑ins.

```python
from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = [
        "collection",                                # ForeignKey → dropdown
        ("last_update", admin.DateFieldListFilter),  # date presets (Today, Past 7 days, etc.)
        "promotions",                                # ManyToMany → membership filter
        # For numeric ranges (e.g., inventory), add a custom filter (below)
    ]
```

For numeric or custom ranges, implement `admin.SimpleListFilter`.

```python
class InventoryLevelFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory_level"

    def lookups(self, request, model_admin):
        return [
            ("<10", "Low (<10)"),
            ("10-49", "Medium (10–49)"),
            ("50+", "High (≥50)"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "<10":
            return queryset.filter(inventory__lt=10)
        if value == "10-49":
            return queryset.filter(inventory__gte=10, inventory__lt=50)
        if value == "50+":
            return queryset.filter(inventory__gte=50)
        return queryset  # or return None to leave the queryset unchanged
```

Use it in your `ModelAdmin`:

```python
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = [
        "collection",
        ("last_update", admin.DateFieldListFilter),
        InventoryLevelFilter,
    ]
```

**Notes**

- `title` controls the label shown in the sidebar.
- `parameter_name` defines the query‑string key (e.g., `?inventory_level=50%2B`) and should be stable for bookmarks.
- In `queryset()`, return a filtered `QuerySet` or `None` (meaning “no additional filtering”).
- For large FK/M2M filters, consider `admin.RelatedOnlyFieldListFilter` to show only related items used by the current result set:

  ```python
  list_filter = [("collection", admin.RelatedOnlyFieldListFilter)]
  ```

- Boolean and `choices` fields get useful filters automatically—just include the field name in `list_filter`.

### Creating custom actions

Admin **actions** let you run bulk operations on the selected rows from a changelist (via the “Action” dropdown sits at the top of the page). We will declare them on our `ModelAdmin`.

```python
from django.contrib import admin, messages
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ["clear_inventory"]  # show in the Action dropdown

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        """Set inventory to 0 for all selected products."""
        updated = queryset.update(inventory=0)  # single bulk UPDATE
        self.message_user(
            request,
            f"{updated} product(s) were successfully updated.",
            level=messages.SUCCESS,
        )
```

**How this works**

- `actions` lists method names defined on the `ModelAdmin`.
- Action methods have the signature `(self, request, queryset)`.
- Use `queryset.update(...)` for efficient, single‑query updates.
- Use `self.message_user(...)` to show a success/warning/error banner. Common levels are `messages.SUCCESS`, `messages.WARNING`, and `messages.ERROR`.

**Tips**

- To limit who can run an action, override `has_change_permission`/`get_actions` or check `request.user` inside the action.
- If an action needs confirmation, render and return an `HttpResponse` (e.g., a template with a confirm form) instead of redirecting immediately.

### Customizing Forms

If we go to individual product forms, we can see a custom update page with all the updating options. However, we can customize them even more.

- If we want to show certain fields, we can do that using fields property `fields = ['title', 'slug']`
- If we want to show every field, except some fields we can do them using `exclude = ['promotions']`
- If we want to make a field readonly, we can make it readonly by `readonly = ['promotions']`
- Now it would be nice, when we populate title field, the slug field automatically gets populated. However, we have to keep one thing in mind, if we touch the slug field and go to the title field again, this feature will not work.

```python
prepopulated_fields = {
        'slug': ['title']
    }
```

- The collection dropdown field is where we should put our attention. If we put look at the dropdown, it loads all the collection name at once. If the collection list was bigger, it would have a bit of overhead. We can implement them by simply using `autocomplete_fields`.

  - However just putting `autocomplete_fields` is not good enough. We will see some error in the terminal.
  - As we are trying the search all the Collections by their title, we have to go to `CollectionAdmin` class and add `search_fields = ['title']`
  - Once we do it, we can see when we load up the collection field we don't see all of the collection name being loaded at once. Once we write a title and pause our writing for a moment, it gives us all the matching titles with collection.

- If you want to go crazy with all the other configuration, hop into [Django Model Admin Page] (https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#modeladmin-options)

- Now if we want to add another order we need to select a payment status and a customer. We see the same problem appearing again. Thus, we will add `autocomplete_fields = ['customer']` to our OrderAdmin class. However, we don't need to add further search field into CustomerAdmin class as we already added the search criteria in customer

### Adding Data Validation

If we go to any page where entities (products, orders) has been added, we will see if we click on the save button without populating any field, it will show some proper validation.

- However we can go even further, when adding product we have to add description field. However we can make them optional. Inside the Product class, we have to add the following field `description = models.TextField(null=True, blank=True)`. - `null=True` makes it nullable on the database level - `blank=True` makes it nullable on the admin sites.

- Now we need to save the migrations into a migration file by using `python manage.py makemigrations store`. Afterwards, we can migrate using the command `python manage.py migrate`

Now let's shift our attention to the validators. The unit price accepts negative value which should not be the case.

- We will first go the `models.py` file and import them from `from django.core.validators import MinValueValidator`
- Inside the `unit_price` we will add `validators=[MinValueValidator(1)`

We can learn more about validator from [Django Validators](https://docs.djangoproject.com/en/5.2/ref/validators/)

### Editing Children Using Inlines

Now when we try to add an order, we must also an OrderItem to an Order. We can add them using `TabularInline`. Let's look at the code.

- `inlines = [OrderItemInline]` inlines help you to edit related models on the same page as the parent model.
- Now let's look at the code of `OrderItemInline`
  - `model = models.OrderItem` the model name needs to be mentioned.
  - If we don't want to show some field extra, we can give `extra = 0`
- Now if we want individual entities of the children to be present as a List format, we use `StackedInline`

```python
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
```

### Using Generic Relationship

- In order to register for generic relations, between Product and Tag we will first register the Tag in the `admin.py` by using `admin.site.register(Tag)`
- Then in the `models.py` inside the Tag model we will return the label using `def __str__(self)`
- Afterwards we have to import `from django.contrib.contenttypes.admin import GenericTabularInline` in order to support the generic-relationships
- Afterwards, we will make a class `TagInline(GenericTabularInline)`
  ```python
  class TagInline(GenericTabularInline):
      model = TaggedItem
      extra = 0
  ```
- In order to search the tags, we have to go a little bit further.
  - For the inline class to work inside the product page of ProductAdmin, we have include it inside the inlines array `inlines = [TagInline]`
  - Now we we have to remove `admin.site.register(Tag)` and replace it with `@admin.register(Tag)` as we are using the decorator on top of the function.

### Extending Pluggable Apps

Right now in the `admin.py` of store app still depends on the `admin.py` of the tags app. However that was not the initial intentions.

- In order to make the app separate, we need to create a new app. We will create the app using `python manage.py startapp store_custom`.
- We are moving the inline class here
  ```python
      class TagInline(GenericTabularInline):
      autocomplete_fields = ['tag']
      model = TaggedItem
      extra = 0
  ```
- Extending the CustomProductAdmin class here
  ```python
  class CustomProductAdmin(ProductAdmin):
      inlines = [TagInline]
  ```
- Now we have to deregister the Product app, as Django admin does not allow to register same model twice. As a result we first de-registering the model and registering it again with `ProductAdmin` app.

  ```python
  admin.site.unregister(Product)
  admin.site.register(Product, CustomProductAdmin)
  ```
