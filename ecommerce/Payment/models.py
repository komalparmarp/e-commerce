from django.db import models
from order.models import Order
from myapp.models import User

# Create your models here.

PAYMENT_STATUS = (
    ('Fail', 'Fail'),
    ('Processing', 'Processing'),
    ('Draft', 'Draft'),
    ('Done', 'Done'),
)

PAYMENT_TYPE = (
    ('COD', 'Case on delivery'),
    ('Stripe', 'Stripe')
)


class PaymentGateway(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='stripe_payment', null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, null=True, blank=True)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE, default='Stripe')
    payment_price = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        order = Order.objects.get(id=self.order_id.id)
        self.payment_price = order.total_amount
        return super().save()
