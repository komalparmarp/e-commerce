from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Invoice)
class AdminInvoice(admin.ModelAdmin):
    list_display = ['user', 'order_id', 'payment_status']


@admin.register(InvoiceItem)
class AdminInvoiceItem(admin.ModelAdmin):
    list_display = ['invoice', 'product']

