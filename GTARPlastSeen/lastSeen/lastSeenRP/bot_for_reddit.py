import praw
import os
from decouple import config
from lastSeenRP.models import rpCharacter, Appearance
import pytz
from datetime import datetime
from django.shortcuts import get_object_or_404
#client_id = config('client_id')
#client_secret = config('client_secret')
#username = config('username')
#password = config('password')


#bot for reddit
reddit = praw.Reddit(

    "bot1", 
    user_agent = "<NoPixelAppearanceBot 1.0> by /u/DeadlyPirate",
)

for item in reddit.inbox.stream(skip_existing=False):
    print(item.subject, flush=True)
    print()
    print(item.body, flush=True)

    data = item.body.replace("\_", "_").split()

    if item.subject == "username mention":
        data.pop(0)
        #print('popped succesfully', flush=True)

    #print(len(data))
    data_length = len(data)

    if len(data) == data_length:
        character_id = get_object_or_404(rpCharacter, character_first_name=data[0], character_last_name=data[1], character_played_by=data[2])
        #character = rpCharacter(character_first_name=data[0], character_last_name=data[1], character_played_by=data[2])
        a = Appearance(character_name=character_id, twitch_clip_URL=data[3], date_of_appearance=pytz.UTC.localize(datetime.now()), clip_Streamer=data[5], publish_time=pytz.UTC.localize(datetime.now()))
        a.save()
        #print("charcter_first_name = {fname}, \n character_last_name = {lname}, \ncharacter_played_by = {played_by}\n, twitch_clip_URL = {clipURL}\n, date_of_appearance = {appearanceDate}\n, clip_Streamer = {streamerClip}\n, publish_time = {publishTime}".format(fname=data[0], lname=data[1], played_by=data[2], clipURL=data[3], appearanceDate=data[4], streamerClip=data[5], publishTime=data[6]), flush=True)
    elif len(data) > data_length:
        print("Error: too many arguments submitted")
    else:
        print("Error: not enough arguments submitted")
        