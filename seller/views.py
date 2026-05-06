from django.shortcuts import render, redirect, get_object_or_404
from .decorators import seller_only_access
from .forms import SellerRegisterationForm, SellerLoginForm, ProductForm
from django.contrib import messages
from django.contrib import auth
from .models import Inventory, InventoryItem
from app.models import Order, Product

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

@seller_only_access()
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

@seller_only_access()
def pending_orders(request):
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'seller/partials/pending_orders_partial.html')
    return render(request, 'seller/pending_orders.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            inventory = get_object_or_404(Inventory, seller=request.user)
            inventory_item = InventoryItem.objects.create(inventory=inventory, product=product, quantity=quantity)
            inventory_item.save()
            return redirect('seller:inventory')
    else:
        form = ProductForm()

    context = {
        'form': form,
    }
    return render(request, 'seller/add_product.html', context=context)

@seller_only_access()
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    inventory_item = get_object_or_404(InventoryItem, product=product)
    if request.method == 'POST':
        form = ProductForm(data=request.POST, instance=product)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            form.save()
            inventory_item.quantity = quantity
            inventory_item.save(update_fields=['quantity'])
            return redirect('seller:inventory')

    form = ProductForm(instance=product, initial={'quantity': inventory_item.quantity})
    context = {
        'form': form,
        'product_slug': product.slug
    }
    return render(request, 'seller/edit_product.html', context=context)

@seller_only_access()
def delete_prooduct(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
        product.delete()

    if request.headers.get('HX-Request') == 'true':
        inventory = get_object_or_404(Inventory, seller=request.user)
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
            'active_listing': active_listings,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
        }
        return render(request, 'seller/partials/inventory_item_partial.html', context=context)

