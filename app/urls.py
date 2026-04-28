from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('categories/filter-by-category/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
    path('search-products/', views.search_products, name='search_products'),
    path('latest-products/', views.latest_products, name='latest_products'),
    path('trending-products/', views.trending_products, name='trending_products'),
    path('product-detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('add-comment/<slug:slug>/', views.add_comment, name='add_comment'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('cart-item/reduce-quantity/<int:id>/', views.reduce_quantity, name='reduce_quantity'),
    path('cart-item/increase-quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('cart-item/remove-cart-item/<int:id>/', views.remove_cart_item, name='remove_cart_item'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('about-us/', views.about_us, name='about_us'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
    path('checkout/<slug:slug>/', views.checkout, name='checkout'),
    path('order-details', views.order_details, name='order_details'),

]

