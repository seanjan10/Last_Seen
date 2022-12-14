# Generated by Django 4.1 on 2022-09-29 03:39

import datetime
from django.db import migrations, models
import lastSeenRP.validators


class Migration(migrations.Migration):

    dependencies = [
        ('lastSeenRP', '0036_alter_appearance_publish_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 28, 23, 39, 43, 617941, tzinfo=datetime.timezone.utc), verbose_name='date and time a user submitted this post'),
        ),
        migrations.AlterField(
            model_name='rpcharacter',
            name='character_image',
            field=models.URLField(blank=True, validators=[lastSeenRP.validators.validate_character_image]),
        ),
    ]
