# Generated by Django 4.0 on 2021-12-22 04:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('follow', '0003_alter_follow_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 22, 4, 22, 5, 267704, tzinfo=utc)),
        ),
    ]
