from django.db import models
from myapp.models import User
from cart.models import Cart, CartItem
from address.models import Address


# Create your models here.
class Order(models.Model):
    item = models.CharField(max_length=50, null=True, blank=True)
    customer = models.ForeignKey(User, related_name='customer_order', on_delete=models.CASCADE, null=True, blank=True)
    order_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='order_address', null=True,
                                      blank=True)
    order_cart = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='cart_order', null=True, blank=True)
