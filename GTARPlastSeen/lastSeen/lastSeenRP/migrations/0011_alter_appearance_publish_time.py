# Generated by Django 4.1 on 2022-09-21 00:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastSeenRP', '0010_alter_appearance_publish_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 20, 37, 16, 906265), verbose_name='date and time a user submitted this post'),
        ),
    ]
