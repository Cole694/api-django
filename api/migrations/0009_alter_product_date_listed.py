# Generated by Django 4.0.3 on 2022-05-31 09:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_product_date_listed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_listed',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 9, 0), max_length=225),
        ),
    ]
