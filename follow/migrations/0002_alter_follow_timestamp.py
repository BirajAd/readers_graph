# Generated by Django 3.2 on 2022-04-21 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]