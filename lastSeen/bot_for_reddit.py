import praw
import os
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lastSeen.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import quote_plus
from decouple import config
from lastSeenRP.models import rpCharacter, Appearance
import pytz
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

#global vars
redditUsername = config('redditUsername')
endString = f"\n\n*This action was automated by a bot. It has no affiliation to the Staff or Owner of NoPixel. You can contact the owner of this bot [here.](https://www.reddit.com/user/{redditUsername})*"

def redditResponseToRecentAppearances(data, mention):
    data.pop(0)
    print("you selected to list the last 5 appearances of a character")




def redditResponseToCreateAppearance(data, parentPost, mention):
    #remove from list since no longer necessary
    data.pop(0)
    print('you selected to create an appearance')
    if len(data) == 3:
        now = pytz.UTC.localize(datetime.now())
        clipURL = parentPost.url

        #check if whitelisted url
        if validClipURL(clipURL) == False:
            mention.reply(body=f'ERROR: supported clip URLS include twitch, youtube, facebook and streamable.{endString}')
            mention.save()
            return

        #should not need to check appearance as reddit posts cannot be posted in the future

        #convert POSIX time to utc time
        appearanceTime = datetime.utcfromtimestamp(parentPost.created_utc)
        user_who_submitted = mention.author
        characterFName = data[0]
        characterLName = data[1]
        clipStreamerName = data[2]
        print(f'Created a new appearance for: First name = {characterFName}, Last Name = {characterLName}, Streamer = {clipStreamerName}')

        try:
            appearance = createAppearance(characterFName, characterLName, clipURL, appearanceTime, clipStreamerName, now)
        except ObjectDoesNotExist:
            #print("ERROR: The character you entered does not exist. If this character does exist then they have not been entered into the database. This can be done at www.url.com")
            mention.reply(body=f"ERROR: The character you entered does not exist. If this character does exist then they have not been entered into the database. This can be done at www.url.com{endString}")
            mention.save()
            return
        reply_template = f"New appearance created for {characterFName} {characterLName}! View other appearances by this character [HERE.](http://127.0.0.1:8000/lastSeenRP/character/{characterFName}_{characterLName}/){endString}"
        mention.reply(body=reply_template)
        mention.save()
    else:
        #print("ERROR: Incorrect Number of arguments. Please only provide the first and last name of the character, and the name of the channel where you clipped from. (e.g. /u/NoPixelAppearanceBot create_appearance Avon Barksdale LIRIK).\nNote: if the character has more than two names, then include the additional names in the last name and indicate the additional names with underscores in place of spaces. (e.g. /u/NoPixelAppearanceBot create_appearance Arush Patel_Santana SayeedBlack")
        mention.reply(body=f"ERROR: Incorrect Number of arguments. Please only provide the first and last name of the character, and the name of the channel where you clipped from. (e.g. /u/NoPixelAppearanceBot create_appearance Avon Barksdale LIRIK).\nNote: if the character has more than two names, then include the additional names in the last name and indicate the additional names with underscores in place of spaces. (e.g. /u/NoPixelAppearanceBot create_appearance Arush Patel_Santana SayeedBlack{endString}")
        mention.save()
    

#function to create a valid appearance
def createAppearance(firstName, lastName, clipURL, appearanceTime, clipStreamerName, publishTime):
    character = rpCharacter.objects.get(character_first_name=firstName, character_last_name=lastName)
    newAppeareance = Appearance(
        character_name=character, 
            twitch_clip_URL=clipURL, 
            date_of_appearance=appearanceTime,
            clip_Streamer=clipStreamerName,
            publish_time=publishTime)
    #print('made it here')
    newAppeareance.save()
    return newAppeareance
#ensure the url the user submits is a whitelisted domain
def validClipURL(clip):
    #print(clip)
    if "twitch" in clip or "youtube"  in clip or "streamable"  in clip or "facebook"  in clip:
        return True
    else:
        return False
        


def configReddit():
    #bot for reddit
    reddit = praw.Reddit(

        "bot1", 
        user_agent = "<NoPixelAppearanceBot 1.0> by /u/{}".format(redditUsername),
    )
    return reddit

def main():
    reddit = configReddit()
    for mention in reddit.inbox.mentions(limit=30):
        time.sleep(15)
        print(mention.new)
        if mention.new == True:
            if (mention.subreddit == 'test' or mention.subreddit == 'RPClipsGTA'):
                print("-----------------------------------------")
                print("-----------------------------------------")
                print(f'{mention.author}\n{mention.body}')

                data = mention.body.split()
                parentPost = mention.submission
                #remove username mention
                data.pop(0)

                if data[0] == "create_appearance":
                    redditResponseToCreateAppearance(data, parentPost, mention)

                elif data[0] == "recent_appearances":
                    redditResponseToRecentAppearances(data,mention)

            else:
                print("Won't respond to unwhitelisted sub")
        else:
            print('I have seen this message already, send me something new.')
    



if __name__ == "__main__":
    main()