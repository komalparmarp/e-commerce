# Generated by Django 4.0.2 on 2022-03-16 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_invoiceitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
