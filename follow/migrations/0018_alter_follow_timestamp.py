# Generated by Django 3.2 on 2022-02-24 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follow', '0017_alter_follow_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
