from django import forms
from app.models import User, Product
from .models import InventoryItem

class SellerRegisterationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'house_no', 'state', 'city', 'district', 'landmark', 'area_pincode']

class SellerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ProductForm(forms.ModelForm):

    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )

    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'description', 'country_of_origin', 'weight', 'box_components', 'category', 'discount']
