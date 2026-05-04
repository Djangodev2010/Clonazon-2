from django.shortcuts import render, redirect
from .decorators import seller_only_access
from .forms import SellerRegisterationForm, SellerLoginForm
from django.contrib import messages
from django.contrib import auth
from .models import Inventory, InventoryItem
from app.models import Order

# Create your views here.

@seller_only_access()
def profile(request):
    if request.headers.get('HX-Request') == 'true':
         return render(request, 'seller/partials/seller_profile_partial.html')
    return render(request, 'seller/index.html')

def seller_registeration_view(request):
    if request.method == 'POST':
        form = SellerRegisterationForm(data=request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.is_seller = True
            seller.save()
            inventory = Inventory.objects.create(seller=seller)
            return redirect('seller:login')
        messages.error(request, f'Something Went Wrong!')
        print(form.errors)
    form = SellerRegisterationForm()
    context = {
        'form': form
    }
    return render(request, 'seller/register.html', context=context)

def seller_login_view(request):
    if request.method == 'POST':
        form = SellerLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('seller:index')
            messages.error(request, 'Invalid Credentials!')
    form = SellerLoginForm()
    context = {
        'form': form
    }
    return render(request, 'seller/login.html', context=context)

def inventory(request):
    inventory = Inventory.objects.get(seller=request.user)
    inventory_items = InventoryItem.objects.filter(inventory=inventory)
    active_listings = len(InventoryItem.objects.filter(inventory=inventory, status=True))
    low_stock = 0
    out_of_stock = 0
    for inventory_item in inventory_items:
        if inventory_item.quantity == 0:
            out_of_stock += 1
        elif inventory_item.quantity <= 5:
            low_stock += 1

    context = {
        'inventory_items': inventory_items,
        'total_items': len(inventory_items),
        'active_listing': active_listings,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
    }
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'seller/partials/inventory_partial.html', context=context)
    return render(request, 'seller/inventory.html', context=context)

def pending_orders(request):
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'seller/partials/pending_orders_partial.html')
    return render(request, 'seller/pending_orders.html')
