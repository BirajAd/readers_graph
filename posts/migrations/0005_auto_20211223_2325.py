# Generated by Django 3.2 on 2021-12-24 05:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20211223_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 23, 23, 25, 23, 370436)),
        ),
        migrations.AlterField(
            model_name='sharepost',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 23, 23, 25, 23, 371425)),
        ),
    ]
