import requests
import urllib.request
import os
from bs4 import BeautifulSoup as BS

string  = "http://manganelo.com/chapter/read_hikaru_no_go/chapter_"
mname   = "hikarunogo"#input("Manga name>")
direc   = "./" + mname + "/"

def checkCreate(name):
    print(name)
    if not os.path.exists(name):
        print("CREATING")
        os.makedirs(name)

checkCreate(direc)

for i in range(1,192):
    chapterdir = direc + "Chapter_" + str(i)
    checkCreate(chapterdir)
    os.chdir(chapterdir)
    r = requests.get(string + str(i))
    data = r.text
    soup = BS(data,"html5lib")
    div  = soup.findAll("div",{"class":"vung-doc"})
    for img in div:
        image = img.find_all("img")
        for k in range(len(image)):
            urllib.request.urlretrieve("http:" + image[k].get('src'),\
                str(k) + ".jpg")
    os.chdir("../../")
