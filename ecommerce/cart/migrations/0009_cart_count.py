# Generated by Django 4.0.2 on 2022-02-17 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='count',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]