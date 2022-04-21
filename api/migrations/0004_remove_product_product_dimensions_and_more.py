# Generated by Django 4.0.3 on 2022-04-04 08:48

import api.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_catalogue_service_region_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_dimensions',
        ),
        migrations.AddField(
            model_name='product',
            name='product_height',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='product',
            name='product_length',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='product',
            name='product_width',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(default=api.models.sku_generator, max_length=10),
        ),
    ]
