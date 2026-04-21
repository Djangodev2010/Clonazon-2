from django.shortcuts import render
from .models import Product, Cart, CartItem, User, Category, Comment
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.

def index(request):
    latest_products = Product.objects.all().order_by('-created_at')[:4]
    trending_products = Product.objects.filter(is_trending=True)[:4]

    try:
        cart = Cart.objects.get(user=request.user)
        cart_products = CartItem.objects.filter(cart=cart)[:3]

        context = {
            'cart_products': cart_products,
            'trending_products': trending_products,
            'latest_products': latest_products,
        }
        return render(request, 'index.html', context=context)
    except Exception as e:
        print("YES")

    context = {
        'trending_products': trending_products,
        'latest_products': latest_products,
    }
    print(context)

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
        
def profile(request, id):
    user = get_object_or_404(User, id=id)
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.price * cart_item.quantity
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'profile.html', context=context)

def reduce_quantity(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.quantity -= 1
    if cart_item.quantity == 0:
        cart_item.delete()
    else:
        cart_item.save()
    user = User.objects.get(id=request.user.id)
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.price * cart_item.quantity
    print(total_price)
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'partials/cart_product_partial.html', context=context)
    return render(request, 'profile.html', context=context)

def increase_quantity(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.quantity += 1
    if cart_item.quantity == 0:
        cart_item.delete()
    else:
        cart_item.save()
    user = User.objects.get(id=request.user.id)
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.price * cart_item.quantity
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'partials/cart_product_partial.html', context=context)
    return render(request, 'profile.html', context=context)

def remove_cart_item(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    user = User.objects.get(id=request.user.id)
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.price * cart_item.quantity
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'partials/cart_product_partial.html', context=context)
    return render(request, 'profile.html', context=context)
