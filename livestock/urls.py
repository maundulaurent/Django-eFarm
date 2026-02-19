from django.urls import path
from . import views

urlpatterns = [
    path('', views.livestock_list, name='livestock-list'),
    path('<int:pk>/', views.livestock_detail, name='livestock-detail'),
    path('add/', views.add_livestock, name='add-livestock'),
    path('<int:pk>/update/', views.update_livestock, name='update-livestock'),
    path('<int:pk>/delete/', views.delete_livestock, name='delete-livestock'),
    path('stats/', views.livestock_stats, name='livestock-stats'),
]