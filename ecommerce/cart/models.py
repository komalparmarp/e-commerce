from django.db import models
from myapp.models import Product, User
from coupon.models import Coupon


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart_user', on_delete=models.CASCADE, null=True, blank=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField(blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='coupon_cart', null=True, blank=True)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
