from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_mail(email, email_token):
    subject = "Activate your EShop Account"
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to verify your account http://127.0.0.1:8000/accounts/activate/{email_token}'
    send_mail(subject, message, email_from, [email])

def send_password_reset_mail(email):
    subject = "Password Reset for EShop"
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to confirm reset of password'
    send_mail(subject, message, email_from, [email])