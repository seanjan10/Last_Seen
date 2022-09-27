from bs4 import BeautifulSoup
import requests
#url = "https://nopixel.fandom.com/wiki/Conan_Clarkson"
#url = "https://nopixel.fandom.com/wiki/Barry_Briddle"
url = "https://nopixel.fandom.com/wiki/Graham_Warren_Hauttogs_IV"
#url = "https://nopixel.fandom.com/wiki/Abduleon_Romanov"
#url = "https://nopixel.fandom.com/wiki/Alabaster_Slim"
#url = "https://www.tutorialspoint.com/index.htm"
req = requests.get(url)
html = '''<b>tutorialspoint</b>, <i>&web scraping &data science;</i>'''
#soup = BeautifulSoup('<b class="boldest" id="boldest">Extremely bold</b>', "lxml")
#tag = soup.b
#tag.name='blockquote'
'''
tag['id'] = 'superbold'
tag['new-attribute'] = 2


print(tag)

del tag['id']
del tag['new-attribute']

print(tag)



print(tag.get('id'))
'''

#css_soup = BeautifulSoup('<p class="body strikeout" id = "my id"></p>', 'lxml')
#print(css_soup.p['id'])

#rel_soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>', 'lxml')
#print(rel_soup.a)

soup = BeautifulSoup(req.text, 'lxml')
img = soup.find_all('img')[0:3]
imgPic = img[2]
print(imgPic['src'])
#print(img[2])


#for link in soup.find_all('img'):
    #print(link.get('src'))


#print(soup.img)

#print(soup.body)


#for link in soup.find_all('a'):
    #print(link.get('href'))