from django.urls import path  
from products.views import get_product

urlpatterns = [
    path('<slug:product_slug>', get_product , name='get_product'),
    # path('<slug:category_slug>', category)
    
]