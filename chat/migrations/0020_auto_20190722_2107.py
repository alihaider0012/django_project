# Generated by Django 2.2.1 on 2019-07-22 16:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0019_auto_20190721_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat_participants',
            name='chat_cleared_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 22, 21, 7, 31, 669865)),
        ),
    ]