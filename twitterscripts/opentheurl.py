import webbrowser
import urllib.request as req
import re
from CONFIG import *
from twitter import Api
from time import sleep
from sys import argv

class TokenInfo:
    '''
    This  class stores the data in order to connect to twitter
    '''
    
    def __init__(self, consumer_key, consumer_secret, 
                 access_token_key, access_token_secret):
        '''
            @param 
                All consumers are strings
        '''

        self.consumer_key        = consumer_key;
        self.consumer_secret     = consumer_secret;
        self.access_token_key    = access_token_key;
        self.access_token_secret = access_token_secret;
        self.api                 = None

    def __str__(self):
        return ("Consumer key: " + str(self.consumer_key) + "\n" + \
                "Consumer secret: " + str(self.consumer_secret) + "\n" + \
                "Access Token Key: " + str(self.access_token_key) + "\n" + \
                "Access Token Secret : " + str(self.access_token_secret) + "\n")

    def connect_api(self):
        '''
        Connects the api with the given cesidentials
        ''' 
        self.api = Api(consumer_key=self.consumer_key,
                    consumer_secret=self.consumer_secret,
                    access_token_key=self.access_token_key,
                    access_token_secret=self.access_token_secret)

        #Our try/catch given to us by twitter api
        self.api.VerifyCredentials()

class OpenUrl:
    '''
    This class takes a token and the username
    and tries to connect to the given username
    through the given token and opens it in a
    browser
    '''
    
    def __init__(self,token,username,interval=10): 
        '''
        @params
            token    : TokenInfo()
            username : String
            interval : int - optional
        '''
        self.token    = token
        self.username = username
        self.interval = interval

    def __str__(self):
        return ("Token: " + str(self.token) + '\n' + "Given username: " + \
                str(self.username) + '\n')

    def start(self):
        '''
        This continues to loop until the first timeline status is a link
        then it opens the url in a browser
        '''
        while(True):
            status = token.api.GetUserTimeline(screen_name=self.username)[0].text
            try:
                #Extracts link from the string (takes first link)
                status = re.findall(r'(https?://\S+)', status)[0]
                request = req.Request(status)
                req.urlopen(request)
                webbrowser.open(status,new=2)
                return
            except:
                sleep(self.interval)
                continue 

if __name__ == "__main__":
    
    token = TokenInfo(COMSUMER_KEY, CONSUMER_SECRET, 
                              ACCESS_TKN_KEY, ACCESS_TKN_SCRT)
    token.connect_api()
    username = input("Username > ")
    interval = int(input("Interval > "))
    given = OpenUrl(token,username,interval)
    given.start()
