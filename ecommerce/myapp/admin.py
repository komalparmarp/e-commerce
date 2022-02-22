from django.contrib import admin
from .models import *

# from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Customer)
admin.site.register(StoreOwner)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Discount)


# admin.site.register(Discount)
# admin.site.register(Order)
# admin.site.register(Cart)
# admin.site.register(Invoice)
# admin.site.register(Address)
# admin.site.register(Store)
# admin.site.register(InvoiceItem)
# admin.site.register(Employee)
# admin.site.register(OrderItem)
# admin.site.register(Payment)
