# Generated by Django 2.2.1 on 2019-07-21 06:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_auto_20190720_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat_participants',
            name='chat_cleared_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 21, 11, 1, 59, 643130)),
        ),
    ]