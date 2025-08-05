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

Since we have postgres installed, now we need a GUI. We can use pgAdmin, but for the this project we will use DataGrip. In Datagrip, creating a new project give the following commands. 1. Username: `myuser` 2. Password: `mypassword` 3. port: `5432` (That should be the default port)

4. Once those details are entered and test connection succeeds, we are ready.
