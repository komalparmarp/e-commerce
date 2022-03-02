from django.db import models
from model_utils.models import TimeStampedModel
from myapp.models import Product, User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from coupon.models import Coupon


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart_user', on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(default=0.0, max_digits=100, decimal_places=2)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField(blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='coupon_cart', null=True, blank=True)
    # total_price = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
