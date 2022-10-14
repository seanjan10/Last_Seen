# Generated by Django 4.1 on 2022-09-28 02:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastSeenRP', '0021_rpcharacter_character_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 22, 56, 9, 596850, tzinfo=datetime.timezone.utc), verbose_name='date and time a user submitted this post'),
        ),
        migrations.AlterField(
            model_name='rpcharacter',
            name='character_image',
            field=models.CharField(blank=True, default='https://static.wikia.nocookie.net/nopixel/images/5/5f/Placeholder.jpg', max_length=200),
        ),
    ]