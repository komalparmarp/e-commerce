from django.db import models
from order.models import Order
from cart.models import CartItem

# Create your models here.

PAYMENT_STATUS = (
    ('Fail', 'fail'),
    ('Processing', 'processing'),
    ('Complete', 'complete'),
    ('Onhold', 'onhold'),
)


class PaymentGetway(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(CartItem, on_delete=models.CASCADE, null=True, blank=True)
    transection_id = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, null=True, blank=True)