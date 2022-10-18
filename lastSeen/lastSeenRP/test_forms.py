from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse


from .models import Appearance, rpCharacter

def create_character(char_fname, char_nname, char_lname, char_play_by, char_image, char_streamurl):
    return rpCharacter.objects.create(character_first_name=char_fname, character_nick_name=char_nname, character_last_name=char_lname, character_played_by=char_play_by, character_image=char_image, streamers_URL=char_streamurl)

def create_appearance(character, twitch_clip_URL, time_unit, clip_Streamer, publish_time, submittedBy):
    time = timezone.now() + timedelta(days=time_unit)
    return Appearance.objects.create(character_name=character, twitch_clip_URL=twitch_clip_URL, date_of_appearance=time, clip_Streamer=clip_Streamer, publish_time=publish_time, submittedBy=submittedBy)