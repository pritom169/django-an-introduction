from django.shortcuts import render
from django.db.models import Value
from store.models import Customer

def say_hello(request):
    queryset = Customer.objects.annotate(is_new=Value(True))
    return render(request, 'hello.html', { 'name': 'Pritom', 'customer': list(queryset)})