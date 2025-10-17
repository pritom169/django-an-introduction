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

## ViewSets

- A viewset is a class that bundles together the logic for a set of related views (like list, create, retrieve, update, delete) into a single class.
- Instead of manually writing separate views for each HTTP method or operation, you define everything in one place.
- DRF’s routers can then automatically generate the corresponding URL patterns for you.

Let's look at the previous code

```python
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error' : 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

has been converted into

```python
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error' : 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

What was happening before

- ProductList(ListCreateAPIView) handled:
  - GET /products/ → list all products
  - POST /products/ → create a product
- ProductDetail(RetrieveUpdateDestroyAPIView) handled:
  - GET /products/{pk}/ → retrieve one product
  - PUT /products/{pk}/ / PATCH → update
  - DELETE /products/{pk}/ → delete

Each view had its own class and URL path.

Now we combined all those endpoints into a single class.
A ModelViewSet automatically includes:

- list (GET all)
- retrieve (GET one)
- create (POST)
- update (PUT)
- partial_update (PATCH)
- destroy (DELETE)

### Routers

In Django REST Framework, a router is a helper that automatically generates URL patterns for your viewsets.

```python
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
]
```

This is fine, but once you move to ViewSets, each viewset can handle multiple actions (list, retrieve, create, update, destroy). If you don’t use a router, you’d still need to manually wire up URLs for each of those actions.

On the other hand, A router inspects your ViewSet and automatically creates the standard RESTful routes for you.

```python
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet

router = SimpleRouter()
router.register('products', ProductViewSet)

urlpatterns = router.urls
```

From just this, DRF generates:

- GET /products/ → list
- POST /products/ → create
- GET /products/{pk}/ → retrieve
- PUT /products/{pk}/ → update
- PATCH /products/{pk}/ → partial update
- DELETE /products/{pk}/ → destroy

### Manual Delete to Viewset DELETE

```python
def destroy(self, request, *args, **kwargs):
    if OrderItem.Objects.filter(product_id=kwargs['pk']).count() > 0:
        return Response(
            {'error': 'Product cannot be deleted because it is associated with an order item'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    return super().destroy(request, *args, **kwargs)
```

In the current method:

- You override destroy, not delete. This is the method DRF expects in viewsets when handling DELETE requests.
- Instead of re-implementing object retrieval, you use super().destroy(...), which calls DRF’s default logic:
  - It runs get_object() (which respects queryset, filters, and permissions).
  - Calls perform_destroy(instance) (where custom hooks can be defined).
  - Returns the proper Response automatically.

With the new code

```python
def destroy(self, request, *args, **kwargs):
    if OrderItem.Objects.filter(product_id=kwargs['pk']).count() > 0:
        return Response({'error' : 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return super().destroy(request, *args, **kwargs)
```

- You override destroy, not delete. This is the method DRF expects in viewsets when handling DELETE requests.
- Instead of re-implementing object retrieval, you use super().destroy(...), which calls DRF’s default logic:
  - It runs get_object() (which respects queryset, filters, and permissions).
  - Calls perform_destroy(instance) (where custom hooks can be defined).
  - Returns the proper Response automatically.

## Creating the Review Model

To enable customers to leave reviews for individual products, we need to define a `Review` model.

```python
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
```

After defining the model, generate a new migration and apply it to update the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Nested Routers

Nested routers allow us to define URL patterns that represent hierarchical relationships between resources.

We can install nested-routers with this command.

```bash
pipenv install drf-nested-routers
```

Now let's look at how we are setting up the nested router.

```python
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
```

- `NestedDefaultRouter` - Works like DefaultRouter, but allows you to define routes inside another route.
- `router` - This tells the nested router which "parent" router to attach to.
- `products` - This is the parent prefix. It says: "Nest this router under /products/".
- `lookup=`product`` - This sets the name of the URL parameter for the parent’s primary key. So instead of product_id, it will be called product_pk in kwargs.

```python
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
```

- `reviews` - This is the url prefix. Combined with the parent (products), this gives you routes like:

```python
/products/<product_pk>/reviews/
/products/<product_pk>/reviews/<pk>/
```

- `views.ReviewViewSet` - The viewset that implements the logic for those routes (list, create, retrieve, update, delete).
- `basename='product-reviews'` - Used internally by DRF to name the URL patterns for reverse lookups.
  - It generates names like:
    - product-reviews-list → /products/<product_pk>/reviews/
    - product-reviews-detail → /products/<product_pk>/reviews/<pk>/

### Getting a Nested Object

To retrieve reviews for a specific product (e.g., `GET /products/2/reviews`), we rely on the `product_pk` parameter provided by the nested router (`products_router.register('reviews', ...)`).

```python
def get_queryset(self):
    return Review.objects.filter(product_id=self.kwargs['product_pk'])
```

### Creating a Nested Object

```python
def create(self, validated_data):
    product_id = self.context['product_id']
    return Review.objects.create(product_id=product_id, **validated_data)
```

This runs when you submit a `POST` request to create a new review. The ReviewViewSet calls the serializer’s .save(), which internally calls `create()`. Since the request body doesn’t have the product_id (you don’t want the client to send it manually), you pull it from the context (injected when serializer is initialized by the view).

Example:

```python
{
  "name": "John",
  "description": "Great product!"
}
```

`create` adds `product_id=2` from `context` and creates:

```python
Review.objects.create(product_id=2, name="John", description="Great product!")
```

## Generic Filtering

Filtering by collection works, but extending filtering logic for multiple fields can quickly become complex.

To handle this more efficiently, we use the third-party library `django-filter`, which provides a flexible and powerful way to filter querysets by any model field.

First, install the package:

```bash
pipenv install django-filter
```

Next, add `django_filters` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    "django_filters"
]
```

### Implementation

First, replace any custom querysets with the default:

```python
queryset = Product.objects.all()
```

Next, enable filtering support by specifying the backend and fields to filter on:

```python
filter_backends = [DjangoFilterBackend]
filterset_fields = ['collection_id']
```

### Custom Filtering

For more advanced scenarios—such as filtering by both collection and a range of prices—we can define a custom filter set.

Create a new `filters.py` file:

```python
from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['lt', 'gt']
        }
```

Then, update `views.py` by replacing the simple `filterset_fields` configuration with the custom filter class:

```python
filterset_class = ProductFilter
```

### Searching

Django REST Framework provides a `SearchFilter` backend for implementing simple text-based search functionality.

```python
# 1. Import the SearchFilter
from rest_framework.filters import SearchFilter

# 2. Add the filter backend and define searchable fields in ProductViewSet
class ProductViewSet(ModelViewSet):
    # Existing configuration...
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
```

With this setup, clients can perform searches across the specified fields (e.g., `title` and `description`) using query parameters such as:

```
/products/?search=clothing
```

This will return all products whose title or description contains the term "clothing".

### Sorting

Django REST Framework provides the `OrderingFilter` backend to enable flexible sorting of query results.

```python
# 1. Import the OrderingFilter alongside other filters
from rest_framework.filters import SearchFilter, OrderingFilter

# 2. Add OrderingFilter to the filter_backends in ProductViewSet
class ProductViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # 3. Define which fields can be used for ordering
    ordering_fields = ['unit_price', 'last_update']
```

With this configuration, clients can sort results dynamically by appending an `ordering` parameter to the query string. For example:

- `/products/?ordering=unit_price` → Orders products by price (ascending).
- `/products/?ordering=-unit_price` → Orders products by price (descending).
- `/products/?ordering=last_update` → Orders products by the last update timestamp.

### Pagination

Pagination helps improve performance and usability by splitting large result sets into smaller, more manageable pages.

#### Configuration

First, configure the default page size in `settings.py`:

```python
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'PAGE_SIZE': 10
}
```

#### Enabling Pagination in a ViewSet

Next, import and apply a pagination class in your view. For example:

```python
from rest_framework.pagination import PageNumberPagination

class ProductViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
```

This setup enables page-number-based pagination for product listings, with 10 results per page by default.

#### Enabling Global Pagination

To apply pagination across all API endpoints by default, configure it globally in `settings.py`:

```python
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

This ensures that all viewsets automatically use page-number-based pagination with a default page size of 10, unless explicitly overridden.

#### Defining a Custom Pagination Class

While enabling global pagination provides a consistent baseline, you may want more control over pagination behavior (e.g., setting page size or customizing query parameters).  
To achieve this, define a custom pagination class:

```python
from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 10
```

This custom class specifies a default `page_size` of 10 items per page.  
Once defined, you can import and apply it in your viewsets by replacing the built-in `PageNumberPagination` with your custom `DefaultPagination`.

### Creating a Cart API

Now let's do an exercise which will put our skills to practice. Let's create the following APIs.

```
# 1. Creating a cart
POST /carts/

When we will create a cart object, we don't need to send anything in the body, as user can put products into cart without logging in.

If we send a POST request to this endpoint, we will get a CART Object back. The cart object will have a unique identifier for subsequent request. So when an user adds an item to the cart, we will send the cart Id back to the server.

# 2. Getting a cart
GET /carts/:id

We get a cart by ID

# 3. Deleting a cart
DELETE /carts/:id

For deleting a cart, we will send a request to this endpoint.

# 4. Adding an Item
POST /carts/:id/items

When we want to add an item to the cart, we put {prodId, qty} in the body as cart id is already present in the url. It will also have a unique identifier which we will use for subsequent request.

# 5. Updating an Item
PATCH /carts/:id/items/:id

The last id in the parameter is the ID of the cart item. Since we are using this API to change the only the product quantity, we will only send the {qty} in the body

# 6. DELETING an ITEM
DELETE /carts/:id/items/:id
```

### Using UUID for CartID

Using a simple numeric Cart ID can be insecure, as it makes it easier for malicious users to guess or manipulate IDs to access or modify other users’ carts.

To mitigate this, we use a UUID (Universally Unique Identifier) as the primary key for the Cart model. UUIDs are practically impossible to guess, providing stronger protection against unauthorized access.

```python
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Enforcing Product Uniqueness in a Cart

cart should not contain duplicate entries of the same product. If a user attempts to add an identical product more than once, the API should return an error. Instead of creating duplicate entries, users should only be able to update the quantity of an existing product in the cart.

This constraint is enforced at the database level by defining a composite uniqueness rule on the cart and product fields:

```python
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]
```

### Creation of a Cart

#### CartViewSet defines the endpoint

```python
class CartViewSet(CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
```

- This registers an API endpoint (e.g. /store/carts/).
- Because we don't need list, we only want to create a cart hence we are utilizing CreateModelMixin.
- When a client sends POST /store/carts/, DRF looks at serializer_class → CartSerializer to handle validation and representation.

#### CartSerializer defines the data representation

```python
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id']
```

- This defines an endpoint for carts using DRF's GenericViewSet.
- It exposes only the id field, which is a UUIDField.
- Since id will be generated by DRF, we have to make the id a `read_only` field.

#### Adding Product description

Currently, the cart API only returns the product ID for each cart item. To provide more meaningful information, we should also include product details such as description.

This can be achieved by nesting the `ProductSerializer` within the `CartItemSerializer`.

Here’s the updated implementation:

```python
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']
```

By nesting serializers, each cart item will now include detailed product information alongside its quantity.

At this point, our `CartViewSet` only supports cart creation (`CreateModelMixin`). To allow clients to retrieve a cart by its ID (e.g., `GET /store/carts/<uuid>/`), we need to include the `RetrieveModelMixin`.

```python
class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
```

#### Streamlining the Product Response

The current product response includes more details than may be necessary in certain contexts. To optimize the response payload and improve clarity, we can create a simplified serializer exposing only the most relevant fields.

Here’s the implementation:

```python
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']
```

Now we replace Product with `SimpleProductSerializer`

```python
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
```

By using `SimpleProductSerializer` within `CartItemSerializer`, each cart item now references a lightweight product representation that includes only the essential fields (`id`, `title`, and `unit_price`).

#### Calculating the Total Price of a Cart Item

To provide a more informative response, we can include a computed field that returns the total price of each cart item (quantity × unit price). This can be achieved using a `SerializerMethodField`.

```python
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
```

With this addition, each cart item now includes a `total_price` field, giving clients immediate visibility into the cost of that item without requiring manual calculation.

#### Calculating the Total Price of a Cart

To calculate the total price of a cart, we aggregate the total prices of all items it contains.

```python
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
```

This ensures that the cart response includes a `total_price` field representing the combined cost of all items, providing users with an immediate overview of their cart’s value.

#### Optimizing the N+1 Query Problem When Fetching Carts and Related Data

When using a basic queryset such as `queryset = Cart.objects.all()`, the following occurs:

- The initial query retrieves all cart records from the database.
- Accessing `cart.items` (the related `CartItem` records) triggers a separate query for each cart.
- For each `CartItem`, accessing the related `Product` results in yet another query.
- This pattern leads to what is commonly known as the **N+1 query problem**.

For example:

```sql
SELECT * FROM store_cart;                  -- 1 query
SELECT * FROM store_cartitem WHERE cart_id=1;  -- 1 query per cart
SELECT * FROM store_product WHERE id=5;       -- 1 query per item
```

We can address this inefficiency by using `prefetch_related`:

- This instructs Django to fetch all carts, their items, and the related products in advance.
- Django executes a small number of queries up front and efficiently associates the results in memory.
- As a result, accessing `cart.items` or `cart.items[0].product` does not trigger additional database queries.

This approach reduces the number of queries to just three, regardless of the number of carts or items:

```sql
SELECT * FROM store_cart;                           -- all carts
SELECT * FROM store_cartitem WHERE cart_id IN (...); -- all items for those carts
SELECT * FROM store_product WHERE id IN (...);       -- all products for those items
```

### Enabling Cart Deletion

To support cart deletion, we extend the `CartViewSet` with the `DestroyModelMixin`. This enables handling of `DELETE` requests at the `/carts/<uuid>/` endpoint, allowing clients to remove an existing cart.

### Viewing Items Within a Cart

To allow clients to view the list of items associated with a specific cart, we define a nested route for cart items.

We begin by creating a dedicated `CartItemViewSet` that uses the `CartItemSerializer`.

```python
class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
```

Next, we configure the nested routes as follows:

```python
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')
```

### Adding a Cart

Now when we want to add a cart item and we have to perform a POST request to this url "http://localhost:8000/store/carts/<cart-id>/items/"

If we want to save an item to the Cart just using product id and quantity, we have to create another Serializer.

The name of the serializer will be AddCartItemSerializer.

```python
class AddCartItemSerializer(serializers.ModelSerializer):
    # 1. For Identifying product_id we need to expose the product_id field for input.
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        ## 2. Since the input field does not contain the cart_id, we have to extract it from the url. The `get_serializer_context`, we must pass the `cart_id`
        cart_id = self.context['cart_id']

        # 3. From the parameters in the body we will collect the product_id and quantity
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        # 4. Then we would try to see if the CartItem with the product_id and cart_id exists or not.

        # 4a. If it exists we will increase the quantity
        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
            # 4b. If the product does not exist, we will create a cart item with new data
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
```

Now we will add the this functionality, which passes the cart_pk to the Serializer.

```python
def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
```

#### Controlling unwanted situations

With the current implementation, if we add a `product_id` that does not exist the app breaks. That should not be the case. The user should be notified with proper message. In order to make it a reality, we will add the following function into the Serializer class.

```python
def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with given Id was found.')
        return value
```

#### Updating a Cart Item

To update a cart item, we create a dedicated serializer that allows modification of the `quantity` field.

```python
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
```

We then configure the view to use this serializer when handling `PATCH` requests.

```python
def get_serializer_class(self):
    if self.request.method == 'POST':
        return AddCartItemSerializer
    elif self.request.method == 'PATCH':
        return UpdateCartItemSerializer
    return CartItemSerializer
```

# Django Authentication

Every Django App comes with django authentication prebuilt. Now let's talk about Middlewares. In settings.py inside **MIDDLEWARE** array we can see a list of middlewares. When a request arrives, it goes through every middleware sequentially. If one middleware does not reply, it goes just to the next middleware.

## Restructuring the project

### Renaming the Application

To improve clarity and organization, we will restructure the project by consolidating shared functionality into a dedicated application named core.

#### Updating the App Configuration

```python
# core/apps.py
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
```

#### Updating Installed Applications

After renaming the app, update the INSTALLED_APPS in settings.py. Replace the previous store_custom entry with core:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "playground",
    "debug_toolbar",
    "django_filters",
    "store",
    "tags",
    "likes",
    "core"
]
```

### Customizing User Model

Django provides the `AbstractUser` base class, which includes all the fields and functionality of the default user model (e.g., `username`, `password`, `first_name`, `last_name`, etc.). By extending `AbstractUser`, you retain all built-in authentication features while being able to override or add fields as needed.

In the example below, the `email` field is redefined with `unique=True`. Although `AbstractUser` already includes an `email` field, it is not unique by default. Redefining it ensures that each user must have a distinct email address, making it suitable for authentication and preventing duplicate accounts.

```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
```

### Defining Custom User Model

When you define a custom user model, you should also tell Django to use it in your settings.py:

```python
AUTH_USER_MODEL = "core.User"
```

### Importing the User Model Correctly

When defining a foreign key to the user model, avoid referencing `User` directly. Doing so can cause migration issues if your project uses a custom user model instead of Django’s default.

❌ Incorrect (direct reference to `User`):

```python
user = models.ForeignKey(User, on_delete=models.CASCADE)
```

✅ Correct (dynamic reference to the active user model):

```python
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

By using `settings.AUTH_USER_MODEL`, Django always points to the currently active user model — whether it is the default `auth.User` or a custom model defined in your project (e.g., `AUTH_USER_MODEL = "core.User"`).  
This approach ensures consistency, portability, and future-proofing of your codebase.

### Creating a New Database

The initial migration of the admin app is tied to the default user model. Once a custom user model is introduced, it cannot simply replace the existing user model mid-project.

To resolve this, we have two options:

1. **Drop and recreate the existing database** – removing all previous data and applying migrations from scratch.
2. **Create a new database** – and apply the migrations there.

Both approaches ensure that the schema is rebuilt cleanly with the custom user model in place.

### Extending UserAdmin

By default, Django’s `BaseUserAdmin` class only displays the `username` and password fields (`password1`, `password2`) when creating a new user in the admin interface.

To provide a more complete user creation form, we can extend `BaseUserAdmin` to include additional fields such as `email`, `first_name`, and `last_name`:

```python
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )
```

This customization ensures that when administrators create new users, they can capture both login credentials and essential profile details in a single step.

### Connecting the User Model with Customer

To associate each customer with exactly one user account, we define a one-to-one relationship between the `Customer` model and the active user model.

`settings.AUTH_USER_MODEL` ensures that the relationship dynamically references whichever user model is configured in the project (either the default `auth.User` or a custom implementation).

```python
user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

With `on_delete=models.CASCADE`, deleting a user will automatically remove the associated customer record, maintaining data consistency.

### Removing Redundant Fields

Because the Customer model already has a one-to-one relationship with the User model, certain fields are unnecessary. Specifically, first_name, last_name, and email can be removed from the Customer model since they are already provided by the User model.

### Incorporating User Fields into Customer

Now in the customer model, we have to refer to the `first_name` and `last_name` from the user. We have to incorporate them in the following code as well.

```python
def __str__(self):
    return f'{self.user.first_name} {self.user.last_name}'

class Meta:
    db_table = 'store_customers'
    ordering = ['user__first_name', 'user__last_name']
```

- The **str** method defines the string representation of a Customer instance. Here, it concatenates the first and last name of the related User object. This makes Customer entries more meaningful when displayed in the Django admin interface or console, showing "John Doe" instead of a generic "Customer object (1)".
  - The Meta class provides configuration for the model:
  - db_table = 'store_customers' explicitly sets the database table name.
- ordering = ['user__first_name', 'user__last_name'] ensures that query results are automatically sorted alphabetically by the related user’s first name and then last name.

### Making Queries a bit efficient

The `list_select_related` option optimizes database queries in the Django Admin by performing a SQL JOIN to fetch related `User` objects in the same query as `Customer` objects.  
Without this optimization, displaying 100 customers would trigger an additional 100 queries to fetch each related user.  
With `list_select_related = ['user']`, both `Customer` and `User` data are retrieved in a single query, significantly improving performance.

### Incorporating User Fields in Admin Configuration

To ensure consistency and avoid redundant data, we now reference the `first_name` and `last_name` fields directly from the related `User` model instead of duplicating them in the `Customer` model.

```python
ordering = ['user__first_name', 'user__last_name']
search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']
```

- `ordering` ensures that customer records are sorted alphabetically by the associated user’s first and last name.
- `search_fields` enables efficient search functionality in the Django admin by allowing case-insensitive queries that match the beginning of the user’s first or last name.

### Incorporating name fields into CustomerAdmin

As right now, `first_name` and `last_name` does not exist in the Customer. So we have to create custom function which fetches `first_name` and `last_name` from the user.

```python
def first_name(self, customer):
    return customer.user.first_name

def last_name(self, customer):
    return customer.user.last_name
```

## Migrating from Customer to Core User

```python
user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

This ensures that each customer is associated with a single user account, and the field is non-nullable (null=False by default).

Since the store_customers table already contains existing records, Django requires a value for the new user field in these rows. For this migration, all existing customers are assigned the user with ID 1.

> Summary: A new user field is added to the Customer table, and existing rows are updated to reference user ID 1.

### Addition of Sorting in the Store Admin

To enable sorting of customers by their associated user’s first and last names in the Django admin interface, we define the following methods:

```python
@admin.display(ordering='user__first_name')
def first_name(self, customer):
    return customer.user.first_name

@admin.display(ordering='user__last_name')
def last_name(self, customer):
    return customer.user.last_name
```

## Authentication

Django includes a built-in authentication system that manages users, passwords, and permissions. However, it does not provide an API interface out of the box.

Djoser is a RESTful implementation of Django’s authentication system. It exposes ready-to-use API endpoints for essential authentication tasks such as user registration, login, password reset, and account management, making it easy to integrate secure user authentication into Django REST Framework–based projects.

### Authentication Token vs JWT based token

In Django REST Framework, authentication can be handled either through simple authentication tokens or through JSON Web Tokens (JWT). A standard authentication token (used by DRF’s TokenAuthentication) is a randomly generated string stored in the database. When a user logs in, the server creates this token and saves it in a dedicated table (authtoken_token). For each subsequent request, the client sends the token in the header (e.g., Authorization: Token <token>), and the server looks it up in the database to identify the user. This method is easy to implement and ideal for small or internal projects, but it requires a database lookup on every request and does not scale efficiently across multiple servers.

JWT-based authentication, on the other hand, is stateless and self-contained. Instead of storing tokens in the database, the server generates a signed JWT containing user information such as the user ID and token expiration time. Clients then include this token in each request (e.g., Authorization: Bearer <jwt>), and the server verifies it using a secret key—no database lookup is needed. This makes JWTs much more scalable and efficient for distributed systems. However, JWTs are harder to revoke once issued, as they remain valid until they expire, making token invalidation slightly more complex.

### Installing JWT for Django

To enable JWT-based authentication in Django, first ensure that **Djoser** is installed and registered in your project’s `INSTALLED_APPS` list.

```python
INSTALLED_APPS = [
    ...
    "djoser",
    ...
]
```

Next, configure the authentication endpoints by including Djoser’s URL patterns in your main `urls.py` file. This setup provides access to standard authentication routes (for registration, login, logout, etc.) as well as JWT-specific endpoints for token management.

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("playground/", include("playground.urls")),
    path("store/", include("store.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
] + debug_toolbar_urls()
```

### Password Validators

When making a `POST` request with the following data:

```json
{
  "email": "hello@gmail.com",
  "username": "hellogmail",
  "password": "12345678"
}
```

the API returns the following validation response:

```json
{
  "password": [
    "This password is too common.",
    "This password is entirely numeric."
  ]
}
```

This occurs because Django enforces password security rules defined in the `AUTH_PASSWORD_VALIDATORS` setting within `settings.py`:

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
```

Each validator enforces a specific password policy to improve account security:

- **`UserAttributeSimilarityValidator`** – Prevents the use of passwords that closely resemble the user’s personal attributes, such as their username, email, or name.
- **`MinimumLengthValidator`** – Ensures that passwords meet a minimum length requirement (default: 8 characters). You can adjust this rule by specifying an option, for example:

  ```python
  {
      "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
      "OPTIONS": {"min_length": 10}
  }
  ```

- **`CommonPasswordValidator`** – Rejects passwords that are too common or appear in lists of easily guessable passwords (e.g., “password123”, “qwerty”).
- **`NumericPasswordValidator`** – Disallows passwords composed entirely of numbers, such as “12345678”.

Together, these validators ensure that user passwords follow best practices for complexity and uniqueness, reducing the risk of weak or easily compromised credentials.

### Capturing Additional Fields During User Registration

By default, Djoser allows users to register with only an email, username, and password. However, in many cases, it’s desirable to collect additional user details—such as the first and last name—during registration.

To achieve this, we extend Djoser’s built-in serializer, which handles both serialization and deserialization of user data. Because this customization is specific to our project, we will define it within a new file named `serializers.py`.

```python
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
```

Here, we override the `Meta` class from Djoser’s `UserCreateSerializer` to include the `first_name` and `last_name` fields. Overriding the `Meta` class directly ensures that our implementation remains compatible with future updates to Djoser’s core serializer.

Once the custom serializer is defined, it must be registered in the project’s settings file so that Djoser uses it instead of the default serializer:

```python
DJOSER = {
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer'
    }
}
```

With this configuration, new users can now provide their first and last names during registration, allowing for a more complete user profile upon account creation.

### Customer Account Creation Endpoint

#### 1\. Serializer Definition

The first step is to define a serializer that will handle the data validation and conversion for the `Customer` model.

The `CustomerSerializer` is designed specifically for this purpose. It includes all necessary fields from the `Customer` model and an additional `user_id` field to associate the customer profile with a user account.

```python
# serializers.py

from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model. It handles the creation and representation
    of customer data.
    """
    # The user_id is explicitly included to accept the ID of the related user
    # during the creation process, as the User object itself is not part of the
    # Customer model's direct fields.
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
```

---

#### 2\. ViewSet Implementation

Next, we implement the `CustomerViewSet` to define the API logic. Instead of using the full `ModelViewSet`, we selectively inherit from specific mixins (`CreateModelMixin`, `RetrieveModelMixin`, `UpdateModelMixin`) and `GenericViewSet`.

This approach intentionally **disables the list endpoint** (i.e., `GET /customers/`), preventing unauthorized users from viewing a complete list of all customers while still providing endpoints to create, retrieve, and update individual customer instances.

```python
# views.py

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """
    A viewset for creating, viewing, and updating customer profiles.

    This viewset explicitly excludes the 'list' action to prevent exposure
    of all customer data.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
```

---

#### 3\. URL Configuration

Finally, we register the `CustomerViewSet` with the Django REST Framework's router in the `urls.py` file. The router automatically generates the necessary URL patterns for the actions enabled in the viewset.

Following RESTful conventions, the endpoint is registered as `customers`.

```python
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
```

### Logging In

Unlike Token-Based Authentication, which requires a database lookup for each request, JWT (JSON Web Token) authentication enables stateless login — no database call is needed during authentication.

To authenticate using JWT, send a POST request to `{baseurl}/jwt/token` with your username and password. A successful login returns both an `access` token and a `refresh` token:

```python
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```

- The `access` token is used to authenticate requests to protected API endpoints. It is short-lived and typically expires after **5 minutes**.
- When the `access` token expires, the `refresh` token — valid for **24 hours** by default — can be used to obtain a new one without re-entering credentials.

For detailed configuration options, refer to the [Django REST Framework SimpleJWT documentation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html).

#### Customizing the Lifetime of JWT Tokens

By default, the JWT access token expires after 5 minutes. However, during development, it can be useful to extend this duration to simplify testing.  
For example, the following configuration sets the access token lifetime to 1 day:

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1)
}
```

## Dimistifying JSON Web Token

To learn more about JSON Web Token hop into [jwt.io](jwt.io).

## Refreshing tokens

When accessing a protected API, clients must include a valid access token with their request. If the access token has expired, the server will return a 401 Unauthorized response.

In this case, the client can obtain a new access token by calling the refresh endpoint and providing the existing refresh token.

To refresh the token, send a POST request to:

```python
<base_url>/auth/jwt/refresh/
```

This endpoint returns a new access token, allowing continued access without requiring the user to log in again.

### Retrieve the current user

To retrieve information about the currently authenticated user, include the access token in the request header. This can be done using a browser extension such as ModHeader.

1. Add an Authorization Header

- Header Name: Authorization
- Header Value: JWT {access_token}

2. Access the User Endpoint

Once the header is configured, send a request to:

```
http://localhost:8080/auth/users/me/
```

### Retrieving Additional User Information

By default, when accessing the **{base_url}/auth/users/me/** endpoint, only basic user details are returned. To include additional fields such as the user’s first and last name, we can extend Djoser’s built-in UserSerializer.

The custom serializer below overrides the default implementation to include these additional attributes:

```python
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
```

After Creating the serializer we have to add it to `settings.py`

```python
DJOSER = {
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer',
        'current_user': 'core.serializers.UserSerializer'
    }
}
```

### Getting Current User's Profile

```python
MIDDLEWARE = [
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]
```

If we look at the `settings.py` of storefront app we will see the authentication middleware. It will look at the request and if there is a matching user, it will attach the user object to the request.

```python
    @action(detail=False)
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
```

In the code when we write `@action(detail=False)`, it means the custom route does not require an object ID (like /customers/3/). So the URL will look like:

```python
{base_url}/store/customers/me/
```

The serializer is determining how the response will look like and finally returning the data.

#### Changing the User Profile Data

Updating user profile information is performed through a PUT request. The following method conditionally handles both retrieval and update operations for the currently authenticated user:

```python
def me(self, request):
    customer, created = Customer.objects.get_or_create(user_id=request.user.id)
    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

- `serializer = CustomerSerializer(customer, data=request.data)` — Initializes a serializer instance with the existing customer object and incoming request data for update validation.
- `serializer.is_valid(raise_exception=True)` — Validates the input data; raises a `ValidationError` if invalid.
- `serializer.save()` — Persists the validated data to the database using the serializer’s internal `.update()` method.
- After saving, the updated customer data is re-serialized and returned as a JSON response.
