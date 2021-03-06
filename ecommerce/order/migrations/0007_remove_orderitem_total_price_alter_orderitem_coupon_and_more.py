# Generated by Django 4.0.2 on 2022-03-14 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0020_remove_product_quantity'),
        ('coupon', '0001_initial'),
        ('order', '0006_remove_order_total_amount_remove_orderitem_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='coupon.coupon'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='myapp.product'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to=settings.AUTH_USER_MODEL),
        ),
    ]
