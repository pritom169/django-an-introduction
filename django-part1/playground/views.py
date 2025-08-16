from django.shortcuts import render
from store.models import Product
from tags.models import TaggedItem

def say_hello(request):
    queryset = Product.objects.all()
    list(queryset)

    return render(request, 'hello.html', {'name': 'Pritom', 'customer': list(queryset)})