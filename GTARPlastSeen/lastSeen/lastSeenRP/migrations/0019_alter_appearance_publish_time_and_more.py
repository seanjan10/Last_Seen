# Generated by Django 4.1 on 2022-09-25 05:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastSeenRP', '0018_rpcharacter_character_nick_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 25, 1, 13, 15, 866389, tzinfo=datetime.timezone.utc), verbose_name='date and time a user submitted this post'),
        ),
        migrations.AlterField(
            model_name='rpcharacter',
            name='character_played_by',
            field=models.CharField(default='Unknown', max_length=50),
        ),
    ]
