# Generated by Django 4.0.2 on 2022-02-11 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_customer_name_storeowner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeowner',
            name='store_id',
        ),
    ]
