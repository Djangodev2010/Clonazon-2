from django.shortcuts import render
from .models import Product, Cart, CartItem, User, Category, Comment
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.

def index(request):
    latest_products = Product.objects.all().order_by('-created_at')[:4]

    cart = Cart.objects.get(user=request.user)

    cart_products = CartItem.objects.filter(cart=cart)[:3]

    trending_products = Product.objects.filter(is_trending=True)[:4]
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

def latest_products(request):
    latest_products = Product.objects.all().order_by('-created_at')
    context = {
        'latest_products': latest_products,
    }
    return render(request, 'latest_products.html', context=context)

def trending_products(request):
    trending_products = Product.objects.filter(is_trending=True)
    sort_type = request.GET.get('sort')
    if sort_type == 'price_low':
        trending_products = Product.objects.filter(is_trending=True).order_by('price')
    elif sort_type == 'price_high':
        trending_products = Product.objects.filter(is_trending=True).order_by('-price')
    if sort_type == 'new':
        trending_products = Product.objects.filter(is_trending=True).order_by('-created_at')
    context = {
        'trending_products': trending_products,
    }
    return render(request, 'trending_products.html', context=context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    discount = 0
    if product.discount:
        discount = product.discount
    discounted_price = int(product.price - product.price * product.discount / 100)
    comments = Comment.objects.filter(product=product)
    cart = Cart.objects.get(user=request.user)
    is_cart_item = False

    if CartItem.objects.filter(cart=cart, product=product).exists():
        is_cart_item = True
    else:
        is_cart_item = False
    context = {
        'product': product,
        'discount': discount,
        'discounted_price': discounted_price,
        'comments': comments,
        'stars': range(5),
        'is_cart_item': is_cart_item
    }
    return render(request, 'product_detail.html', context=context)

def add_to_cart(request, id):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id)
        cart_item = CartItem.objects.create(cart=cart, product=product, price=product.price)
    if request.headers.get('HX-Request') == 'true':
        is_cart_item = True
        context = {
            'is_cart_item': is_cart_item
        }
        return render(request, 'partials/add_to_cart_form_partial.html', context=context)
        