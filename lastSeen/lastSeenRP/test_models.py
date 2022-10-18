from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError


from .models import Appearance, rpCharacter


class ModelTests(TestCase):

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

    def test_valid_character(self):
        '''valid character follows all constraints of the validators'''

        #all valid fields
        first_name = 'Bob'
        last_name = 'Joe'
        nick_name = '\"Tiger\"'
        image = 'https://static.wikia.nocookie.net/scoobydoo/images/2/28/Billy_Bob_Joe_Bob_Harris.png'
        played_by = "BillyJoe"
        url = 'https://www.twitch.tv/BobRoss'
        character = rpCharacter(character_first_name=first_name, character_last_name=last_name, character_nick_name=nick_name, character_image=image, character_played_by=played_by, streamers_URL=url)
        character.full_clean()

        #underscore connecting last name
        last_name = 'Joe_Jean_III'
        character.character_last_name = last_name
        character.full_clean()


    def test_character_first_name_invalid_char(self):
        '''first name is invalid if it includes non alphanumeric characters except - . ' _  '''

        #invalid char
        first_name = "Bob#"
        last_name = "Joe"
        character = rpCharacter(character_first_name=first_name, character_last_name=last_name)
        with self.assertRaises(ValidationError):
            character.full_clean()

        #space in first name
        first_name = "Bob Jean"
        character.character_first_name = first_name
        with self.assertRaises(ValidationError):
            character.full_clean()

    def test_character_last_name_invalid_char(self):
        '''last name is invalid if it includes non alphanumeric characters except - . ' _  '''

        #invalid char
        first_name = "Bob"
        last_name = "Joe@"
        character = rpCharacter(character_first_name=first_name, character_last_name=last_name)
        with self.assertRaises(ValidationError):
            character.full_clean()
        
        #space in last name
        last_name = "Joe Jean"
        character.character_last_name = last_name
        with self.assertRaises(ValidationError):
            character.full_clean()

    def test_character_nick_name_invalid_char(self):
        '''last name is invalid if it includes non alphanumeric characters except - . ' _  '''
        #invalid char
        first_name = "Bob"
        last_name = "Joe"
        nick_name = "\"Cho*p\""
        character = rpCharacter(character_first_name=first_name, character_nick_name=nick_name, character_last_name=last_name)
        with self.assertRaises(ValidationError):
            character.full_clean()

        #no surrounding quotation marks
        nick_name = "Chop"
        character.character_nick_name = nick_name
        with self.assertRaises(ValidationError):
            character.full_clean()

    def test_character_played_by_invalid_requirements(self):
        '''played by is invalid if it includes non alphanumeric characters except _ and cannot lead with it. also name can only be between 4-25 characters  '''
        #leading underscore
        first_name = "Bob"
        last_name = "Joe"
        played_by = "_joejj"
        character = rpCharacter(character_first_name=first_name, character_last_name=last_name, character_played_by=played_by)
        with self.assertRaises(ValidationError):
            character.full_clean()

        #less than 4 chars
        played_by = "jj"
        character.character_played_by = played_by
        with self.assertRaises(ValidationError):
            character.full_clean()

        #more than 25 chars
        played_by = "jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj"
        character.character_played_by = played_by
        with self.assertRaises(ValidationError):
            character.full_clean()

    def test_character_image_invalid(self):
        '''character image is invalid if it has the incorrect file extension at the end or missing the https:// '''
        #no https
        first_name = "Bob"
        last_name = "Joe"
        image = 'static.wikia.nocookie.net/nopixel/images/9/91/ConanLT.png'
        character = rpCharacter(character_first_name=first_name, character_last_name=last_name, character_image=image)
        with self.assertRaises(ValidationError):
            character.full_clean()

        #unsupported file extension
        image = 'https://static.wikia.nocookie.net/nopixel/images/9/91/ConanLT.tiff'
        character.character_image = image
        with self.assertRaises(ValidationError):
            character.full_clean()

    def test_character_streamer_url_invalid(self):
        '''streamer url is invalid if link submitted is not a supported website or missing https://'''
        #missing https
        first_name = "Bob"
        last_name = "Joe"
        url = 'twitch.tv/BobRoss'
        character = rpCharacter(character_first_name=first_name, character_last_name=last_name, streamers_URL=url)
        with self.assertRaises(ValidationError):
            character.full_clean()

        #unsupported file extension
        url = 'https://www.google.com/BobRoss'
        character.streamers_URL = url
        with self.assertRaises(ValidationError):
            character.full_clean()


def create_character(char_fname, char_nname, char_lname, char_play_by, char_image, char_streamurl):
    return rpCharacter.objects.create(character_first_name=char_fname, character_nick_name=char_nname, character_last_name=char_lname, character_played_by=char_play_by, character_image=char_image, streamers_URL=char_streamurl)

def create_appearance(character, twitch_clip_URL, time_unit, clip_Streamer, publish_time, submittedBy):
    time = timezone.now() + timedelta(days=time_unit)
    return Appearance.objects.create(character_name=character, twitch_clip_URL=twitch_clip_URL, date_of_appearance=time, clip_Streamer=clip_Streamer, publish_time=publish_time, submittedBy=submittedBy)