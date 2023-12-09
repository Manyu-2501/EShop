from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


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
           return redirect('/')
            
        messages.warning(request, "Password does not match the username")
        return HttpResponseRedirect(request.path_info)

            
    return render(request, 'accounts/login.html')

def registration_page(request):
    if(request.method=='POST'):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

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