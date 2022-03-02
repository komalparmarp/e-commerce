from django.db import models
from myapp.models import User


# Create your models here.
class Address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    country = models.CharField(max_length=15, null=False, blank=False, default='India')
    state = models.CharField(max_length=50, null=False, blank=False, default='Gujarat')
    city = models.CharField(max_length=50, null=False, blank=False, default='Gir_Somnath')
    street_address = models.CharField(max_length=50, null=False, blank=False, default='Kodinar')
    pincode = models.PositiveIntegerField(default=False)
