from django.db import models
from myapp.models import User
from cart.models import Cart, CartItem
from address.models import Address
from coupon.models import Coupon

# Create your models here.
ORDER_STATUS_CHOICES = (
    ('Created', 'created'),
    ('Paid', 'paid'),
    ('Shipped', 'shipped'),
    ('Refunded', 'refunded'),
    ('Cancelled', 'cancelled')
)


class Order(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create_order', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='update_order', null=True, blank=True)
    order_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='order_address', null=True,
                                      blank=True)
    order_cart = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='cart_order', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_created=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, null=True, blank=True)
    # coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='coupon_order', null=True, blank=True)


class OrderItem(models.Model):
    pass
