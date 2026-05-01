from django.shortcuts import render
from .decorators import seller_only_access

# Create your views here.

@seller_only_access()
def index_view(request):
    return render(request, 'seller/index.html')
