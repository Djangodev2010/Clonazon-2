from .models import Category

def get_categories(request):
    categories = Category.objects.all().order_by('name')
    return dict(categories=categories)
