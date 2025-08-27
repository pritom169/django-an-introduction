## Project Setup

### 1) Cloned `django-part1` → `django-part2`

```bash
# from the parent folder
rsync -a --exclude ".venv" --exclude "venv" --exclude "__pycache__" \
  --exclude "*.pyc" --exclude ".mypy_cache" --exclude ".pytest_cache" \
  --exclude ".DS_Store" --exclude "node_modules" --exclude ".idea" --exclude ".vscode" \
  django-part1/ django-part2/
```

### 2) Cleaned state in django-part2

```bash
cd django-part2
rm -f db.sqlite3
find . -name "__pycache__" -type d -prune -exec rm -rf {} +
find . -path "*/migrations/*.py" ! -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
```

### 3) New virtualenv + installed deps

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip wheel setuptools
# Otherwise, at minimum:
python -m pip install "Django>=4.2,<6"
```

### 4) Fixed missing packages as errors popped up

For running the project in a successful manner, we also need to install django-debug-toolbar

```bash
python -m pip install django-debug-toolbar
```

### 5) Pointed Django to a new DB (storefront2)

```bash
# settings.py
DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "storefront2",
    "HOST": "localhost",
    "USER": "", ## The username of yours
    "PASSWORD": "", ## The password you had set
    "PORT": 5432,
  }
}
```

### 6) Created the DB in Postgres

```sql
CREATE DATABASE storefront2;
```

### 7) Applied schema to the new DB

```sql
source .venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### 8) Created admin user + ran the server (to verify /admin/)

```python
python manage.py createsuperuser
python manage.py runserver
```

### 9) Verified connection / migrations

```python
python manage.py dbshell      # prompt should be: storefront2=>
\q
python manage.py showmigrations
python manage.py check
```

## REST

REST is an architectural style for designing networked applications. It uses stateless communication (usually HTTP) where everything is modeled as resources. Clients interact with resources using standard HTTP methods (verbs).

### Resources

The key abstractions in REST. Anything that can be identified and addressed on the server can be identified as Resource. Each resource is identified by a URI (URL is one type of URI).

### Resource Representation

The format in which a resource is exchanged between client and server. Common format on which a resources are being represented are `JSON, XML, HTML, and YAML`

### HTTP Methods

- GET – Retrieve a resource (read-only, safe).
- POST – Create a new resource (non-idempotent).
- PUT – Update/replace a resource (idempotent).
- PATCH – Partially update a resource.
- DELETE – Remove a resource.
- HEAD – Same as GET but only headers.
- OPTIONS – Get communication options.

> Idempotent = safe to repeat without changing the outcome.

> A GET request always returns the same resource, no matter how many times you call it.

> PUT /products/42 with { "name": "Laptop" } → Whether you send it once or 10 times, the result is the same: product 42’s name is “Laptop”.

> DELETE /products/42 → First call deletes it. Subsequent calls still leave it deleted → effect is the same.

> POST /products with { "name": "Laptop" } → Each call creates a new resource, so repeating changes the state differently.
