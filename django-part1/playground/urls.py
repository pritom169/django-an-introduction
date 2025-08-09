from django.urls import path
from playground.views import orm_demo
from . import views

# URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('orm-demo/', orm_demo)
]