# Generated by Django 4.0.2 on 2022-02-24 12:12

import coupon.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0003_alter_coupon_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateTimeField(validators=[coupon.models.Coupon.star_date]),
        ),
    ]
