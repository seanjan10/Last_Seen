from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse


from .models import Appearance, rpCharacter
# Create your tests here.

class AppearanceModelTests(TestCase):

    def test_appearance_is_before_right_now(self):
        ''' form should not accept appearances of a character that appear in the future '''

        time = datetime.now() + timedelta(days=30)
        future_appearance = Appearance(date_of_appearance=time)
        self.assertIs(future_appearance.recently_published(), False)

    def test_was_published_recently_with_old_appearance(self):
        '''was_published_recently() returns False for appearances that were published more than a day ago'''

        time = datetime.now() - timedelta(days=1, hours=1)
        old_appearance = Appearance(date_of_appearance=time)
        self.assertIs(old_appearance.recently_published(), False)


    def test_was_published_recently_with_recent_appearance(self):
        '''was_published_recently() returns True for appearances that were published within the last day'''

        time = datetime.now()
        recent_appearance = Appearance(date_of_appearance=time)
        self.assertIs(recent_appearance.recently_published(), True)

def create_character(char_fname, char_lname, char_play_by):
    return rpCharacter.objects.create(character_first_name=char_fname, character_last_name=char_lname, character_played_by=char_play_by)

def create_appearance(character, twitch_clip_URL, days, clip_Streamer, publish_time):
    time = datetime.now() + timedelta(days=days)
    return Appearance.objects.create(character_name=character, twitch_clip_URL=twitch_clip_URL, date_of_appearance=time, clip_Streamer=clip_Streamer, publish_time=publish_time)

class AppearanceViewTests(TestCase):
    
    def test_no_appearances(self): 
        '''return a message to the user saying that there are no messages'''
        character = create_character('bob', 'joe', 'BOOMER')
        response = self.client.get(reverse('lastSeenRP:character', args=(character.character_first_name, character.character_last_name)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This character has no appearances in the database. Would you like to create one?")
        #self.assertQuerysetEqual(response.context['character_id'], [])

    