# Generated by Django 4.0 on 2022-02-09 23:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('follow', '0012_alter_follow_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 9, 23, 53, 6, 975899, tzinfo=utc)),
        ),
    ]