# Generated by Django 3.0.4 on 2020-03-22 12:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200320_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 22, 18, 8, 45, 736782)),
        ),
    ]
