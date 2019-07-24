import os
from urllib.request import urlopen, urlretrieve, Request
from bs4 import BeautifulSoup

print("4chan.org Image scraper\n")

board = input("What board? ")
threadnum = input("What is the thread Number? ")

url = "https://boards.4chan.org/%s/thread/%s" % (board, threadnum)
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
print(req)

html = urlopen(req)
soup = BeautifulSoup(html)

imgs = soup.findAll("div", {"class":"fileText"})
for img in imgs:
    link = img.a['href'].split("imgurl=")[0]
    link = "http:" + link
    name = img.a.string
    
    print(name)
    urlretrieve(link, 'images/' + name)

