# Generated by Django 3.0.4 on 2020-03-28 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryMS', '0002_bookborrowed_bookhold'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookhold',
            name='available',
            field=models.SmallIntegerField(default=0),
        ),
    ]
