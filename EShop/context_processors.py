# EShop/context_processors.py
from django.conf import settings

def base_url(request):
    """
    Exposes BASE_URL to templates as 'BASE_URL'.
    """
    return {
        "BASE_URL": settings.BASE_URL
    }