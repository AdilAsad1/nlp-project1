import nltk
import tweepy
from tweepy import OAuthHandler
import wordcloud
import re
import matplotlib.pyplot as plt

#get Input from user, keyword, consumerKey, consumerSecret, accessToken and accessSecret
def getInput():
    keyword = input("Enter the keyword you want to search: ")
    consumer_key = input('Enter your Consumer Key: ')
    consumer_secret = input('Enter your Consumer Secret: ')
    access_token = input('Enter your Access Token: ')
    access_secret = input('Enter your Access Secret: ')
    
    return keyword, consumer_key, consumer_secret, access_token, access_secret

def stopWordLst():
    wordList = [] 
    with open("stopwords.txt", "r") as f:
        for line in f:
            wordList.extend(line.split())

    return wordList

def loadApi(consumer_key, consumer_secret, access_token, access_secret):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)

def getTweets(api,keyword):
    tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en",tweet_mode='extended').items(1000)
    list_tweets = [tweet for tweet in tweets]
    tweet_data = []
    for tweet in list_tweets:
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        tweet_data.append(text)
    return tweet_data

def cleanTweetData(tweet_data):
    cleanedData = []
    for tweet in tweet_data:
        tweet = re.sub(r'http\S+','',str(tweet))
        tweet1 = re.sub(r'[^\w\s]','',tweet)
        tweet2 = re.sub(r"\d+", "", tweet1)
        tweet3 = re.sub(r"(?<!\\)\\n|\n",'', tweet2)
        tweet4 = re.sub(r'@([A-Za-z0-9_]+)','',tweet3)
        tweet5 = re.sub(r'#([A-Za-z0-9_]+)','',tweet4)
        cleanedData.append(tweet5)
    return cleanedData

def wordTokenization(tweetData):
    result = ' '.join(tweetData)
    words = nltk.word_tokenize(result)
    words = ' '.join(words)
    return words

def generateWordCloud(words, stopwords):
    wc = wordcloud.WordCloud(background_color='white',stopwords=stopwords).generate(words)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def main():
    keyword, consumer_key, consumer_secret, access_token, access_secret = getInput()
    api = loadApi(consumer_key, consumer_secret, access_token, access_secret)
    tweet_data = getTweets(api, keyword)
    tweetData = cleanTweetData(tweet_data)
    words = wordTokenization(tweetData)
    stopwords = stopWordLst()
    generateWordCloud(words, stopwords)

main()





