import csv
import json

class Episode:
    
    def __init__(self,title,season,episode,reason,watched=False):
        self.season  = int(season)
        self.episode = int(episode)
        self.title   = title
        self.reason  = reason 
        self.watched = watched

    def __eq__(self,other):
        return self.season == other.season and self.episode == other.episode

    def __lt__(self,other):
        if(self.season == other.season):
            return self.episode < other.episode

        return self.season < other.season

    def __gt__(self,other):
        if(self == other):
            return false

        return not self < other

    def __str__(self):
        return "S{}E{},\nTitle:{},\nReason:{}\n".format(self.season,self.episode,
                self.title, self.reason) 

    def toJson(self):
        return {'title':self.title,'season':self.season,'episode':self.episode,
                'reason':self.reason, 'watched':self.watched}

def loadfromcsv():
    csvfile  = open('AdventureTime.csv') 
    episodes = list() 
    
    fieldnames = ("Season","Episode","Title","Reason")
    reader     = csv.DictReader(csvfile,fieldnames)
    for r in reader:
        if(r['Season'] == 'Season'):
            continue
        episodes.append(Episode(r['Title'],r['Season'],r['Episode'],r['Reason']))

    return episodes

def loadfromjson():
    data = json.load(open('AdventureTime.json')) 
    epis = list()
    for r in data['list']:
        epis.append(Episode(r['title'],r['season'],r['episode'],r['reason'],r['watched']))

    return epis

def dumptojson(li):
    di = {'list':[]}
    for i in li:
        di['list'].append(i.toJson())
    with open('AdventureTime.json','w') as f:
        json.dump(di,f)

def getNext(li):
    for i in li:
        if(not i.watched):
            print(str(i))
            i.watched = True
            return

def setWatched(li,s,e):
    for i in li:
        if(i.season < s or (i.season == s and i.episode < e)):
            i.watched = True
        
li = loadfromjson()
getNext(li)
dumptojson(li)
