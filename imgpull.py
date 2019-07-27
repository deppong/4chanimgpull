#d3pp 7-23-19

import os
import sys
from urllib.request import urlopen, urlretrieve, Request
from bs4 import BeautifulSoup


def createDirs():
    try:
        os.mkdir('images')
    except FileExistsError:
        print("Directory 'images' already exists")

    if needFolder:
        try:
            os.mkdir('images/' + folderName)
        except FileExistsError:
            print("Directory '"  + folderName +  "' already exists")


def folderPrompt():
    check = str(input("Would you like to put the images in a seperate folder? (Y/N): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return folderPrompt()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return folderPrompt()

sys.tracebacklimit = 0
print("4chan.org Image scraper")
print("Made by d3pp\n")

board = input("What board? ")
threadnum = input("What is the thread number? ")
needFolder = folderPrompt()
if needFolder:
    folderName = input("What do you want to name the folder? ")


# form the url the user requested
url = "https://boards.4chan.org/%s/thread/%s" % (board, threadnum)
# make sure it looks like an actual user input it from a browser to bypass anti-bot systems
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
# initialize beautiful soup to read the html of the url
html = urlopen(req)
soup = BeautifulSoup(html)

createDirs()

# find all html divisions with the class fileText and grab the image url from the href, then download the image to specified dir
imgs = soup.findAll("div", {"class":"fileText"})
# enumerate the list to have a jank progress indicator
for c, img in enumerate(imgs):
    link = img.a['href'].split("imgurl=")[0]
    link = "http:" + link
    name = img.a.string
    # print the (number of image / total images): imagename.png
    print("({}/{}): {}".format(c + 1, len(imgs), str(name)))
    # make sure you even need the dang folder
    if needFolder:
        urlretrieve(link, 'images/' + folderName + '/' + name)
    else:
        urlretrieve(link, 'images/' + name)
