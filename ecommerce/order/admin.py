from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'total_amount']


@admin.register(OrderItem)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ['id', 'order', 'total_price']
