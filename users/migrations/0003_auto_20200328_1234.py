# Generated by Django 3.0.4 on 2020-03-28 07:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200327_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 12, 34, 13, 954130)),
        ),
    ]
