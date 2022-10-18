from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError


from .models import Appearance, rpCharacter


class AppearanceModelTests(TestCase):

    #====== recently_appeared =====

    def test_appearance_is_before_right_now(self):
        '''form should not accept appearances of a character that appear in the future '''
        time = timezone.now() + timedelta(days=30)
        future_appearance = Appearance(date_of_appearance=time)
        self.assertIs(future_appearance.recently_appeared(), False)

    def test_was_appeared_recently_with_old_appearance(self):
        '''recently_appeared() returns False for appearances that were published more than a week ago'''
        time = timezone.now() - timedelta(days=7, hours=1)
        old_appearance = Appearance(date_of_appearance=time)
        self.assertIs(old_appearance.recently_appeared(), False)

    def test_was_appeared_recently_with_three_day_appearance(self):
        '''recently_appeared() returns True for appearances that were published less than a week ago'''
        time = timezone.now() - timedelta(days=3)
        old_appearance = Appearance(date_of_appearance=time)
        self.assertIs(old_appearance.recently_appeared(), True)

    def test_was_appeared_recently_with_recent_appearance(self):
        '''recently_appeared() returns True for appearances that were published within the last day'''
        time = timezone.now()
        recent_appearance = Appearance(date_of_appearance=time)
        self.assertIs(recent_appearance.recently_published(), True)

    #===== recently_published =====

    def test_recently_published_is_before_right_now(self):
        '''form should not accept publishes of a character that appear in the future '''
        time = timezone.now() + timedelta(days=30)
        future_publish = Appearance(publish_time=time)
        self.assertIs(future_publish.recently_published(), False)

    def test_was_published_recently_with_old_publish(self):
        '''published_recently() returns False for appearances that were published more than a week ago'''
        time = timezone.now() - timedelta(days=7, hours=1)
        old_publish = Appearance(publish_time=time)
        self.assertIs(old_publish.recently_published(), False)


    def test_was_published_recently_with_three_day_publish(self):
        '''published_recently() returns True for appearances that were published less than a week ago'''
        time = timezone.now() - timedelta(days=3)
        old_publish = Appearance(publish_time=time)
        self.assertIs(old_publish.recently_published(), True)


    def test_was_published_recently_with_recent_publish(self):
        '''published_recently() returns True for appearances that were published within the last day'''
        time = timezone.now()
        recent_publish = Appearance(publish_time=time)
        self.assertIs(recent_publish.recently_published(), True)



    #===== validators check =====

    def test_character_first_name_valid(self):
        '''valid first name includes alphanumeric characters'''
        first_name = "Bob#"
        last_name = "Joe"
        character = rpCharacter(character_first_name=first_name, character_last_name=last_name)
        with self.assertRaises(ValidationError):
            character.full_clean()

    def test_character_last_name_valid(self):
        '''valid last name includes alphanumeric characters'''
        first_name = "Bob"
        last_name = "Joe@"
        character = rpCharacter(character_first_name=first_name, character_last_name=last_name)
        with self.assertRaises(ValidationError):
            character.full_clean()





def create_character(char_fname, char_nname, char_lname, char_play_by, char_image, char_streamurl):
    return rpCharacter.objects.create(character_first_name=char_fname, character_nick_name=char_nname, character_last_name=char_lname, character_played_by=char_play_by, character_image=char_image, streamers_URL=char_streamurl)

def create_appearance(character, twitch_clip_URL, time_unit, clip_Streamer, publish_time, submittedBy):
    time = timezone.now() + timedelta(days=time_unit)
    return Appearance.objects.create(character_name=character, twitch_clip_URL=twitch_clip_URL, date_of_appearance=time, clip_Streamer=clip_Streamer, publish_time=publish_time, submittedBy=submittedBy)