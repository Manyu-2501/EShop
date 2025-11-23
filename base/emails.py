from django.conf import settings
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def send_account_activation_mail(email, email_token):
    subject = "Activate your EShop Account"
    email_from = settings.EMAIL_HOST_USER
    activation_link = f"{settings.BASE_URL.rstrip('/')}/accounts/activate/{email_token}"
    message = f"Hi,\n\nClick the link to verify your account:\n{activation_link}\n\nIf you didn't sign up, ignore this email."
    try:
        send_mail(subject, message, email_from, [email])
    except Exception as e:
        logger.exception("Failed to send account activation email to %s", email)
        raise

def send_password_reset_mail(email, email_token):
    subject = "Password Reset for EShop"
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, \n\nclick on the link to reset your password: {settings.BASE_URL.rstrip("/")}/accounts/reset-password/{email_token}\n\nIf you did not request a password reset, please ignore this email.'
    send_mail(subject, message, email_from, [email])