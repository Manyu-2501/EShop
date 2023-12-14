from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, Cart, CartItem
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from products.models import Product, SizeVariant
from home.views import index


def login_page(request):
    if request.method=='POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(username = email).last()
    
        if not user:
            messages.warning(request, "User not found")
            return HttpResponseRedirect(request.path_info)

        if not user.profile.is_email_verified:
            messages.warning(request, "Account not activated, please check mail")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username=email, password=password)
        if user_obj:
           login(request, user)
           return redirect('http://127.0.0.1:8000/home/')
            
        messages.warning(request, "Password does not match the username")
        return HttpResponseRedirect(request.path_info)

            
    return render(request, 'accounts/login.html')

def registration_page(request):
    if request.method=='POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password!= confirm_password:
            messages.warning(request, "Password does not match")
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.filter(username=email).last()
        if(user_obj):
            messages.info(request, "User already exists.")
            return HttpResponseRedirect(request.path_info)
        else:
            user = User.objects.create(username = email, first_name = first_name, last_name = last_name)
            user.set_password(password)
            user.save()
            messages.success(request, "An email has been sent to you")
            
            return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')

def activate_account(request, email_token):
    try:
        profile = Profile.objects.get(email_token=email_token)
        profile.is_email_verified = True 
        profile.save()
        return redirect('/')
    except Exception as e:
        print(e)
        return HttpResponse("Invalid token. Exception:", e)
    
def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        username = request.POST.get("email")
        user = User.objects.filter(username = username).last()
        print(password)
        if not user:
            messages.warning(request, "User does not exist")
            return HttpResponseRedirect(request.path_info)
        
        if not password == confirm_password:
            messages.warning(request, "Password does not match")
            return HttpResponseRedirect(request.path_info)
        user.set_password(password)
        user.save()
        messages.success(request, "Password changed succesfully")
    return render(request, "accounts/reset_password.html")

def add_to_cart(request, uuid):
    user = request.user
    print(type(user))
    product = Product.objects.get(uuid=uuid)
    cart,_ = Cart.objects.get_or_create(user=user, is_paid=False)
    item = CartItem.objects.create(cart=cart, product=product, price=product.price)
    if request.GET.get("size"):
        size = request.GET.get("size")
        size = SizeVariant.objects.get(size = size, product = product)
        item.size = size 
        item.price += size.price
        item.save()
    return HttpResponseRedirect(request.path_info)


def cart(request):
    return render(request, "accounts/cart.html")

def logout_page(request):
    logout(request)
    return redirect("index")
