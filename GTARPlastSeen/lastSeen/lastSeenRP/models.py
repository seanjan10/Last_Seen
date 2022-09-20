from django.db import models
from datetime import datetime

# Create your models here.

class rpCharacter(models.Model):
    character_first_name = models.CharField(max_length=30)
    character_last_name = models.CharField(max_length=45)
    character_played_by = models.CharField(max_length=50)
    def __str__(self):
        return self.character_first_name + ', ' + self.character_last_name + ', ' + self.character_played_by
    

class Appearance(models.Model):
    #character_name = models.CharField(max_length=65)
    character_name = models.ForeignKey(rpCharacter, on_delete=models.CASCADE)
    #character_played_by = models.CharField(max_length=50)
    twitch_clip_URL = models.CharField(max_length=100)
    date_of_appearance = models.DateTimeField('date and time that the character showed up')
    clip_Streamer = models.CharField(max_length=50) #in case the clip gets deleted they can find the streamers vod and watch
    publish_time = models.DateTimeField('date and time a user submitted this post', default=datetime.now)
    def __str__(self):
        return self.twitch_clip_URL + ', ' + self.date_of_appearance.strftime("%Y-%m-%d, %H:%M:%S") + ', ' + self.clip_Streamer + ', ' + self.publish_time.strftime("%m/%d/%Y, %H:%M:%S")
    def recently_published(self):
        return self.publish_time >= timezone.now() - datetime.timedelta(days=1)
    class Meta:
        ordering = ('-date_of_appearance',)
    