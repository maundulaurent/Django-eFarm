from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service-list'),
    path('<int:pk>/', views.service_detail, name='service-detail'),
    path('<int:pk>/book/', views.book_service, name='book-service'),
    path('my-bookings/', views.my_bookings, name='my-bookings'),
    path('manage-bookings/', views.manage_bookings, name='manage-bookings'),
    path('confirm-booking/<int:booking_id>/', views.confirm_booking, name='confirm-booking'),
]