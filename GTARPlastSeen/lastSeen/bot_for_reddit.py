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
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

#global vars
redditUsername = config('redditUsername')
endString = f"\n\n*This action was automated by a bot. It has no affiliation to the Staff or Owner of NoPixel. You can contact the owner of this bot [here.](https://www.reddit.com/user/{redditUsername})*"
myURL = "http://127.0.0.1:8000/lastSeenRP/create"


def redditResponseToRecentAppearances(data, mention):
    data.pop(0)
    print("you selected to list the last 5 appearances of a character")
    if len(data) % 2 == 0:
        reply_template = ""
        #multiple names inputted
        while len(data) > 0:
            #get first character name
            fName = data[0]
            lName = data[1]
            lNameRemoveUnderscore = lName.replace("_", " ")
            #remove from the list for the upcoming characters if they exist
            del data[0], data[0]
            try:
                character = rpCharacter.objects.get(character_first_name=fName, character_last_name=lName)
                characterAppearances = Appearance.objects.filter(character_name=character)
                latestAppearances = characterAppearances.order_by('-date_of_appearance')[:5]
                strAppearance = ''
                
                if not latestAppearances:
                    mention.reply(body=f"{fName} {character.character_nick_name} {lNameRemoveUnderscore} has no appearances saved in the database. {endString}")
                    mention.mark_read()
                else:
                    for appearance in latestAppearances:
                        appearTime = appearance.date_of_appearance.strftime("%b. %d, %Y, %H:%M")
                        pubTime = appearance.publish_time.strftime("%b. %d, %Y, %H:%M")
                        strAppearance = strAppearance + f"* appeared on {appearTime} on [{appearance.clip_Streamer}]({appearance.twitch_clip_URL})'s stream. Updated at {pubTime}\n\n"
                if len(data) == 0:
                    reply_template = reply_template + f"Recent appearances for {fName} {character.character_nick_name} {lNameRemoveUnderscore}\n\n{strAppearance}{endString}"  
                    mention.reply(body=reply_template)
                    mention.mark_read() 
                else:
                    reply_template = reply_template + f"Recent appearances for {fName} {character.character_nick_name} {lNameRemoveUnderscore}\n\n{strAppearance}"  

            except ObjectDoesNotExist:
                #mention.reply(body=f"ERROR: The character you entered does not exist. If this character does exist then they have not been entered into the database. This can be done at {myURL}{endString}")
                #mention.mark_read()
                if len(data) == 0:
                    reply_template = reply_template + f"ERROR: {fName} {lNameRemoveUnderscore} does not exist. If this character does exist then they have not been entered into the database. This can be done [HERE.]({myURL}){endString}"
                    mention.reply(body=reply_template)
                    mention.mark_read() 
                else:
                    reply_template = reply_template +f"ERROR: {fName} {lNameRemoveUnderscore} does not exist. If this character does exist then they have not been entered into the database. This can be done [HERE.]({myURL})\n\n"
    else:
        mention.reply(body=f"ERROR: Incorrect Number of arguments. Please only provide the first and last name of the character. (e.g. /u/NoPixelAppearanceBot create_appearance Avon Barksdale).\nNote: if the character has more than two names, then include the additional names in the last name and indicate the additional names with underscores in place of spaces. (e.g. /u/NoPixelAppearanceBot create_appearance Arush Patel_Santana{endString}")
        mention.mark_read()
        


#TODO: add validation for channel name for twitch requirements
def redditResponseToCreateAppearance(data, parentPost, mention):
    #remove from list since no longer necessary
    data.pop(0)
    print('you selected to create an appearance')

    
    clipStreamerName = data[0]

    #create if statement for channel name validity

    data.pop(0)
    #print(len(data))
    #print(data)
    if len(data) % 2 == 0:
        #now = pytz.UTC.localize(datetime.now())
        now = timezone.now()
        clipURL = parentPost.url

        #check if whitelisted url
        if validClipURL(clipURL) == False:
            mention.reply(body=f'ERROR: supported clip URLS include twitch, youtube, facebook and streamable.{endString}')
            mention.mark_read()
            return

        #should not need to check appearance as reddit posts cannot be posted in the future

        #convert POSIX time to utc time
        appearanceTime = datetime.utcfromtimestamp(parentPost.created_utc)
        user_who_submitted = mention.author
        reply_template = ""
        while len(data) > 0:

            characterFName = data[0]
            characterLName = data[1]
            lNameRemoveUnderscore = characterLName.replace("_", " ")
            #clipStreamerName = data[2]
            #print(f'Created a new appearance for: First name = {characterFName}, Last Name = {characterLName}, Streamer = {clipStreamerName}')
            #remove the first 3 values to read the next 3
            del data[0], data[0]
            try:
                character = rpCharacter.objects.get(character_first_name=characterFName, character_last_name=characterLName)
                appearance = createAppearance(character, clipURL, appearanceTime, clipStreamerName, now)
                
                if len(data) == 0:
                    reply_template = reply_template +f"New appearance created for {characterFName} {character.character_nick_name} {lNameRemoveUnderscore}! View other appearances by this character [HERE.](http://127.0.0.1:8000/lastSeenRP/character/{characterFName}_{characterLName}/){endString}"
                    mention.reply(body=reply_template)
                    mention.mark_read()
                else:
                    reply_template = reply_template +f"New appearance created for {characterFName} {character.character_nick_name} {lNameRemoveUnderscore}! View other appearances by this character [HERE.](http://127.0.0.1:8000/lastSeenRP/character/{characterFName}_{characterLName}/)\n\n"

            except ObjectDoesNotExist:
                #print("ERROR: The character you entered does not exist. If this character does exist then they have not been entered into the database. This can be done at www.url.com")
                #mention.reply(body=f"ERROR: The character you entered does not exist. If this character does exist then they have not been entered into the database. This can be done at {myURL}{endString}")
                #mention.mark_read()

                if len(data) == 0:
                    reply_template = reply_template +f"ERROR: {characterFName} {lNameRemoveUnderscore} does not exist. If this character does exist then they have not been entered into the database. This can be done [HERE.]({myURL}){endString}"
                    mention.reply(body=reply_template)
                    mention.mark_read()
                else:
                    reply_template = reply_template +f"ERROR: {characterFName} {lNameRemoveUnderscore} does not exist. If this character does exist then they have not been entered into the database. This can be done [HERE.]({myURL})\n\n"
                

    else:
        #print("ERROR: Incorrect Number of arguments. Please only provide the first and last name of the character, and the name of the channel where you clipped from. (e.g. /u/NoPixelAppearanceBot create_appearance Avon Barksdale LIRIK).\nNote: if the character has more than two names, then include the additional names in the last name and indicate the additional names with underscores in place of spaces. (e.g. /u/NoPixelAppearanceBot create_appearance Arush Patel_Santana SayeedBlack")
        mention.reply(body=f"ERROR: Incorrect Number of arguments. Please only provide the name of the channel where you clipped from and the first and last name of the character(s). (e.g. /u/NoPixelAppearanceBot create_appearance LIRIK Avon Barksdale).\n\nNote: if the character has more than two names, then include the additional names in the last name and indicate the additional names with underscores in place of spaces. (e.g. /u/NoPixelAppearanceBot create_appearance SayeedBlack Arush Patel_Santana).\n\nFor multiple characters, add them after the first character and so on. (e.g. /u/NoPixelAppearanceBot LIRIK Avon Barksdale Lang Buddha).{endString}")
        mention.mark_read()
    

#function to create a valid appearance
def createAppearance(character, clipURL, appearanceTime, clipStreamerName, publishTime):
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
        time.sleep(3)
        print(mention.new)
        if mention.new == True:
            if (mention.subreddit == 'test' or mention.subreddit == 'RPClipsGTA'):
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
        print("-----------------------------------------")
        print("-----------------------------------------")
    



if __name__ == "__main__":
    main()