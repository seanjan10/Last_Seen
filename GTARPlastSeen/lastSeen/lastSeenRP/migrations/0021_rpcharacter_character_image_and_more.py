# Generated by Django 4.1 on 2022-09-27 03:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastSeenRP', '0020_alter_appearance_publish_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rpcharacter',
            name='character_image',
            field=models.CharField(default='https://static.wikia.nocookie.net/nopixel/images/5/5f/Placeholder.jpg', max_length=200),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 23, 47, 6, 174376, tzinfo=datetime.timezone.utc), verbose_name='date and time a user submitted this post'),
        ),
    ]
