from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

# Create your models here.
PRODUCT_CHOICES = (('', ''),
                   ('Saree', 'saree'),
                   ('Shirt', 'shirt'),
                   ('Jeans', 'jeans'),
                   ('Top', 'top'),
                   ('Dress', 'dress'),
                   ('Kurta', 'kurta'),
                   ('Plaza', 'plaza'))

STATE_CHOICES = (("", ""),
                 ("Gujarat", "gujarat"),
                 ("Maharastra", "maharastra"),
                 ("Delhi", "delhi"))

CITY_CHOICES = (("", ""), ("Ahemdabad", "ahemdabad"),
                ("Gandhinagar", "gandhinagar"),
                ("Baroda", "baroda"),
                ("Surat", "surat"),
                ("Delhi", "delhi"),
                ("Rajkot", "rajkot"),
                ("Bhavnagar", "bhavnagar"),
                ("Mumbai", "mumbai"),
                ("Somnath", "Somnath"),)

DISCOUNT_CHOICES = (('percentage', 'Percentage'), ('flat', 'Flat'))

PYMENT_CHOICES = (("UPI_ID", "upi_id"),
                  ("GOOGLE_PAY", "google_pay"),
                  ("COD", "caseondelivery"),
                  ("AMAZON_PAY", "amazon_pay"),
                  )

USER_TYPE_CHOICES = (('1', 'is_customer'), ('2', 'is_store_owner'),)


class User(AbstractUser):
    first_name = models.CharField(max_length=10, null=False, blank=False)
    last_name = models.CharField(max_length=10, null=False, blank=False)
    phone_number = PhoneNumberField(null=True, blank=True, default="9999999999")
    email = models.EmailField(null=False, blank=False)
    password = models.CharField(max_length=8, null=False, blank=False, default=0,
                                validators=[RegexValidator(
                                    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
                                    "Minimum Eight Character,One Upper case,One lowercase,One number,and One special character like a @#$")])
    forgot_password_token = models.CharField(max_length=100, null=True, blank=True)
    is_customer = models.BooleanField(default=False)
    is_store_owner = models.BooleanField(default=False)


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
#                                                    reset_password_token.key)
#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#
#         "komal612412@gmail.com",
#         # to:
#         [reset_password_token.user.email]
#     )
#

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class StoreOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    store_id = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=20, null=True, blank=True)


class Discount(models.Model):
    discount_id = models.PositiveIntegerField(blank=False, null=False)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES, default='flat')
    discount_price = models.PositiveIntegerField()


class Product(models.Model):
    product_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=20, null=False, blank=True)
    store_id = models.ForeignKey(StoreOwner, on_delete=models.CASCADE, null=False, blank=True, default=1)
    description = models.TextField(max_length=50)
    product_price = models.PositiveIntegerField()
    # discount_id = models.ForeignKey(Discount, on_delete=models.CASCADE, default=1)
    product_image = models.ImageField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
