# Generated by Django 3.2 on 2022-02-24 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_auto_20220217_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sharepost',
            name='date',
            field=models.DateTimeField(),
        ),
    ]