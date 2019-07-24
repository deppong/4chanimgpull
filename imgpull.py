import os
import sys
from urllib.request import urlopen, urlretrieve, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup

sys.tracebacklimit = 0

def folderPrompt():
    check = str(input("Would you like to put the images in a seperate folder? (Y/N): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()

print("4chan.org Image scraper\n")

board = input("What board? ")
threadnum = input("What is the thread number? ")
needFolder = folderPrompt()
if needFolder:
    folderName = input("What do you want to name the folder? ")

url = "https://boards.4chan.org/%s/thread/%s" % (board, threadnum)
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

html = urlopen(req)
soup = BeautifulSoup(html)

try:
    os.mkdir('images')
except FileExistsError:
    print("Directory 'images' already exists")

if needFolder:
    try:
        os.mkdir('images/' + folderName)
    except FileExistsError:
        print("Directory '"  + folderName +  "' already exists")


imgs = soup.findAll("div", {"class":"fileText"})
for img in imgs:
    link = img.a['href'].split("imgurl=")[0]
    link = "http:" + link
    name = img.a.string
    
    print(name)
    urlretrieve(link, 'images/' + folderName + '/' + name)

