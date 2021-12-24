# Generated by Django 3.2 on 2021-12-24 07:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_auto_20211224_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 24, 1, 5, 11, 374867)),
        ),
        migrations.AlterField(
            model_name='sharepost',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 24, 1, 5, 11, 374867)),
        ),
        migrations.AlterField(
            model_name='sharepost',
            name='list_authors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
