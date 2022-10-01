import praw
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lastSeen.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.core.exceptions import ObjectDoesNotExist

from decouple import config
from lastSeenRP.models import rpCharacter, Appearance
import pytz
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
#client_id = config('client_id')
#client_secret = config('client_secret')
#username = config('username')
#password = config('password')

redditUsername = config('redditUsername')

#bot for reddit
reddit = praw.Reddit(

    "bot1", 
    user_agent = "<NoPixelAppearanceBot 1.0> by /u/{}".format(redditUsername),
)
#print(reddit.user.me())
#for item in reddit.inbox.stream(skip_existing=False):
for mention in reddit.inbox.mentions(limit=100 ):
    print(f'{mention.author}\n{mention.body}')

    data = mention.body.split()
    #print("link id below")
    parentPost = mention.submission
    
    #print(parentPost)
    #print(parentPost.url)

    data_length = len(data)
    #print(data_length)
    data.pop(0)
    print(data[0])

    if data[0] == "create_appearance":
        data.pop(0)
        print('you selected to create an appearance')
        if len(data) == 3:
            now = pytz.UTC.localize(datetime.now())
            print(now)
            clipURL = parentPost.url

            #convert POSIX time to utc time
            appearanceTime = datetime.utcfromtimestamp(parentPost.created_utc)
            print(appearanceTime)

            user_who_submitted = mention.author
            #print(user_who_submitted)

            characterFName = data[0]
            characterLName = data[1]
            clipStreamerName = data[2]
            print(f'Created a new appearance for: First name = {characterFName}, Last Name = {characterLName}, Streamer = {clipStreamerName}')

            try:

                character = rpCharacter.objects.get(character_first_name=characterFName, character_last_name=characterLName)
                newAppeareance = Appearance(
                    character_name=character, 
                    twitch_clip_URL=clipURL, 
                    date_of_appearance=appearanceTime,
                    clip_Streamer=clipStreamerName,
                    publish_time=now)
                newAppeareance.save()
            except ObjectDoesNotExist:
                print("ERROR: The character you entered does not exist. If this character does exist then they have not been entered into the database. This can be done at www.url.com")
            

        else:
            print("ERROR: Incorrect Number of arguments. Please only provide the first and last name of the character, and the name of the channel where you clipped from. (e.g. /u/NoPixelAppearanceBot create_appearance Avon Barksdale LIRIK).\nNote: if the character has more than two names, then include the additional names in the last name and indicate the additional names with underscores in place of spaces. (e.g. /u/NoPixelAppearanceBot create_appearance Arush Patel_Santana SayeedBlack")


    elif data[0] == "recent_appearances":
        print("you selected to list the last 5 appearances of a character")


    print("-----------------------------------------")
    print("-----------------------------------------")