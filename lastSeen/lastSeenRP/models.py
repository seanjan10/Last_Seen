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
    character_first_name = models.CharField(max_length=30)
    character_last_name = models.CharField(max_length=45)
    character_played_by = models.CharField(max_length=50)
    def __str__(self):
        return self.character_first_name + ', ' + self.character_last_name + ', ' + self.character_played_by
    

class Appearance(models.Model):
    #character_name = models.CharField(max_length=65)
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
    def recently_published(self):
        now = pytz.UTC.localize(datetime.now())
        #return self.publish_time >= datetime.now() - timedelta(days=1)
        return now - timedelta(days=7) <= self.date_of_appearance <= now + timedelta(hours=1)
    class Meta:
        ordering = ('-date_of_appearance',)
    