# Generated by Django 2.2.1 on 2019-08-06 17:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0023_auto_20190806_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat_participants',
            name='chat_cleared_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 6, 22, 40, 50, 865723)),
        ),
    ]
