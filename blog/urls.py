from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article-list'),
    path('add/', views.add_article, name='add-article'),
    path('categories/', views.category_list, name='category-list'),
    path('<slug:slug>/', views.article_detail, name='article-detail'),
    path('<slug:slug>/update/', views.update_article, name='update-article'),
    path('<slug:slug>/delete/', views.delete_article, name='delete-article'),
]