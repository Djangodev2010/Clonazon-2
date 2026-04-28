from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem, User, Category, Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import UserRegisterationForm, UserLoginForm, CommentForm
from django.contrib import auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    latest_products = Product.objects.all().order_by('-created_at')[:4]
    trending_products = Product.objects.filter(is_trending=True)[:4]

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_products = CartItem.objects.filter(cart=cart)[:3]
        context = {
            'trending_products': trending_products,
            'latest_products': latest_products,
            'cart_products': cart_products
        }

        return render(request, 'index.html', context=context)

    context = {
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

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    discount = product.discount if product.discount else 0
    discounted_price = int(product.price - product.price * discount / 100)
    comments = Comment.objects.filter(product=product)
    
    is_cart_item = False
    if request.user.is_authenticated:
        # Using filter().first() is a bit safer than .get() to avoid errors
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            is_cart_item = CartItem.objects.filter(cart=cart, product=product).exists()

    context = {
        'product': product,
        'discount': discount,
        'discounted_price': discounted_price,
        'comments': comments,
        'stars': list(range(5)),
        'is_cart_item': is_cart_item,
    }
    return render(request, 'product_detail.html', context)

def add_to_cart(request, slug):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
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

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            cart = Cart.objects.create(user=user)
            return redirect('/login')
    form = UserRegisterationForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context=context)

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            messages.error(request, 'Invalid Creditentials!')
    else:

        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def add_comment(request, slug):
    product = get_object_or_404(Product, slug=slug)
    user = request.user
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if Comment.objects.filter(user=user, product=product).exists():
                messages.error(request, "You Cannot Post More Than 1 Comment!")
                return HttpResponseRedirect(request.path_info)
            else:
                comment.product, comment.user = product, user
                comment.save()
                return HttpResponseRedirect(request.path_info)
    else:
        discount = 0
        if product.discount:
            discount = product.discount
        discounted_price = int(product.price - product.price * product.discount / 100)
        comments = Comment.objects.filter(product=product)
        context = {
                'product': product,
                'discount': discount,
                'discounted_price': discounted_price,
                'comments': comments,
                'stars': list(range(5)),
            }
        return render(request, 'product_detail.html', context=context)
    
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        house_no = request.POST.get('house_no')
        city = request.POST.get('city')
        state = request.POST.get('state')
        landmark = request.POST.get('landmark')
        pincode = request.POST.get('pincode')
        confirm_password = request.POST.get('confirm_password')
        user.username = username
        user.email = email
        user.house_no = house_no
        user.city = city
        user.state = state
        user.landmark = landmark
        user.area_pincode = pincode

        if password != '' and password == confirm_password:
            user.set_password(password)
        user.save()
        messages.success(request, 'Information Saved Successfully!')
        return redirect('login')
    
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.price * cart_item.quantity
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'profile.html')

def about_us(request):
    return render(request, 'about_us.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def cart_checkout(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.product.price * cart_item.quantity
    print(total_price)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context=context)

def checkout(request, slug):
    return render(request, 'checkout.html')

def order_details(request):
    return render(request, 'order_details.html')

