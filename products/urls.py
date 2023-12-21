from django.urls import path  
from products.views import *

urlpatterns = [
    path('product/<slug:product_slug>', get_product , name='get_product'),
    path('categories/<slug:category_slug>', get_category, name='get_category')
    
]