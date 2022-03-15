from django.db import models
from myapp.models import User
from coupon.models import Coupon
from myapp.models import Product

# Create your models here.
ORDER_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
    ('Shipped', 'shipped'),
    ('Cancelled', 'cancelled')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create_order', null=True, blank=True)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, default='Pending', max_length=100)
    total_amount = models.FloatField(blank=True)

    def _get_total_amount(self):
        items = self.order_items.all()
        total = 0
        for i in items:
            total += i.total__price
        return total

    total_amount = property(_get_total_amount)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField(blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='order_items', null=True, blank=True)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)

    def _get_total_price(self):
        return self.total_price

    total__price = property(_get_total_price)

    def __str__(self):
        return f"{self.user} - {self.product} - {self.order.id}"
