from django.contrib import admin
from .models import User, Product, Cart, CartItem, Category, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {"slug": ["name"]}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'image', 'category__name', 'seller__username', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ["name"]}

class CartAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'created_at', 'updated_at',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart__user__username', 'product__name', 'price',)

admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
