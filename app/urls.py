from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('categories/filter-by-category/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
    path('search-products/', views.search_products, name='search_products'),
    path('latest-products/', views.latest_products, name='latest_products'),
    path('trending-products/', views.trending_products, name='trending_products'),
    path('product-detail/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart')
]

