from django.shortcuts import render
from .models import Product, Cart, CartItem, User, Category, Comment
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q

# Create your views here.

def index(request):
    latest_products = Product.objects.all().order_by('-created_at')

    cart = Cart.objects.get(user=request.user)

    cart_products = CartItem.objects.filter(cart=cart)[:3]

    trending_products = Product.objects.filter(is_trending=True)
    for t in trending_products:
        print(t.image.url)

    context = {
        'cart_products': cart_products,
        'trending_products': trending_products,
        'latest_products': latest_products,
    }
    return render(request, 'index.html', context=context)

def categories(request):
    return render(request, 'categories.html')

def filter_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    filtered_products = Product.objects.filter(category=category)

    sort_type = request.GET.get('sort')
    if sort_type == 'price_low':
        filtered_products = Product.objects.filter(category=category).order_by('price')
    elif sort_type == 'price_high':
        filtered_products = Product.objects.filter(category=category).order_by('-price')
    elif sort_type == 'new':
        filtered_products = Product.objects.filter(category=category).order_by('-created_at')

    context = {
        'filtered_products': filtered_products,
        'category': category
    }
    return render(request, 'filter_by_category.html', context=context)

def search_products(request):
    search_query = request.GET.get('search_query')
    products = Product.objects.filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))
    context = {
        'products': products,
        'query': search_query
    }
    return render(request, 'search_results.html', context=context)
