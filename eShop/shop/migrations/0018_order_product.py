# Generated by Django 4.1.3 on 2022-12-11 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_order_user_made_order_alter_order_zip_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Название товара'),
            preserve_default=False,
        ),
    ]
