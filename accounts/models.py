from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.emails import send_account_activation_mail
from django.contrib import messages
import uuid
# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    profile_picture = models.ImageField(upload_to='profiles', default = 'profiles/no_image')
    is_email_verified = models.BooleanField(default = False)
    email_token = models.CharField(max_length=100)

@receiver(post_save, sender=User)
def _post_save_receiver(sender, instance, created, **kwargs):
    try:
        if created:
            account_token = str(uuid.uuid4)
            email = instance.username
            profile = Profile.objects.create(user=instance, email_token=account_token)
            send_account_activation_mail(email, account_token)
    except Exception as e:
        messages.error( "Account activation failed due to : ", e)





    

