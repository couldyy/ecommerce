# Generated by Django 4.1.3 on 2022-12-09 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_order_payment_method_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_quantity',
            field=models.IntegerField(default=1, verbose_name='Количество товара'),
        ),
    ]