# Generated by Django 3.2.15 on 2025-06-20 14:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_order_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='registered_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Зарегистрирован'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]
