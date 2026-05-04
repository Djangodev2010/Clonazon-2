from django.db import models
from app.models import User, Product
from django.core.exceptions import ValidationError

# Create your models here.

class Inventory(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if self.seller.is_seller:
            return super().clean()
        raise ValidationError("You Are Not An Authorised Seller!")

    def __str__(self):
        return self.seller.first_name + "'s Inventory"


class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.inventory.seller.first_name + self.product.name + str(self.quantity)
