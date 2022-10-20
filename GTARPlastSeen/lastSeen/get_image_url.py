from bs4 import BeautifulSoup
import requests
import re 

#mainly similar to insert data except was used to retrieve image that are hosted on an external website

file_reader = open('characterSplit.txt', 'r', encoding='UTF-8')
file_writer = open('characterSplit_add_images.txt', 'w', encoding='UTF-8')
invalidIndex = []
for i in range(0,4149):

    #url = "https://nopixel.fandom.com/wiki/Arush_Patel_Santana"
    #same as insert data
    line = file_reader.readline()
    splitList=line.split(',')
    print(splitList)
    strStripped = splitList[5].strip('\n')
    splitList[5] = strStripped
    fullLastName=""
    if splitList[4] == "":
        if splitList[3] == "":
            fullLastName = splitList[2]
        else:
            fullLastName = splitList[2] + "_" + splitList[3]
    else:
        fullLastName = splitList[2] + "_" + splitList[3] + "_" + splitList[4]

    #different urls based on if they provided a last name or not
    try:
        if splitList[2] == "No-Last-Name":
            url = "https://nopixel.fandom.com/wiki/{}".format(splitList[0])
        else:
            url = "https://nopixel.fandom.com/wiki/{}_{}".format(splitList[0], fullLastName)
        
        #print(url)
        #create http request into the website of the character
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        #link for the img of the character is always the 3rd img link
        img = soup.find_all('img')[0:3]
        imgPic = img[2]
        #retrieve https address of the image
        imgURL = imgPic['src']
        #regex to make sure correct image link is followed, create group around entire link so it can be easily accessed
        revistedURL = re.search("(https\:\/\/static\.wikia\.nocookie\.net\/nopixel\/images\/([a-z0-9])\/([a-z0-9][a-z0-9])\/(([A-Za-z0-9]|\_|\.|\-|\%)*))\/", imgURL)
        print(revistedURL.group(1))
        #write to file so that it can be inserted into db whenever it is flushed, may be adjusted if i make a migrations file
       # file_writer.write("{},{},{},{},{},{}, {}\n".format(splitList[0], splitList[1], splitList[2], splitList[3], splitList[4], splitList[5], revistedURL.group(1)))
    #error if the index is out of bounds in case the specific character wiki page didn't follow exactly as the generateed URL above
    except IndexError:
        print("Error, could not get the image, most likely due to the name not matching the URL")
        invalidIndex.append(i+1)
        #write to file that no photo could be found
        #file_writer.write("{},{},{},{},{},{}, URL_NOT_FOUND\n".format(splitList[0], splitList[1], splitList[2], splitList[3], splitList[4], splitList[5]))
    #error if the wiki page has not photos at all
    except AttributeError:
        print("Error, could not get the image, most likely due to the name not matching the URL")
        invalidIndex.append(i+1)
        #file_writer.write("{},{},{},{},{},{}, URL_NOT_FOUND\n".format(splitList[0], splitList[1], splitList[2], splitList[3], splitList[4], splitList[5]))

file_reader.close()
file_writer.close()
print("indexes that did not work")
print(invalidIndex)