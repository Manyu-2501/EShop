from django.urls import path  
from accounts.views import login_page, registration_page, activate_account, cart, add_to_cart, reset_password, logout_page

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', registration_page, name= 'register'),
    path('activate/<str:email_token>', activate_account, name='activate'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<uuid>/', add_to_cart, name='add_to_cart'),
    path('reset-password/', reset_password, name='reset_password'),
    path('logout/', logout_page, name='logout')
]