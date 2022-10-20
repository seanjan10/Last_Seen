from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from .models import Appearance, rpCharacter

class IndexViewTests(TestCase):

    def test_valid_index_no_characters(self):
        '''test to see if html returns no characters available if there are not entries in the db'''
        response = self.client.get("/lastSeenRP/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<p> No characters are available. </p>', html=True)

    def test_valid_index_character(self):
        '''test to see if html returns an index with characters in the db'''
        create_character('Bob', '\"Ross\"', 'Joe', 'BobRoss', '', '')
        create_character('Billy', '', 'Heel', '', '', '')
        response = self.client.get("/lastSeenRP/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, '<p> No characters are available. </p>', html=True)


class CharacterViewTests(TestCase):

    def test_valid_character(self):
        #normal name
        create_character("Bob", '', 'Joe', '', '', '')
        response = self.client.get('/lastSeenRP/character/Bob_Joe/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<h1> Bob Joe </h1>', html=True)

        #underscore last name
        create_character("Bob", '', 'Joe_Smith_Jacob', '', '', '')
        response = self.client.get('/lastSeenRP/character/Bob_Joe_Smith_Jacob/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<h1> Bob Joe Smith Jacob </h1>', html=True)

    def test_valid_character_appearance(self):
        create_character("Bob", '', 'Joe', '', '', '')
        character = get_object_or_404(rpCharacter, character_first_name="Bob", character_last_name="Joe")
        time = timezone.now()
        timeAppear = timezone.now() - timedelta(days=3)
        create_appearance(character, 'https://clips.twitch.tv/TrustworthyPlacidAntelopePanicBasket-f6ZxpXFVSw6hxI3J',timeAppear , 'BobRoss', time)
        response = self.client.get('/lastSeenRP/character/Bob_Joe/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, f'<li> appeared on {timeAppear} on <a href="https://clips.twitch.tv/TrustworthyPlacidAntelopePanicBasket-f6ZxpXFVSw6hxI3J" target="_blank"> BobRoss\'s</a> stream. <i>Updated at {time} </i>', html=True)



def create_character(char_fname, char_nname, char_lname, char_play_by, char_image, char_streamurl):
    return rpCharacter.objects.create(character_first_name=char_fname, character_nick_name=char_nname, character_last_name=char_lname, character_played_by=char_play_by, character_image=char_image, streamers_URL=char_streamurl)

def create_appearance(character, twitch_clip_URL, time_unit, clip_Streamer, publish_time):
    #time = timezone.now() - timedelta(days=time_unit)
    return Appearance.objects.create(character_name=character, twitch_clip_URL=twitch_clip_URL, date_of_appearance=time_unit, clip_Streamer=clip_Streamer, publish_time=publish_time)