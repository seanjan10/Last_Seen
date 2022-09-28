from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
import pytz
from django.contrib import admin

# Create your models here.

class rpCharacter(models.Model):
    #potential fields to be added
    #link to the streamers twitch/facebook/youtube field
    #optional middle name/nickname field
    #link to an image of the character
    #additional linkes to their youtube/twitch if they have it
    character_first_name = models.CharField(max_length=30)
    character_nick_name = models.CharField(max_length=50, default="", blank=True)
    #currently all names except first are considered last name or nick name
    character_last_name = models.CharField(max_length=50)
    #if info about who plays a character isn't available, then display unknown
    character_played_by = models.CharField(max_length=50,  blank=True)
    character_image = models.CharField(max_length=200, blank=True)
    streamers_URL = models.CharField(max_length=60, blank=True)

    #default="https://static.wikia.nocookie.net/nopixel/images/5/5f/Placeholder.jpg"

    class Meta:
        unique_together = ["character_first_name", "character_last_name"]

    def __str__(self):
        return self.character_first_name + ', ' + self.character_nick_name + ', ' + self.character_last_name + ', ' + self.character_played_by + ', ' + self.streamers_URL + ', ' + self.character_image
    

class Appearance(models.Model):
    #future fields to be added
    #adjust twitch_clip_URL to include streamable, youtube, facebook etc. 
    #link to the clip streamers twitch/youtube/facebook
    #change times to only include UTC time
    #username of reddit user etc who submitted the appearance
    character_name = models.ForeignKey(rpCharacter, on_delete=models.CASCADE)
    twitch_clip_URL = models.CharField(max_length=100)
    date_of_appearance = models.DateTimeField('date and time that the character showed up')
    clip_Streamer = models.CharField(max_length=50) #in case the clip gets deleted they can find the streamers vod and watch
    publish_time = models.DateTimeField('date and time a user submitted this post', default= pytz.UTC.localize(datetime.now()))
    def __str__(self):
        return self.twitch_clip_URL + ', ' + self.date_of_appearance.strftime("%Y-%m-%d, %H:%M:%S") + ', ' + self.clip_Streamer + ', ' + self.publish_time.strftime("%m/%d/%Y, %H:%M:%S")
    #should change to recently appeared, or make a new func

    @admin.display(
        boolean=True,
        ordering='date_of_appearance', 
        description='recently appeared',
    )
    #try to troubleshoot why some appearances made within the past hour aren't recent but more than a day are
    #change published to recently seen
    def recently_published(self):
        now = pytz.UTC.localize(datetime.now())
        #return self.publish_time >= datetime.now() - timedelta(days=1)
        return now - timedelta(days=7) <= self.date_of_appearance <= now + timedelta(hours=1)
        #order appearances by their earliest known appearance
    class Meta:
        ordering = ('-date_of_appearance',)
    