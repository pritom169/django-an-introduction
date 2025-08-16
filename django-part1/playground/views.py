from django.shortcuts import render
from store.models import Collection, Product

def say_hello(request):
    collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product.objects.get(pk=1)
    collection.save()

    return render(request, 'hello.html', {'name': 'Pritom'})