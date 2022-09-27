import os
import re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lastSeen.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from lastSeenRP.models import rpCharacter






filename = "characterSplit_add_images.txt"

f = open(filename, 'r', encoding='UTF-8')


#insert a record from a CSV (txt) file to be inserted into the DB after every time the DB is flushed
#4145 is the current amount of the records in the txt file
for i in range(0, 4145):
    #flag if there is no streamer name provided
    flag = 0
    line = f.readline()
    #split csv values into a list
    splitList=line.split(',')
    print(splitList)
    #their twitch/facebook/youtube handle
    URL=splitList[5]
    #remove the leading whitespace at the beginning of their img src's
    removeSpace = splitList[6]
    splitList[6] = removeSpace.strip(" ")

    #csv format is first name, nick name, last name 1, last name 2, last name 3, streamer URL, img src
    if URL == 'Does-Not-Stream':
        flag = 1
        print('streamers name is unknown')
    else:
        #regex to match group for the domain of their url and their username
        x =re.search(r"https\:\/\/(www\.)?([A-Za-z0-9]*)\.(.){2,3}(\/)?([A-Za-z0-9\_]*)(\/)?([A-Za-z0-9\_]*)", URL)
        #check which website they use
        if x.group(2) == 'twitch':
            groupList = x.group(5)
            print(groupList)
        else:
            groupList = x.group(7)
            print(groupList)
    #create their full last name if they use the optional 2nd and 3rd last name
    fullLastName = ""
    if splitList[4] == "":
        if splitList[3] == "":
            fullLastName = splitList[2]
        else:
            fullLastName = splitList[2] + "_" + splitList[3]
    else:
        fullLastName = splitList[2] + "_" + splitList[3] + "_" + splitList[4]

    #create each object of a character, 
    #if they provided a username
    if flag == 0:
        r = rpCharacter(character_first_name=splitList[0], character_nick_name=splitList[1], character_last_name=fullLastName, character_played_by=groupList, streamers_URL=splitList[5], character_image=splitList[6])
    #if they didn't provide username
    else:
        r = rpCharacter(character_first_name=splitList[0], character_nick_name=splitList[1], character_last_name=fullLastName, character_image=splitList[6])
    #save each object into the DB
    r.save()
    