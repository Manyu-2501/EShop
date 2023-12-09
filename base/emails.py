from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_mail(email, account_token):
    subject = "Activate your EShop Account"
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to verify your account http://127.0.0.1:8000/accounts/activate/{account_token}'
    send_mail(subject, message, email_from, [email])
