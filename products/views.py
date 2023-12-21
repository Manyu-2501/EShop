from django.shortcuts import render
from .models import *

# Create your views here.
def get_product(request, product_slug):
    try:
        product = Product.objects.get(product_slug=product_slug)
        context = {"product":product}
        if request.GET.get("size"):
            size = request.GET.get("size")
            price = product.get_price_by_size(size)
            context["selected_size"]=size
            context["adjusted_price"]=price

        return render(request, "products/product.html", context)
    except Exception as e:
        print(e)

def get_category(request, category_slug):
    try:
        category = Category.objects.get(category_slug=category_slug)
        categories = Category.objects.all()
        context = {"category":category, "categories":categories}

        return render(request, "products/category.html", context)
    except Exception as e:
        print(e)






