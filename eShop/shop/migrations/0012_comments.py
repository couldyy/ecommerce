# Generated by Django 4.1.3 on 2022-12-08 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_product_users_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Текст комментария')),
                ('product_of_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_comment', to='shop.product')),
                ('user_posted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL, verbose_name='Имя пользователя')),
            ],
        ),
    ]
