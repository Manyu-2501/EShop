from django.shortcuts import render
from products.models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {"products":products}
    if request.user.is_authenticated:
        print("authenticated", request.user.username)
    return render(request, 'home/index.html', context)
