# Generated by Django 4.1.3 on 2022-12-06 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_remove_account_users_wishlist_product_users_wishlist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WishList',
        ),
    ]
