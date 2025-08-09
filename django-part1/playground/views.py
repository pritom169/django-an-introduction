from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product

def say_hello(request):
    try:
        product_exists = Product.objects.filter(pk=0).exists
    except ObjectDoesNotExist:
        pass
    return render(request, 'hello.html', { 'name': 'Pritom'})

# -----------ORM Showcase Helpers---------------------------
def _get_models():
    names = [
        "Product",
        "Collection",
        "Customer",
        "Order",
        "OrderItem",
        "Cart",
        "CartItem",
        "Tag"
    ]

    models = {name: None for name in names}

    try:
        for name in names:
            models[name] = getattr(store_models, name, None)
    except Exception:
        pass
    return models

def _maybe_field(model, *candidates):
    if not model:
        return None
    field_names = {f.name for f in model._meta.get_fields()}
    for c in candidates:
        if c in field_names:
            return c
    
    return None

def _add(lines, title, body):
    lines.append(f'## {title}\n{body}')


# _________________Modular ORM Demo Sections_________________
## 1. Demo for managers

def demo_01_managers(models, lines):
    Product = models.get("Product")
    if Product:
        qs_all = Product.objects.all()
        _add(lines, "1. Managers & QuerySets", f"Product.objects.all() SQL: {qs_all.query}")
    else:
        _add(lines, "1. Managers & QuerySets", "Product model not found; skipping Product-based examples.")


def orm_demo(request):
    models = _get_models()
    lines = []
    
    demo_01_managers(models, lines)
    return HttpResponse("<pre>" + "\n\n".join(lines) + "</pre>")