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
        x =re.search(r"https\:\/\/(www\.)?([A-Za-z0-9]*)\.(.){2,3}(\/)?([A-Za-z0-9]*)(\/)?([A-Za-z0-9]*)", URL)
        if x.group(2) == 'twitch':
            groupList = x.group(5)
            print(groupList)
        else:
            groupList = x.group(7)
            print(groupList)

    if flag == 0:
        r = rpCharacter(character_first_name=splitList[0], character_nick_name=splitList[1], character_last_name=splitList[2]+" "+splitList[3]+" "+splitList[4], character_played_by=groupList, streamers_URL=splitList[5])
    else:
        r = rpCharacter(character_first_name=splitList[0], character_nick_name=splitList[1], character_last_name=splitList[2]+" "+splitList[3]+" "+splitList[4])
    r.save()