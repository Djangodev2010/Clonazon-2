from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    house_no = models.PositiveIntegerField()
    landmark = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=200, default='')
    district = models.CharField(max_length=200, default='')
    state = models.CharField(max_length=200, default='')
    area_pincode = models.PositiveIntegerField(default=202020)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_address(self):
        return self.house_no + ', ' + self.district + ', ' + self.city + ', ' + self.state + ', ' + self.area_pincode
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.first_name + '-' + self.last_name

class Category(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='category_images/')
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=355)
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField(max_length=855)
    price = models.PositiveIntegerField(default=0)
    country_of_origin = models.CharField(max_length=155)
    weight = models.PositiveIntegerField(default=0)
    box_components = models.CharField(max_length=455)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(max_length=355)
    discount = models.PositiveIntegerField(default=0)
    free_delivery = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.discount:
            self.price -= int(self.price * (self.discount/100))
        super(Product, self).save(*args, **kwargs)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + "'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=555)
    rating = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.username + ': ' + self.product.name    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ': '  + self.product.name
    
