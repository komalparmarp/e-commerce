# Generated by Django 4.0.2 on 2022-02-24 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0006_coupon_updated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
