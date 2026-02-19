from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
    path('add/', views.add_product, name='add-product'),
    path('<int:pk>/update/', views.update_product, name='update-product'),
    path('<int:pk>/delete/', views.delete_product, name='delete-product'),
]