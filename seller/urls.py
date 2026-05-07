from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('profile/', views.profile, name='seller_profile'),
    path('register/', views.seller_registeration_view, name='seller_registeration'),
    path('login/', views.seller_login_view, name='seller_login'),
    path('inventory/', views.inventory, name='inventory'),
    path('pending-orders/', views.pending_orders, name='pending_orders'),
    path('ship-order/<int:id>/', views.ship_order, name='ship_order'),
    path('confirm-shipment/<int:id>/', views.confirm_shipment, name='confirm_shipment'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<slug:slug>/', views.edit_product, name='edit_product'),
    path('delete-product/<slug:slug>/', views.delete_prooduct, name='delete_product'),
    
]

