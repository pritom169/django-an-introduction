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

### Querying Multiple Records

So far, we have queried a single record. To fetch multiple records, we can use a queryset and serialize the results with the `many=True` option.

```python
# 1. Retrieve all products from the database
queryset = Product.objects.all()

# 2. Serialize the queryset (note: set `many=True` for multiple objects)
serializer = ProductSerializer(queryset, many=True)

# 3. Return the serialized data as the response
return Response(serializer.data)
```

### Creating Custom Serializer Fields

Sometimes, we may want to include additional computed fields in our serializer.  
Django REST Framework provides `SerializerMethodField` for this purpose.

```python
from decimal import Decimal
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal("1.1")
```

> Note: Always use Decimal instead of floating-point numbers when performing calculations with DecimalField to avoid precision errors.

### Changing the name of the field

Now let's change the field name unit_price to price it will show us an error. By default, Django assumes that a field exits in the model class with same name. In order to change the names properly, we have to set the source to `unit_price`.

```python
price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price")
```

### Using PrimaryKeyRelatedField for a foreign key

A product belongs to exactly one collection (many-to-one). Expose that FK as an integer ID and validate it by providing a queryset:

```python
collection = serializers.PrimaryKeyRelatedField(
    queryset = Collection.objects.all()
)
```

### Using `StringRelatedField` for Foreign Keys

By default, a foreign key field returns the related object’s ID.  
If we want to display the related object’s name (or its `__str__` representation), we can use `StringRelatedField`.

```python
collection = serializers.StringRelatedField()
```

However, this introduces a potential performance issue. When serializing multiple products, each related collection would be queried separately.
To avoid the N+1 query problem, we can optimize the queryset by preloading the related collection using select_related.

```python
def product_list(request):
    queryset = Product.objects.select_related("collection").all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)
```

### Showing nested Object

If we want to show the id and the name of the collection we have to use nested object.

```python
### 1. First we declare another serializer class for it
class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

### 2. We use the object and assign it to collection
class ProductSerializer(serializers.Serializer):
    collection = CollectionSerializer()
```

### Including a Hyperlink in the nested object to see the whole object

First we have to add, HyperlinkRelatedField to the collection property. Inside the parenthesis we have to include the queryset for fetching the collection and the view function that will be executed

```python
collection = serializers.HyperlinkedRelatedField(
    queryset = Collection.objects.all(),
    view_name = 'collection-detail'
)
```

In the `urls.py`, we also have to include the url

```python
urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
    path('collection/<int:pk>/', views.collection_detail, name='collection-detail')
]
```

Now inside the `views.py` we will create the function

```python
@api_view()
def collection_detail(request, pk):
    return Response('ok')
```

### Model Serializers

Let's say we want to change the name of the product title. We have to change it in two places. We can solve this problem using `ModelSerializer`. When your API mirrors a Django model, prefer ModelSerializer. It derives fields from the model and stays in sync with model changes, so you don’t duplicate field definitions.

We first change the `serializers.Serializer` to `serializers.ModelSerializer`. Afterwards, we mention the model class we want to take with the fields from.

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'collection']
```

#### Adding a computed (read-only) field

Now if we want to add price with tax, we need an extra field. Here is how we can do it

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax' ,'collection']
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
```

## Deserializers

Deserializing is actually opposite of serializing. In short, taking incoming data (usually JSON from an HTTP request) and convert it back into Python objects (validated dicts or even Django model instances).

```python
### Previously, we didn't include any request type at the top. But now the same endpoint can server as GET or POST.
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        ### Deserializing the incoming data
        serializer = ProductSerializer(data=request.data)
        return Response('ok')
```

### Validating Deserialized Data

```python
serializer = ProductSerializer(data=request.data)
### Check whether the serialized data is valid or not
if serializer.is_valid():
    serializer.validated_data
    return Response('ok')
else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Validating Deserialized Data (Cleaner Way)

Now we have replaced if else block by adding `(raise_exception=True)`

```python
serializer = ProductSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
serializer.validated_data
return Response
```

### [ISSUE] Id counter fix

The root cause of the IntegrityError: duplicate key value violates unique constraint "store_product_pkey" was that your PostgreSQL database's internal ID counter for the store_product table was out of sync with the actual data in the table.

The database table has 1000 products in that table, but the database was trying to assign a new product a very low ID (like 11 or 12), which was already in use. This happens sometimes if data is imported manually or after a database restore, which can cause the primary key sequence (the ID counter) to not be updated correctly.

#### Fixation

- First we have to perform some dependency resolution. **django-debug-toolbar:** This was required to run some of the Django management commands.
- Used the built-in Django management command sqlsequencereset. For your project, the
  command was `pipenv run python django-part2/manage.py sqlsequencereset store`
- Used the built-in Django management command sqlsequencereset. For the project, the command is: `pipenv run python django-part2/manage.py sqlsequencereset store`. This command generates the necessary SQL to reset the ID counters for all the tables in your store app, based on
  the current data in those tables.
- Applying the Fix: I then executed the generated SQL on your database by piping the output of the previous command to Django's dbshell utility: `pipenv run python django-part2/manage.py sqlsequencereset store | pipenv run python`. This command took the generated SQL and executed it directly on your PostgreSQL database, which reset the ID counter for the store_product table to start after the highest existing ID (1000).

### Creating Product

This method is called when you make a POST request to /store/products/ to create a new product. After the
serializer validates the incoming data, it calls this create method.

```python
def create(self, validated_data):
    # Creates a new Product instance using the validated data from the request.
    product = Product(**validated_data)
    # This line will cause an error. The Product model doesn't have a field
    # named 'other', so trying to set it will raise an AttributeError.
    product.other = 1
    # Saves the new product to the database.
    product.save()
    # Returns the newly created product instance.
    return product
```

### Updating the Product

This method is called when you make a PUT or PATCH request to a product's detail URL (e.g., /store/products/1/) to update an existing product.

```python
def update(self, instance, validated_data):
    # 'instance' is the existing Product object that needs updating.
    # This line gets the 'unit_price' from the validated request data
    # and updates the product's unit_price with it.
    instance.unit_price = validated_data.get('unit_price')

    # Saves the changes to the database.
    instance.save()

    # Returns the updated product instance.
    return instance
```

## Class-based Views

We can refactor our function-based API views into class-based views for improved readability, maintainability, and scalability. Each HTTP method (GET, POST, PUT, DELETE) is implemented as a dedicated method (get, post, put, delete) within the class.

```python
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'error' : 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

    def get_serializer_context(self):

## Mixins

Mixins is a pattern of data that encapsulates some pattern of codes.

## Generic Views

Most of the time we are not going to use a mixin, however we are going to use a combination of mixin aka Generic Views.

Let's look at these block of codes.

```python
def get(self, request):
    queryset = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

def post(self, request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
```

They can be replaced with the following querysets.

```python
def get_queryset(self):
    return Product.objects.select_related('collection').all()

def get_serializer(self, *args, **kwargs):
    return ProductSerializer()

def get_serializer_context(self):
    return {'request': self.request}
```

- get_queryset() → replaces the explicit queryset = Product.objects... in get().
  - DRF will automatically use this queryset for listing objects.
- get_serializer() → replaces the explicit serializer = ProductSerializer(...) calls.

  - Normally you don’t override this unless you want special behavior.
  - In your code, it’s incomplete (return ProductSerializer() should pass \*args, \*\*kwargs), but the idea is to centralize serializer creation.

- get_serializer_context() → replaces manually passing context={'request': request}.
  - DRF will automatically add this context to every serializer it creates.

So:

- With manual get() / post(), you explicitly define how data is fetched, serialized, and returned.
- With get_queryset() + get_serializer_context(), you just provide the pieces, and ListCreateAPIView automatically wires them into its built-in get() and post() logic.

### Replacing methods with Class attributes

#### Class attributes

```python
queryset = Product.objects.select_related('collection').all()
serializer_class = ProductSerializer
```

- These are the default values for the view.

- DRF’s ListCreateAPIView will automatically look for queryset and serializer_class at the class level if you don’t override get_queryset() or get_serializer().

- So you don’t need to write those methods unless you want something dynamic.

#### Methods

```python
def get_queryset(self):
    return Product.objects.select_related('collection').all()

def get_serializer(self, *args, **kwargs):
    return ProductSerializer()
```

- These are hooks that override the defaults.

- get_queryset() is used if the queryset needs to change (e.g., filter by request.user).

- get_serializer() is used if you need custom serializer instantiation (though normally you override get_serializer_class() instead).

### Benefits of Generic Views

Open the browser and navigate to `http://localhost:8000/store/products/`. All the previously implemented functionalities remain available.

Additionally, the interface now provides extra features. At the bottom of the page, you can find input fields for Title, Description, Slug, Inventory, Unit Price, and Collection. If preferred, you can switch to the "Raw Data" view to input data directly in JSON format. It is an extra benefit one gets for using Generics.

#### Adding Product Count to Collection

##### Product model reverse corelation

In the new ProductModel

```python
class Product(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name="products"
    )
```

- This makes the reverse relation from Collection → Product accessible as collection.products.
- Without related_name, Django would have called this product_set.

##### The queryset with annotation

In the CollectionList:

```python
queryset = Collection.objects.annotate(products_count=Count('products')).all()
```

- Count('products') uses the reverse relation defined by related_name="products".
- For every Collection row, Django adds a calculated field called products_count, which is the number of products linked to that collection.
- The .annotate() ensures this value is available as part of each Collection object in the queryset.

##### The serializer

In CollectionSerializer:

```python
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField()
```

#### Read Only Fields

There is one small issue with the current implementation. Now in order to add a collection, we also have to input `products_count`. However that `products_count` is a computed field which should not be manually entered.

We can eliminate the following issue just by adding read_only in the computed_field.

```python
products_count = serializers.IntegerField(read_only=True)
```

### Customizing Generic Views

Now generic views provides some default feature which may not be enough sometimes. As a result we need to use `RetrieveUpdateDestroyAPIView` to do some custom operation.

### Replacing generic requests with Class Attributes

When using Django REST Framework's generic class-based views, you can simplify your view definitions by specifying class attributes such as `queryset` and `serializer_class`. This approach eliminates the need to explicitly implement methods like `get()` and `put()` when their behavior is standard. The generic views will automatically use these attributes to handle common operations, making your code more concise and maintainable.

#### Before: Explicit Method Implementations

```python
def get(self, request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

def put(self, request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
```

#### After: Using Class Attributes

```python
queryset = Product.objects.all()
serializer_class = ProductSerializer
```

By defining `queryset` and `serializer_class` as class attributes, the generic view classes will handle the standard GET, PUT, and other HTTP methods for you. Override these attributes or provide custom methods only when you need specialized behavior.

#### Replacing primary key

In the URL unless you have a strong reason to change it, because DRF and Django both conventionally expect pk.

```python
path('products/<int:pk>/', views.ProductDetail.as_view()),
```

#### Aligning URL Parameters with View Methods

In the current implementation, the `delete` method uses `id` as a parameter, while the URL pattern expects `pk`. For consistency with Django REST Framework conventions, it is recommended to align both to use `pk`.

```python
def delete(self, request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.orderitems.count() > 0:
        return Response({'error' : 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
```
