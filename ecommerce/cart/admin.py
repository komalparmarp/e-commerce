from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Cart)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(CartItem)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ['id', 'cart']
