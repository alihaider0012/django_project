# Generated by Django 2.2.1 on 2019-07-20 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucircle', '0002_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
