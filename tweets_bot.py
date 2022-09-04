import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db
import tweepy
import random
import time

#firebase authentication for db
def firebase_auth():
    cred = credentials.Certificate('files/serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': ''
    })

#Configuration API Twitter
def configuration():
    api_key = ""
    api_key_secret = ""
    access_token = ""
    access_token_secret = ""
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    conf = tweepy.API(auth,  wait_on_rate_limit=True)
    return conf

#Configure Tweet
def tweet(api, text):
    api.update_status(status=(text))
    print("Tweeted: " + text)
    time.sleep(60 * 16)

#Random item integer generator
def random_item():
    return random.randint(0, 3000)

#Conditional length bit
def lengthBit(x):
    if len(x) <= 180:
        return True
    else:
        return False

#Delete last char = ','
def del_end_comma(x):
    if x[-1] == ",":
        x = x[:-1]
    else:
        pass
    return x

#Tweets 
def tweets(quotes, cookies, api, n):
    x = quotes.get()[n]
    cookies.push().set(n)
    if lengthBit(x) is True:
        text = del_end_comma(x)
        tweet(api, text)
    else:
        pass

#Tweet Bot Main
def main():
    #Authentication Firebase
    firebase_auth()
    #Cookies data
    cookies = db.reference('cookies')
    #Qoutes data
    quotes = db.reference('quotes')
    #API Configuration
    api = configuration()
    #Loop for tweets bot
    while True:
        x = random_item()
        if cookies.get() is None:
            tweets(quotes, cookies, api, x)
        else:
            if x in cookies.get().values():
                pass
            else:
                tweets(quotes, cookies, api, x)

if __name__=="__main__":
    main()