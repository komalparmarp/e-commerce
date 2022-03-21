# Generated by Django 4.0.2 on 2022-03-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='order_id',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_method',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_amount',
            field=models.FloatField(default=250.5),
        ),
    ]
