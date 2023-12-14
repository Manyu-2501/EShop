from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from products.models import Product, SizeVariant, ColorVariant
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.emails import send_account_activation_mail
from django.contrib import messages
import uuid
# Create your models here.

class Cart(BaseModel):
    user = models.ForeignKey(User, related_name='carts', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    profile_picture = models.ImageField(upload_to='profiles')
    is_email_verified = models.BooleanField(default = False)
    email_token = models.CharField(max_length=100)

    def get_cart_count(self):
        return CartItem.objects.filter(cart__user=self.user, cart__is_paid=False).count()

@receiver(post_save, sender=User)
def _post_save_receiver(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            email = instance.username
            Profile.objects.create(user=instance, email_token=email_token)
            send_account_activation_mail(email, email_token)
    except Exception as e:
        messages.error( "Account activation failed due to : ", e)









    

