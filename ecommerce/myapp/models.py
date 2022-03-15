from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


# Create your models here.


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


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class StoreOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    store_id = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=20, null=True, blank=True)


class Product(models.Model):
    product_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=20, null=False, blank=True)
    store_id = models.ForeignKey(StoreOwner, on_delete=models.CASCADE, null=False, blank=True, default=1)
    description = models.TextField(max_length=50)
    product_price = models.PositiveIntegerField()
    product_image = models.ImageField(blank=True, null=True)

