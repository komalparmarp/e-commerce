# Generated by Django 4.0.2 on 2022-02-21 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_address_city_address_country_address_pincode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default='india', max_length=15),
        ),
    ]
