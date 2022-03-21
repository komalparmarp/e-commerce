from django.db import models
from myapp.models import User
from order.models import Order
from Payment.models import PaymentGateway
from myapp.models import Product


# Create your models here.
class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_user')
    order_id = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20)
    total_amount = models.FloatField(default=250.50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_invoice')
    product_amount = models.FloatField(default=0)
