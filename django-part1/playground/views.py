from django.shortcuts import render
from django.db.models import Value, F, ExpressionWrapper, DecimalField
from store.models import Customer, Product

def say_hello(request):
    discounted_price = ExpressionWrapper(F('unit_price') * 0.9, output_field=DecimalField())

    queryset = Product.objects.annotate(
        discounted_price = discounted_price
    )
    return render(request, 'hello.html', { 'name': 'Pritom', 'customer': list(queryset)})