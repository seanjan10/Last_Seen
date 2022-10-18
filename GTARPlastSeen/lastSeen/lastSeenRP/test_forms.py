from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from lastSeenRP.forms import searchForCharacter, createAppearanceForm, createCharacter

from .models import Appearance, rpCharacter

class CreateAppearanceFormTests(TestCase):
    '''sample valid form'''
    form_data = {
        'clipURL': 'https://clips.twitch.tv/SucculentFantasticBunnyKeyboardCat-LCSuRGU6vDupvOXH',
        'dateOfAppearance': timezone.now(),
        'channelName': 'BobRoss'
    }

    def test_valid_appearance_creation(self):
        '''using the sample form_data should return a valid form'''

        t_form = self.form_data.copy()
        form = createAppearanceForm(data=t_form)
        self.assertTrue(form.is_valid())
        

    def test_invalid_clip_url(self):
        '''test clipURL validators to ensure valid form submission'''
        #test if no https://
        t_form = self.form_data.copy()

        t_form['clipURL'] = 'clips.twitch.tv/SucculentFantasticBunnyKeyboardCat-LCSuRGU6vDupvOXH'
        form = createAppearanceForm(data=t_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['clipURL'], ["Please submit the full URL (including the https://)"])

        #test if invalid domain
        t_form['clipURL'] = 'www.google.com/BobRoss'
        form = createAppearanceForm(data=t_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['clipURL'], ["Clip provided is not a whitelisted URL. Whitelisted URLS included facebook, youtube, twitch or streamable"])

    def test_invalid_date_of_appearance(self):
        t_form = self.form_data.copy()

        #test if in the future by a day
        time = timezone.now() + timedelta(days=1)
        t_form['dateOfAppearance'] = time
        form = createAppearanceForm(data=t_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dateOfAppearance'], ["Appearance cannot be in the future"])

        #test if in the future by a hour
        time = timezone.now() + timedelta(hours=1)
        t_form['dateOfAppearance'] = time
        form = createAppearanceForm(data=t_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dateOfAppearance'], ["Appearance cannot be in the future"])

        #test if in the future by a minute
        time = timezone.now() + timedelta(minutes=1)
        t_form['dateOfAppearance'] = time
        form = createAppearanceForm(data=t_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dateOfAppearance'], ["Appearance cannot be in the future"])

    def test_invalid_channelName(self):
        '''test channelName validators'''

        t_form = self.form_data.copy()

        #less than 4 characters
        t_form['channelName'] = 'jj'
        form = createAppearanceForm(data=t_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['channelName'], [
            "Channel names can only be alphanumeric including underscores (cannot start with an underscore) and must have more than 3 characters"
        ])
        
        #more than 25
        t_form['channelName'] = 'jsdfadfadfjlddsfadftathadfkjhadflkj'
        form = createAppearanceForm(data=t_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['channelName'], [
            "Channel names can only be alphanumeric including underscores (cannot start with an underscore) and must have more than 3 characters"
        ])

        #start with underscore
        t_form['channelName'] = '_jsjlddsfadftathadfkjhadflkj'
        form = createAppearanceForm(data=t_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['channelName'], ["Channel names can only be alphanumeric including underscores (cannot start with an underscore) and must have more than 3 characters"
        ])

        #invalid characters
        t_form['channelName'] = 'Bob&Ross'
        form = createAppearanceForm(data=t_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['channelName'], ["Channel names can only be alphanumeric including underscores (cannot start with an underscore) and must have more than 3 characters"
        ])

class SearchForCharacterTests(TestCase):
    
    def test_invalid_search_query(self):
        '''currently no validator, just verify max length is below 60'''
        form_data = {"searchQuery": "this is a very long querry test test test teest tests test test test test test test"}
        form = searchForCharacter(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['searchQuery'], [
            f"Ensure this value has at most 60 characters (it has {len(form_data['searchQuery'])})."
        ])
    
def create_character(char_fname, char_nname, char_lname, char_play_by, char_image, char_streamurl):
    return rpCharacter.objects.create(character_first_name=char_fname, character_nick_name=char_nname, character_last_name=char_lname, character_played_by=char_play_by, character_image=char_image, streamers_URL=char_streamurl)

def create_appearance(character, twitch_clip_URL, time_unit, clip_Streamer, publish_time, submittedBy):
    time = timezone.now() + timedelta(days=time_unit)
    return Appearance.objects.create(character_name=character, twitch_clip_URL=twitch_clip_URL, date_of_appearance=time, clip_Streamer=clip_Streamer, publish_time=publish_time, submittedBy=submittedBy)