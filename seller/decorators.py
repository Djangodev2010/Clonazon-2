from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def seller_only_access():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_seller:
                messages.error(request, 'Only Verified Sellers Can Access This URL!')
                return redirect('index')
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator
