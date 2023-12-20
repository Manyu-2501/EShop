from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .models import Profile, Cart, CartItem
from products.models import Product, SizeVariant, Coupon
from django.conf import settings
from base.emails import send_password_reset_mail
from base.helper import send_invoice_mail
import hmac
import hashlib
import razorpay


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
        send_password_reset_mail(user.username)
        user.set_password(password)
        user.save()
        messages.success(request, "Password changed succesfully")
    return render(request, "accounts/reset_password.html")

@login_required
def add_to_cart(request, uuid):
    user = request.user
    product = Product.objects.get(uuid=uuid)
    cart,_ = Cart.objects.get_or_create(user=user, is_paid=False)
    item = CartItem.objects.create(cart=cart, product=product)
    if request.GET.get("size"):
        size = request.GET.get("size")
        size = SizeVariant.objects.get(size = size, product = product)
        item.size = size 
        item.save()
    return redirect("index")

@login_required
def cart(request):
    cart = None
    payment = None
    try:
        cart = Cart.objects.get(user = request.user, is_paid=False)
    except Exception as e:
        print(e)    
    
    if cart:

        if request.method == "POST":
            coupon_code = request.POST.get("coupon_code")
            coupon = Coupon.objects.filter(coupon_code = coupon_code, is_expired=False)
            if not coupon.exists():
                messages.warning(request, "Coupon does not exist or it has expired")
                return redirect("cart")
            
            if cart.coupon:
                messages.warning(request, "Coupon already applied")
                return redirect("cart")
            
            if cart.get_cart_price() < coupon.last().minimum_amount:
                messages.warning(request, f'Minimum amount of cart should be {coupon.last().minimum_amount}')
                return redirect("cart")
            
            cart.coupon = coupon.last()
            cart.save()
            messages.success(request, f'Coupon Applied: {coupon_code}')
    
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        client.set_app_details({"title" : "EShop", "version" : "1.0"})
        data = { "amount": cart.get_final_amount()*100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)

        cart.razorpay_order_id = payment["id"]
    razorpay_key_id = settings.RAZORPAY_KEY_ID
    context = {"cart" : cart, "payment": payment, "razorpay_key": razorpay_key_id }
    
    return render(request, "accounts/cart.html", context)

def payment_success(request):
    
    cart = Cart.objects.get(user = request.user, is_paid=False)
    razorpay_payment_signature = request.GET.get("razorpay_signature")
    razorpay_payment_id = request.GET.get("razorpay_payment_id")
    razorpay_order_id = cart.razorpay_order_id
    print("***** REACHED ******")
    string_hmac = f'{razorpay_order_id}|{razorpay_payment_id}'
    key=settings.RAZORPAY_KEY_SECRET
    generated_signature = hmac.new(key.encode('utf-8') , string_hmac.encode('utf-8'), hashlib.sha256).hexdigest()
    print(generated_signature)
    print(razorpay_payment_signature)
    if generated_signature == razorpay_payment_signature :
        cart.razorpay_payment_id = razorpay_payment_id
        cart.is_paid = True
        cart.save()
        print("done")
        
    return redirect("cart")
    
@login_required
def remove_coupon(request):
    cart = Cart.objects.get(user=request.user, is_paid=False)
    cart.coupon = None
    cart.save()
    return redirect("cart")

@login_required
def remove_cart_item(request, uuid):
    try:
        cart_item = CartItem.objects.get(uuid=uuid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return redirect("cart")

@login_required
def logout_page(request):
    logout(request)
    return redirect("index")
