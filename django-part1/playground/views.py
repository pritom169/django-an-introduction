from django.shortcuts import render
from django.db.models import Value, F, Func, Count
from store.models import Customer

def say_hello(request):
    queryset = Customer.objects.annotate(
        orders_count=Count('order_count')
    )

    return render(request, 'hello.html', { 'name': 'Pritom', 'customer': list(queryset)})