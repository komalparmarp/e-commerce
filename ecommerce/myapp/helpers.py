from django.core.mail import send_mail
import uuid
from django.conf import settings


def send_forgot_password_email(email,token):
    subject = "Your  forgot password link"
    message = f'hi,click link to forgot ur password http://127.0.0.1:8000/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

    return True
