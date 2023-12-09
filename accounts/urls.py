from django.urls import path  
from accounts.views import login_page, registration_page

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', registration_page, name= 'register'),
]