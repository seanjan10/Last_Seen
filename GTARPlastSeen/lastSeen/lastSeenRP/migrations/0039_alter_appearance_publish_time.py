# Generated by Django 4.1 on 2022-09-29 04:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastSeenRP', '0038_alter_appearance_publish_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 29, 0, 5, 40, 67618, tzinfo=datetime.timezone.utc), verbose_name='date and time a user submitted this post'),
        ),
    ]
