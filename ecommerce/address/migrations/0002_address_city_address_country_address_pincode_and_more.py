# Generated by Django 4.0.2 on 2022-02-21 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default=False, max_length=50),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(default=False, max_length=15),
        ),
        migrations.AddField(
            model_name='address',
            name='pincode',
            field=models.PositiveIntegerField(default=False),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(default=False, max_length=50),
        ),
        migrations.AddField(
            model_name='address',
            name='street_address',
            field=models.CharField(default=False, max_length=50),
        ),
    ]
