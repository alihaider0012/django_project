# Generated by Django 2.2.1 on 2019-07-02 00:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20190702_0521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat_messages',
            name='msg_created_at',
        ),
        migrations.AlterField(
            model_name='chat_participants',
            name='chat_cleared_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 2, 5, 40, 1, 249390)),
        ),
    ]
