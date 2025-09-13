from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetail.as_view()),
    path('collection/', views.collection_list),
    path('collection/<int:pk>/', views.collection_detail, name='collection-detail')
]