from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('categories/filter-by-category/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
    path('search-products/', views.search_products, name='search_products')
]

