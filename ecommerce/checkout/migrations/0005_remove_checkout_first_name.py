# Generated by Django 4.0.2 on 2022-02-23 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_checkout_address_alter_checkout_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='first_name',
        ),
    ]