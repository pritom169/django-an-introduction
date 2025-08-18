# Django - An Introduction

## 1. Project Setup

### First things first

Let us navigate to the directory and create a virtual environment for the project. Let's type the command

```bash
PIPENV_VENV_IN_PROJECT=1 pipenv install django
```

Here are some descriptions about the command

- It uses Pipenv, a tool that manages Python dependencies and virtual environments, to install the `django` packages into a project.
- The line `PIPENV_VENV_IN_PROJECT=1` tells pipnv, **Rather than using the global shared space create a virtual environment inside the project**

### Create a project

Now coming to the project creation.

```bash
pipenv run django-admin startproject storefront .
```

- `pipenv run django-admin startproject storefront` runs the command inside the pip virtual environemnt
- The `.` at the end tells Django to create the project in the current directory, not a subfolder

### Opening the Shell

Activating the virtual environment we previously created is the standard way to go.

```bash
pipenv shell
```

### Runing the server

If we run the command `django-admin runserver`, it will not run as django-admin does not know which project to run. Instead all the necessary commands needed to run the server are inside the `manage.py` (It was generated when we created the project).

Hence we can run the project using

```bash
python manage.py runserver
```

## Creating an App

In the directory the django project was created, we will type the command

```bash
python manage.py startapp playground
```

It will create an app with playground. Inside the app we can see multiple files. Let's go one by one to describe their responsiblities

1. The `migrations` folder is responsible for generating database tables. More about this in the future section.
2. In the `admin.py` we declare how the admin inteface is going to look like for this app.
3. The `apps.py` is where we configure the app.
4. In the `models.py` we pull out data from the database to show to user.
5. Test module is where we write our tests.
6. Views is responsible for request handler.

## Views

HTML is a request response protocol. These is where we use views in Django. In a nutshell, a view function takes a request and returns a response. More accurately it's request handler.

### Url Configuration

When we want to configure the urls, it should starts with the app. Please note, we don't call the function we just mention the name of it without using '()'

```python
from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('playground/hello', views.say_hello)
]
```

We have declared the URL in the `playground` app. However, the project does not know the route yet. Hence, it order to let it know, we have to add it into the `urls.py` of the main project.

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path('playground/', include('playground.urls'))
]
```

What is essentially tells, django when any request comes with 'playground', navigate it to the urls of playground app.

In django, every url must end with a '/' and since`playground` has already been mentioned into the `urls.py` of the main app.

```python
urlpatterns = [
    path('hello/', views.say_hello)
]
```

## Templates

As we have already known views in django are not views exactly. Templates are the real views in django. Let's create a **templates** folder inside the migrations folder. Let's write `<h1>Hello World!</h1>` inside the folder.

> When rendering a template, the django app looks for the `hello.html` inside the the template folder of the `playground` app. If it's there, it renders it accordingly.

## Django Debug Toolbar

In order to add django-toolbar to VS code project, hop into this [link](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

# 2. Entity Diagram

For more demonstration of django ORM (object relation mapping), we will use an e-commerce app. Please have a look at the ER diagram for more details.

<img src="images-and-diagrams/er-diagram.png" alt="ER Diagram" width="80%">

## Organizing the project

As we already know, a Django project contains different apps. Let's brainstorm a way to organize our application:

1. We can put Product, Collection, Cart, CartItem, Order, OrderItem and Customer into a single app named `Store`. Befits of using this application is using anyone can download the app and install it without any hassle. However, as this app grows it gets bloated with too many models. These phenomenon is called Monolith. At some point our app becomes to hard to incorporate new features and also becomes hard to maintain. Thus, we can do better.

2. We should follow the UNIX philosophy, each app should do one and one thing only. This app is better than the previous one. Let's break the app into couple of different categories. Let's break down the app in the following apps.

   - **Products** (Product, Collection, Tag)
   - **Customers** (Customer) -> Depends on Product
   - **Carts** (Cart, CartItem) -> Depends on Customers and Products
   - **Orders** (Order, OrderItem) -> Depends on Carts and Customers

   > However, it comes with one issue. We have to install in the apps in the following sequence: Product, Customers, Carts and Orders.

   > Another issue we might face, is if we change something in the product, now the Carts and Orders has to be changed accordingly.

As we have see two ideas are completely polarized. If we choose monolith our projects become bloated. If we fine grain our app into many apps it become hard maintain as one app becomes dependent on others. There is a sweat spot if we look carefully. So we should give attention to these two parts:

1. **Minimal Coupling:** Means they should have minimal dependencies between them.

2. **High Cohesion (aka Focus):** A single app should be responsible for one functionality only.

Following the two principles we can divide the app into two apps:

1. Store (Product, Collection, Customer, Cart, CartItem, Order, OrderItem)
2. Tags (Tag, TaggedItem)

Hence, let's go to the terminal and create the two apps via the following command:

```bash
python manage.py startapp store
python manage.py startapp tags
```

One another responsibility comes with installing a new app that we have to include it in the `INSTALLED_APPS` of the root app inside the `settings.py`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "playground",
    "debug_toolbar",
    "store",
    "tags"
]
```

## Models

When creating a model, we put considerations into two details.

1. Field types (comes after calling `models`)
2. Field options (declared inside parenthesis)

Here is the models class for `models.py`

```python
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
```

### Choice Fields

If a schema entity can have a limited choice, we can do that using choices. Inside the choices which only accepts a dictionary. We can also provide a default value. Here is the code for Customer model for more reference.

```python
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True)
    phone = models.IntegerField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
```

### Defining Relationship

#### One to one relationship

Let's consider how we can set up a one-to-one relationship. A customer can only have one address and an address can only be assigned to only one customer. The following code is self explanatory.

```python
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
```

The customer property creates a one-to-one relationship with the CUSTOMER table. One positive thing is that, we don't have to go to the address class and repeat the same code. Django takes care of that.

#### One to many relationship

When setting one-to-many relationship, the entity which is one the end of `many` must have a variable that points to that one table it is pointing to. Look at class Address.

```python
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
```

Here multiple address can be assigned to one customer. If The customer field gets deleted, all the address associated with it, will also should be deleted. Thus we have chosen models.CASCADE. If we don't want to delete them, we should have chosen models.PROTECT.

#### Many to Many relationship

Just like one to one relationship, in many to many relationship we also have to mention the relationship to one class and the rest of the work will be done by django.

Let's look at the class of Product and Promotion. A Product can have multiple promotion and a promotion can have multiple products. Look at the code for more reference

```python
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.‚DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
```

#### Resolving Circular Relationships

For instance, we need a two way relationship within two table. In this project, for example multiple products can point to one collection and multiple collection can point to a single product. It can lead to circular dependencies. Let's look at the code for `Collection` and `Product`:

```python
class Collection(models.Model):
    label = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
```

Let's focus our attention to this line `featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')`.

1. `on_delete=models.SET_NULL` means if the corresponding product is deleted, set this field to NULL.
2. `null=True` allows the featured_product to be optional. (It can be NULL in the database).
3. `related_name='+'` tells Django not to create a reverse relation with Product as it would create unnecessary complexities.

> Question might arise: `Why not a many-to-many relationship here?` The featured_product on Collection is a special pointer—it’s like saying “this is the star product for this collection,” and that’s it. It does not mean the product “belongs” to the collection in the regular sense. That's much different from many-to-many relationship.

#### Generic Relationship

Generic relationships are important as it allows the apps to be more independent of each other. Here Tag will be used with Products but in future in can be used with other apps also. It uses Django’s GenericForeignKey system (with content_type and object_id) so you can tag anything (products, blog posts, users, whatever).

```python
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
```

- tag set to the “sale” Tag
- content_type set to “Product”
- object_id set to the product’s id
- content_object lets you access the actual product directly

Likewise LinkedItem entity was also created

```python
class LinkedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
```

#### Creating Migrations

When it comes to creating migration, we can simply perform it by typing the command

```bash
python manage.py makemigrations
```

For every app, it will create a migration file inside the `migration` folder.

#### Performing Migrations

Since we have done the migrations, now we have to perform the migration in order to create the database.

```bash
python manage.py migrate
```

Now say we want to change something and then want to perform the migration. Lets add the following code inside Customer class.

```python
class Meta:
    db_table = 'store_customers'
    indexes = [
        models.Index(fields=['last_name', 'first_name'])
    ]
```

This code perform two tasks:

1. Changes the database table to `db_table`
2. Makes a composite index to make some queries performs faster. `Customer.objects.filter(last_name="Smith", first_name="John")`

If perform the migration and look at the migrations folder, we see the new migration file has a very tedious name. This teaches us a lesson, the two changes we are doing should not have been done in one go, in each migration we should have at most two changes.

#### Reverting Migrations

Of course we can reverse our changes in git, however if we want to revert back to some version of the migration, we can simply do it typing the command `python manage.py migrate store 0003`. Just the migration number is good enough to perform the migration.

#### Connecting to PostgresSQL

We have created a database migration, now perform the setup for connecting to PostgreSQL. If you have postgres installed already, it's fine. If not, please follow along till the setup.

1. Install postgresql through this command `brew install postgresql`. We will install brew as our package manager.
2. Let's gets inside the postgres console. We can simply do that via performing `pspl postgres`
3. Since we are inside the postgres command console, we will perform some operation.
   ```bash
   CREATE USER myuser WITH PASSWORD 'mypassword';
   ALTER USER myuser CREATEDB;
   CREATE DATABASE storefront OWNER myuser;
   GRANT ALL PRIVILEGES ON DATABASE storefront TO myuser;
   ```
4. After we can get out of postgres command console by typing `\q``

Since we have postgres installed, now we need a GUI. We will use the following credentials to connect to pgadmin4

4. Once those details are entered and test connection succeeds, we are ready.

### Using PostgreSQL in Django

In order to connect to Postgresql, we need the following library. We can install it by typing `pip install psycopg2-binary`.

Now inside settings.py in DATABASES section, we have to include the following details

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

Once we have installed the packages and the proper database setting has been done, we can go forward and type `python manage.py migrate`. Once databases are successfully migrated we can go to pgadmin4 console and refresh the database.

#### Running Custom SQL

Let's assume for a task we need to perform SQL operation. For that we will create a empty migration file via `python manage.py makemigrations store --empty`. The file will be stored in the `migrations` folder.

In the migration file, inside the operations array we write this sql command.

```python
operations = [
    migrations.RunSQL("""
        INSERT INTO store_collection (label)
        VALUES ('collection1')
    """, """
        DELETE FROM store_collection
        WHERE label='collection1'
    """)
]
```

When we perform migrations via `python manage.py migrate`, the first sql command will be executed. The second command will be store and will be performed if someone performs a reverse migration using the command `python manage.py migrate store 0004`.

## Django ORM

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

### Filtering Objects

Let's talk about filtering objects. If we want to filter products who price is greater than 20, we can write some filter code.

```python
queryset = Product.objects.filter(unit_price__gt=20)
```

For getting a range of product

```python
queryset = Product.objects.filter(unit_price__range=(20, 30))
```

For getting a product with a specific name is also possible.

```python
queryset = Product.objects.filter(title__contains='coffee')
```

Now this query is case sensitive. If want to make it case insensitive we can also do it using

```python
queryset = Product.objects.filter(title__icontains='coffee')
```

For more more queries please hop into the office [documentation](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#field-lookups)

#### Filtering Multiple queries

When we want to put multiple conditions inside we can do it two way

1. Putting all the conditions inside the parenthesis and separating them with comma
2. We can also chain them.

```python
queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
```

### Complex Lookups Using Q Objects

If we want to get queries a bit more complex, we need to use Q objects. Let's look at queries.

1. Filter the products where inventory < 10 OR price < 20

```python
queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
```

2. Product where inventory < 10 OR not price < 20

```python
queryset = Product.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__lt=20))
```

### Reference Fields using F Objects

If we want to compare a variable with another variable inside the filter. Say we want to compare the if inventory = price

```python
queryset = Product.objects.filter(inventory=F('unit_price'))
```

### Sorting

If we want to perform some sorting. We can do them using,

```python
queryset = Product.objects.order_by('title') ## Sorting by product title
queryset = Product.objects.order_by('unit_price', '-title')
## Sorting by unit_price in ascending order
## Sorting by title in descending order
queryset = Product.objects.order_by('unit_price', '-title').reverse()
# Reversing the order
```

### Limiting Results

Now let's assume we want to limit the result by 5.

```python
queryset = Product.objects.order_by('unit_price', '-title')[:5]
```

### Selecting Fields Query

If we want to get specific fields, we can simply do it by selecting values inside the quotation mark.

```python
queryset = Product.objects.values('id', 'title')
```

When we want to get something that involves multiple database tables. Let's assume we want to get the collection id in which the collection belongs.

```python
queryset = Product.objects.values('id', 'title', 'collection__title')
```

If we want to get the same data in a tuple format without mentioning the fields name, we can use `values_list`

```python
queryset = Product.objects.values_list('id', 'title', 'collection_title')
```

Now take a complex query. Let's perform one exercise. We need to sort product that have been ordered, and we can sort them by their title.

```python
# We first need to sort the product that has been ordered by their distinct values
ids = OrderItem.objects.values_list('product_id').distinct()
# After we will filter them by using the product_ids that are present in the queries
queryset = Product.objects.filter(id__in=ids).order_by('title')
```

### Deferring Fields

When the database has too many fields to load we can simply avoid it by typing only.

```python
queryset = Product.objects.only('id', 'title')
```

However we need to be careful if we use only. Let's look how this can cause issue.

```python
<html>
  <body>
    <h1>Hello World!</h1>
    <ul>
      {% for product in products %}
      <li>{{ product.title }} {{ product.unit_price }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
```

These takes a massive amount of time to load. Now if we look at the sql queries, we will see it has made the query to fetch unit_price. However, the `queryset` only fetched id and title. So for `unit_price`, it had to call the database `N=1000` times for us. Moral of the story, we need to be careful when fetching the data.

Let's talk about deferring. Sometime we are sure we don't want certain fields. Then we can take help of defer.

```python
queryset = Product.objects.defer('description')
```

### Selection of Related Objects

For a moment, let's assume we want to fetch the product title and the collection it belongs to. Hence, we have written this query in our template.

```html
<html>
  <body>
    <h1>Hello World!</h1>
    <ul>
      {% for product in products %}
      <li>{{ product.title }} {{ product.collection.title }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
```

with the following query in the views.

```python
queryset = Product.objects.all()
```

If we do that we will face a similar problem we have faced before. The query takes too much time to execute.

For the reason, we can preload the data from necessary field, here in our case the `collection` field.

```python
queryset = Product.objects.select_related('collection').all()
```

We have to keep one thing in mind. When the relationship is 1 to N, means a product can be associated with only one collection, we will use select_related.

However we use `prefetch_related()` when the other end of the relationship has N. Means a product can be associated to many promotions.

```python
queryset = Product.objects.prefetch_related('collection').all()
```

We can also use a combination of them. We can see the product title, the collection it belongs to and all the promotions it is attached to just with this

```python
<html>
  <body>
    <h1>Hello World!</h1>
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
  </body>
</html>
```

Let's do one exercise. Get the last 5 orders with their customer and items. That can be achieved by the following code

```python
queryset = Order.objects.select_related('customer').order_by('-placed_at')[:5]
```

### Aggregating Objects

There are many aggregate functions inside django which we can import from `django.db.models.aggregates`.

If we want to get on how many entries are in a database, we can simply do them using

```python
result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
```

### Annotating Objects

We can add extra fields into the table when we are fetching via aggregating function. We can add an extra field `is_new` to every customer row.

```python
queryset = Customer.objects.annotate(is_new=Value(True))
```

If you look at the specific SQL queries inside the database it is creating the following command,

```python
SELECT "store_customers"."id",
       "store_customers"."first_name",
       "store_customers"."last_name",
       "store_customers"."email",
       "store_customers"."phone",
       "store_customers"."birth_date",
       "store_customers"."membership",
       true AS "is_new"
FROM "store_customers"
```

### Calling Database Functions

Now let's assume we want to get the full name of the customer. We can use `CONCAT` function.

```python
queryset = Customer.objects.annotate(
    full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
)
```

However, we can get the same result using the same query

```python
queryset = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    )
```

### Grouping Data

If we want to see the count of orders of each customer we can also see that using the count variable.

```python
queryset = Customer.objects.annotate(
        orders_count=Count('order_count')
    )
```

### Expressions

Now let's assume we want to get the price list after applying discount. How can we do it.

```python
discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())

queryset = Product.objects.annotate(
    discounted_price = discounted_price
)
```

> F is Django’s F expression. It lets you refer to a database field’s value directly in the query, so the math/comparison happens in SQL, not in Python. F('unit_price') \* 0.8 builds the expression “take each row’s unit_price and multiply by 0.8”.

### Querying Generic Relationships

As we have already mentioned a the store app and models app are separated. We have deliberately kept them separate just to make them more reusable.

However we can connect them using ContentType table. On the database named `content_type`. For that we need to import the models from ContentType table in order to connect those two items.

Here is a short description.

```python
def say_hello(request):
    content_type = ContentType.objects.get_for_model(Product)

    queryset = TaggedItem.objects.select_related('tag').filter(
        content_type = content_type,
        object_id = 1
    )

    return render(request, 'hello.html', {'name': 'Pritom', 'customer': list(queryset)})
```

Let's go through this query one by one. What this line tells, `content_type = ContentType.objects.get_for_model(Product)`, is to find the id of content_type where `app_label` is 'store' and model is 'Product'.

```python
queryset = TaggedItem.objects.select_related('tag').filter(
    content_type = content_type,
    object_id = 1
)
```

Even though we have taggedItem but the label tag is only available in the the SQL table `tags_tag`. After joining the table we will perform some filtering operation where `content_type=14`

### Custom Managers

If we look at the previous code, it is clearly visible it is a verbose code. It would have been really nice if we just write `TaggedItem.objects.get_tags_for(Product, 1)`

We can set up our custom manager inside the model file, using the following code

```python
class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects.select_related('tag').filter(
            content_type = content_type,
            object_id = obj_id
        )
```

and inside the TaggedItem class, we can include the following code

```python
class TaggedItem(models.Model):
    objects = TaggedItemManager()
```

### Query Caching

When we talk about query we have to talk about query caching. Let's look at this line of code

```python
queryset = Products.objects.alL()
list(queryset)
queryset[0]
```

First all the all the products will be fetched from the disk. Since it is a expensive query django will store the result of queryset. Then whichever operation we perform, django will use the stored result.

```python
queryset = Products.objects.alL()
queryset[0]
list(queryset)
```

Now storing the query will not happen as, the first query only asks for the first element, and the second query asks for all the elements.

### Creating Objects

What we have already done, is querying data. However, we have not entered data. However we can do it using the following command

```python
def say_hello(request):
    collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product.objects.get(pk=1)
    collection.save()

    return render(request, 'hello.html', {'name': 'Pritom'})
```

We first introduce the collection. Afterwards we select the title and we add the featured product to primary key 1. Afterward we save the collection.

Now for some reason, we don't want to update the title. We just want to update the product_key. If we do that, and look at the SQL command we will see, the title is being set to empty string and that we don't want. It is causing Data loss.

```sql
UPDATE "store_collection"
   SET "title" = '',
       "featured_product_id" = NULL
 WHERE "store_collection"."id" = 11
```

The main reason of this issue is Django automatically adds `collection.title = ''`. However we can solve it by using by first reading it from the database and then updating it.

```python
collection = Collection.objects.get(pk=11)
collection.featured_product = None
collection.save()
```

You might argue, this extra reading may cause performance issues. However, it is the simplest way to implement it in the code. However, we can do that by using the keyword argument.

```python
Collection.objects.filter(pk=11).update(featured_product=None)
```

### Deleting Objects

We have seen how to read objects, how to delete objects, and now we have to know to delete objects. It is actually pretty simple in Django. Let's look at this code for a bit.

```python
def say_hello(request):
    collection = Collection(pk=11)
    collection.delete()
```

If we want to delete multiple elements from a database table we can simply do it using filter function.

```python
Collection.objects.filter(pk__gt=5)
```

It will look into the database and delete all the element whose primary key is above 5.

### Transactions

Let's assume we want to add an orderItem. Now without Order we can not import OrderItem. First we need to create an Order and OrderItem will use that value to create an OrderItem.

```python
def say_hello(request):
    order = Order()
    order.customer_id = 1
    order.save()

    item = OrderItem()
    item.order = order
    item.product_id = 1
    item.quantity = 1
    item.unit_price = 10
    item.save()
```

Since it is a sequential order, in other words, if for some part fails in creating the Order and OrderItem, the other part will be inconsistent. As a result, we have to make sure the one part fails, the whole operation should be rolled back. We can exactly do that by the help of Transactions.

We can wrap a whole function inside a Transaction by using `@transaction.atomic()` decorator.

```python
@transaction.atomic()
def say_hello(request):
    order = Order()
    order.customer_id = 1
    order.save()

    item = OrderItem()
    item.order = order
    item.product_id = 1
    item.quantity = 1
    item.unit_price = 10
    item.save()
```

Now let's assume we want to enclose certain part of the the code inside a function into the transaction. We can do that using `with transaction.atomic()``

```python
with transaction.atomic():
    order = Order()
    order.customer_id = 1
    order.save()

    item = OrderItem()
    item.order = order
    item.product_id = 1
    item.quantity = 1
    item.unit_price = 10
    item.save()
```

### Executing RAW SQL queries

Sometimes we can not implement some complex queries with Django ORM. As it would lead us to writing convoluted queries. In addition, the SQL query will be much more performance efficient.

```python
def say_hello(request):
    queryset = Product.objects.raw('SELECT * FROM store_product')

    return render(request, 'hello.html', {'name': 'Pritom', 'result': list(queryset)})
```

## Making an Admin Site

### Setting Up the Admin Site

As we know every Django project comes with an admin site. We can access the admin site using the link `http://localhost:8000/admin/`. In order to access the admin site we need to create a super user.

We can create a super user by the following command.

```bash
python manage.py createsuperuser
```

However, we can perform even more modification. We can change the header and the index title using the following code inside `storefront/urls.py`

```python
admin.site.site_header = 'Storefront Admin'
admin.site.index_title = 'Admin'
```

### Registering Models

In order to register for models, we need to go the `admin.py` file and register the models. If we want to register the Collection model, we can simply do that using

```python
admin.site.register(models.Collection)
```

After registering the models if we go to the admin panel we will see all the collections. However the collections will be represented a more vague format. We will see a list sort of like this one

```
Collection object (10)
Collection object (9)
Collection object (8)
Collection object (7)
Collection object (6)
Collection object (5)
Collection object (4)
Collection object (3)
Collection object (2)
Collection object (1)
```

However, this is not very meaningful as looking at it we are not understanding anything. However, we can change by adding a very simple function. The function would be

```python
def __str__(self):
    return self.title
```

- **str** is a special Python method that defines the human-readable string representation of an object.
- Inside the function we will return the title.

Now we see the following collection

```
Magazines
Toys
Spices
Baking
Pets
Stationary
Cleaning
Beauty
Grocery
Flowers
```

If we want the titles to to come in sorted manner, we can implement them by including a Meta class. Inside the meta class we can include stuffs like ordering, table name, and indexes. Here we are only concerned with the ordering.

```python
class Meta:
    ordering = ['title']
```

Likewise we can implement the same collection addition, and the title ordering just by including collection.

### Customizing the List Pages

Let's see another way to registering the admin.

```python
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']
    list_editable = ['unit_price']
    list_per_page = 10
```

- `@admin.register(models.Product)` registers Product to the admin
- `class ProductAdmin(admin.ModelAdmin):` is a class where all the configurations will be mentioned
- `list_display = ['title', 'unit_price']` tells django to only load the **title**, **unit_price** from the database.
- `list_per_page` allows you to limit data on per page count basis.

The Customer page has also been organized in the same manner.

> In order to get a full picture of allowed admin object hop into the following [link](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#modeladmin-objects)

### Adding Computed Column

Now for knowing the current status of the inventory, we may need another computer field to add. Let's assume we want to label all those inventories that has less than 10 products.

- First we will add the following function into the code

  ```python
  def inventory_status(self, product):
      if product.inventory < 10:
          return 'Low'
      return 'OK'
  ```

- Then we will add function name (inventory_status) to the `list_display`
- However, it is not sortable. We can add sorting by adding the decorator `@admin.display(ordering='inventory')` on top of `inventory_status` function.

### Selecting Related Objects

When it comes to selecting related fields, we can do it in a certain way to make it bit more performance efficient.

- First we will preload the necessary table for adding related tables. We will pre load all the collection that the product belongs to via `list_select_related = ['collection']`
- We will get the collection title, via the following command
  ```python
  def collection_title(self, product):
      return product.collection.title
  ```
- After that, we will add the collection_title into `list_display` array.

### Overriding the Base QuerySet

In we can get the base querySet that Django Admin uses to fetch via

```python
def get_queryset(self, request):
    return super().get_queryset(request).annotate(
        products_count = Count('product')
    )
```

get_queryset(self, request) overrides the base queryset that Django Admin uses to fetch rows for the changelist.

- By default, super().get_queryset(request) returns a plain queryset of the model (Collection.objects.all() with admin filters/permissions applied).
- .annotate(products_count=Count('product')), so every Collection row comes with an extra computed column (products_count).

### Providing

In the product count column, when we click on it, we just want to see the product which is associated with the current column.

```python
def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
        + '?'
        + urlencode({
            'collection__id': str(collection.id)
        }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
```

- `reverse('admin:store_product_changelist')` get the admin page link
- `urlencode({'collection__id': str(collection.id)}))` adds the queries in a dictionary format.
