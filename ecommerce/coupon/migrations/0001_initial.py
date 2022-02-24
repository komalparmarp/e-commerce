# Generated by Django 4.0.2 on 2022-02-24 12:07

import coupon.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_code', models.CharField(default=False, max_length=8, unique=True, validators=[django.core.validators.RegexValidator('^[A-Z0-9]*$', 'Only uppercase letters & numbers are allowed.')])),
                ('start_date', models.DateTimeField(validators=[coupon.models.Coupon.start_date])),
                ('expire_date', models.DateTimeField(validators=[coupon.models.Coupon.end_date])),
                ('max_limit', models.PositiveIntegerField(default=2, help_text='How Many Times Used this coupon')),
                ('per_user', models.PositiveIntegerField(default=2, help_text='How often user used this Coupon')),
                ('discount_type', models.CharField(blank=True, choices=[('P', 'percentage'), ('F', 'flat')], max_length=10, null=True)),
                ('discount_amount', models.PositiveIntegerField(default=1, help_text='what is customer discount')),
            ],
        ),
    ]