from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('profile/', views.profile, name='seller_profile'),
    path('register/', views.seller_registeration_view, name='seller_registeration'),
    path('login/', views.seller_login_view, name='seller_login'),
    path('inventory/', views.inventory, name='inventory'),
    path('pending-orders/', views.pending_orders, name='pending_orders'),
    
]

