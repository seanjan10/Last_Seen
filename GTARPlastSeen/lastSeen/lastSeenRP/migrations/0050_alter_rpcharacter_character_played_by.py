# Generated by Django 4.1.1 on 2022-10-18 02:28

from django.db import migrations, models
import lastSeenRP.validators


class Migration(migrations.Migration):

    dependencies = [
        ('lastSeenRP', '0049_alter_appearance_publish_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpcharacter',
            name='character_played_by',
            field=models.CharField(blank=True, max_length=50, validators=[lastSeenRP.validators.validate_channel_name]),
        ),
    ]
