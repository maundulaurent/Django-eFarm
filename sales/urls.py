from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order-list'),
    path('order/<str:order_number>/', views.order_detail, name='order-detail'),
    path('create/', views.create_order, name='create-order'),
    path('order/<str:order_number>/update-status/', views.update_order_status, name='update-order-status'),
    path('cart/', views.cart_view, name='cart-view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
]