from django.shortcuts import render
from django.db import transaction
from store.models import Product

def say_hello(request):
    queryset = Product.objects.raw('SELECT * FROM store_product')

    return render(request, 'hello.html', {'name': 'Pritom', 'result': list(queryset)})