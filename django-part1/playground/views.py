from django.shortcuts import render
from django.http import HttpResponse
from store import models as store_models

def say_hello(request):
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
