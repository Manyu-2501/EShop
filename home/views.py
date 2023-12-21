from django.shortcuts import render
from products.models import *

# Create your views here.
def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {"products":products, "categories":categories}
    if request.user.is_authenticated:
        print("authenticated", request.user.username)
    return render(request, 'home/index.html', context)
