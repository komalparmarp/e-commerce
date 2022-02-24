from django.db import models

from django.core.validators import RegexValidator

from django.utils import timezone
from django.core.exceptions import ValidationError
from myapp.models import User

# Create your models here.
DISCOUNT_TYPE = (("P", "percentage"), ('F', 'flat'))


class Coupon(models.Model):
    def star_date(value):
        if value >= timezone.now():
            raise ValidationError("You don't put Future-date here")

    def end_date(end):
        if end < timezone.now():
            raise ValidationError("You don't put Past-date here")

    promo_code = models.CharField(max_length=8, unique=True, validators=[
        RegexValidator("^[A-Z0-9]*$", "Only uppercase letters & numbers are allowed.")], default=False)

    start_date = models.DateTimeField(null=False, blank=False, validators=[star_date])
    expire_date = models.DateTimeField(null=False, blank=False, validators=[end_date])
    max_limit = models.PositiveIntegerField(help_text="How Many Times Used this coupon", default=2)
    per_user = models.PositiveIntegerField(help_text="How often user used this Coupon", default=2)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE, null=True, blank=True)
    discount_amount = models.PositiveIntegerField(help_text="what is customer discount", default=1)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_user', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='update_user', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
