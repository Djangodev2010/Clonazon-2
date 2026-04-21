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
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('profile/cart-item/reduce-quantity/<int:id>/', views.reduce_quantity, name='reduce_quantity'),
    path('profile/cart-item/increase-quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('profile/cart-item/remove-cart-item/<int:id>/', views.remove_cart_item, name='remove_cart_item'),
]

