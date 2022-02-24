# Generated by Django 4.0.2 on 2022-02-24 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupon', '0005_coupon_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='update_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
