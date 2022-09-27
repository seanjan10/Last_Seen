import os
import re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lastSeen.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from lastSeenRP.models import rpCharacter






filename = "characterSplit.txt"

f = open(filename, 'r', encoding='UTF-8')



for i in range(0, 4149):
    flag = 0
    line = f.readline()
    splitList=line.split(',')
    print(splitList)
    URL=splitList[5]

    if URL == 'Does-Not-Stream\n':
        flag = 1
        print('streamers name is unknown')
    else:
        x =re.search(r"https\:\/\/(www\.)?([A-Za-z0-9]*)\.(.){2,3}(\/)?([A-Za-z0-9\_]*)(\/)?([A-Za-z0-9\_]*)", URL)
        if x.group(2) == 'twitch':
            groupList = x.group(5)
            print(groupList)
        else:
            groupList = x.group(7)
            print(groupList)

    fullLastName = ""
    if splitList[4] == "":
        if splitList[3] == "":
            fullLastName = splitList[2]
        else:
            fullLastName = splitList[2] + "_" + splitList[3]
    else:
        fullLastName = splitList[2] + "_" + splitList[3] + "_" + splitList[4]


    if flag == 0:
        r = rpCharacter(character_first_name=splitList[0], character_nick_name=splitList[1], character_last_name=fullLastName, character_played_by=groupList, streamers_URL=splitList[5])
    else:
        r = rpCharacter(character_first_name=splitList[0], character_nick_name=splitList[1], character_last_name=fullLastName)
    r.save()
    