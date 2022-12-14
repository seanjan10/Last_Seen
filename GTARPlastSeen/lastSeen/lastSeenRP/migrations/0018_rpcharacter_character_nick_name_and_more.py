# Generated by Django 4.1 on 2022-09-25 02:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastSeenRP', '0017_alter_appearance_publish_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='rpcharacter',
            name='character_nick_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='rpcharacter',
            name='streamers_URL',
            field=models.CharField(default='Unknown', max_length=60),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 24, 22, 40, 57, 255467, tzinfo=datetime.timezone.utc), verbose_name='date and time a user submitted this post'),
        ),
        migrations.AlterField(
            model_name='rpcharacter',
            name='character_last_name',
            field=models.CharField(max_length=50),
        ),
    ]
