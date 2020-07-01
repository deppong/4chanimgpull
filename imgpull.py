#!/usr/bin/env python
#d3pp 7-23-19

import os, sys, threading
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

def downloadImgs(startImg, endImg):
    for i in range(startImg, endImg):
        print("({}/{}): {}".format(i + 1, len(links), str(links[i][1])))
        # make sure you even need the dang folder
        if needFolder:
            urlretrieve(links[i][0], 'images/' + folderName + '/' + links[i][1])
        else:
            urlretrieve(links[i][0], 'images/' + links[i][1])


sys.tracebacklimit = 0
print("4chan.org Image scraper")
print("Made by d3pp\n")

board = input("What board? ")
threadnum = input("What is the thread number? ")
folderName = input("What do you want to name the folder?(Hit enter to skip) ")
if folderName == "":
    needFolder = False
else:
    needFolder = True



# form the url the user requested
url = "https://boards.4chan.org/%s/thread/%s" % (board, threadnum)
# make sure it looks like an actual user input it from a browser to bypass anti-bot systems
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
# initialize beautiful soup to read the html of the url
html = urlopen(req)
soup = BeautifulSoup(html)

# find all html divisions with the class fileText and grab the image url from the href, then download the image to specified dir
imgs = soup.findAll("div", {"class":"fileText"})
links = []
for img in imgs:
    link = "http:" + img.a['href'].split("imgurl=")[0]
    print(link)
    name = img.a.string
    both = [link, name]
    links.append(both[:])


createDirs()

downloadThreads = []
for i in range(0, len(links)):
    downloadThread = threading.Thread(target=downloadImgs, args=(i, i+1))
    downloadThreads.append(downloadThread)
    downloadThread.start()

for downloadThread in downloadThreads:
    downloadThread.join()
print('Done')
