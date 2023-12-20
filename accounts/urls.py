from django.urls import path  
from accounts.views import *

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', registration_page, name= 'register'),
    path('activate/<str:email_token>', activate_account, name='activate'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<uuid>/', add_to_cart, name='add_to_cart'),
    path('buy-now/<uuid>/', buy_now, name='buy_now'),
    path('remove-cart-item/<uuid>', remove_cart_item, name='remove_cart_item'),
    path('reset-password/', reset_password, name='reset_password'),
    path('remove-coupon/', remove_coupon, name='remove_coupon'),
    path('success/', payment_success, name='payment_success'),
    path('logout/', logout_page, name='logout')
]