# Generated by Django 4.1.3 on 2022-12-06 20:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_account_users_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='users_wishlist',
        ),
        migrations.AddField(
            model_name='product',
            name='users_wishlist',
            field=models.ManyToManyField(blank=True, related_name='user_wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
