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

## Installing Django REST Framework

In order to install the REST framework we must first install

```bash
pip install djangorestframework
```

Next, register it in the `INSTALLED_APPS` section of your `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "rest_framework",
    ...
]
```

## Creating API Views

### API Views using HttpRequest and HttpResponse

- First we need to create a function inside the `store/views.py` as it will be responsible when an API endpoint hits the browser URL.

```python
def product_list(request):
    return HttpResponse('ok')
```

Now we want to the function discoverable, and we can do it inside `store/urls.py` file

```python
urlpatterns = [
    path('products/', views.product_list)
]
```

Now we have to make the `urls.py` discoverable to the main urls.py

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path('playground/', include('playground.urls')),
    path('store/', include('store.urls'))
] + debug_toolbar_urls()
```

### API Views using Django Rest Framework

Now we will use Django Rest Framework to check the API endpoints as it is more powerful and much easier to use. In order to do that we need do it in a couple of steps.

```python
### 1. Import decorators and responses
from rest_framework.decorators import api_view
from rest_framework.response import Response

### 2. Add decorator on the top
@api_view()

### 3. Replace HttpResponse with just Response
def product_list(request):
    return Response('ok')
```

#### Taking a Parameter in the URL

Now let's write a function where an ID parameter will be taken in the URL as Parameter. Inside, `url.py`, we are will add the parameter inside `<>`

```python
path('products/<id>/', views.product_detail)
```

Once it is done, we add the function inside the views.py

```python
@api_view()
def product_detail(request, id):
    return Response(id)
```

However even though our product id should be in integer format, right now it accepts every format. However, we can limit them by adding the type in front of the parameter.

```python
path('products/<int:id>/', views.product_detail)
```

## Serializers

In Django REST Framework, serializers are used to convert complex data types (like Django models or querysets) into native Python data types (dicts, lists) that can then be easily rendered into formats like JSON or XML for APIs.

### Writing a serializer class

Within the `store` app, create a `serializers.py` file. In this file, we define serializer classes by specifying the fields we want to expose, similar to how fields are declared in Django models.  
Here is an example implementation for the `Product` serializer:

```python
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
```

### Decimal to string (DRF) conversion

Now if we hit the `/store/product/1/` endpoint we will see the following response

```
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "title": "Bread Ww Cluster",
    "unit_price": "4.00"
}
```

We can see the unit_price in string format. However, in order to convert it in floating points, we have to add the following code inside the settings.py

```python
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False
}
```

Without that setting, unit_price would show up as "12.50" (string). With it, you get 12.50 (numeric).

### Exception Handling

When fetching a product by ID, the object may not exist, which would normally raise an error.  
To handle this gracefully, wrap the query in a `try/except` block and return a proper HTTP 404 response.

```python
from rest_framework import status

try:
    product = Product.objects.get(pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
except Product.DoesNotExist:
    return Response({"detail": "Product not found."}, status=404)
```

### Using Proper HTTP Status Codes

Previously, the error response used a hard-coded value. Instead, we should leverage the standard HTTP status codes provided by Django REST Framework for clarity and maintainability.

```python
# 1. Import standard HTTP status codes
from rest_framework import status

# 2. Use the appropriate status code in the exception handler
except Product.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
```

### Replacing `try/except` with `get_object_or_404`

The previous implementation using `try/except` was more verbose.  
Django REST Framework provides the `get_object_or_404` shortcut, which simplifies the code by automatically raising a `404 Not Found` error when the object does not exist.

```python
from django.shortcuts import get_object_or_404

product = get_object_or_404(Product, pk=id)
serializer = ProductSerializer(product)
return Response(serializer.data)
```
