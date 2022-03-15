from django.db import models
from cart.models import CartItem, Cart
from myapp.models import Product, User
from address.models import Address


# Create your models here.
class CheckOut(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    cart = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='cart_user', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='add', null=True, blank=True)
