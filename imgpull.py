import os
import sys
from urllib.request import urlopen, urlretrieve, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup

sys.tracebacklimit = 0

print("4chan.org Image scraper\n")

board = input("What board? ")
threadnum = input("What is the thread Number? ")

url = "https://boards.4chan.org/%s/thread/%s" % (board, threadnum)
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

html = urlopen(req)
soup = BeautifulSoup(html)

try:
    os.mkdir('images')
except FileExistsError:
    print("Directory 'images' already exists")

imgs = soup.findAll("div", {"class":"fileText"})
for img in imgs:
    link = img.a['href'].split("imgurl=")[0]
    link = "http:" + link
    name = img.a.string
    
    print(name)
    urlretrieve(link, 'images/' + name)

