# Generated by Django 4.1 on 2022-09-29 05:09

import datetime
from django.db import migrations, models
import lastSeenRP.validators


class Migration(migrations.Migration):

    dependencies = [
        ('lastSeenRP', '0042_alter_appearance_publish_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 29, 1, 9, 14, 568027, tzinfo=datetime.timezone.utc), verbose_name='date and time a user submitted this post'),
        ),
        migrations.AlterField(
            model_name='rpcharacter',
            name='character_last_name',
            field=models.CharField(max_length=50, validators=[lastSeenRP.validators.validate_character_last_name]),
        ),
    ]
