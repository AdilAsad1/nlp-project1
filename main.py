import nltk
import tweepy
from tweepy import OAuthHandler
import wordcloud
import re
import matplotlib.pyplot as plt
nltk.download('punkt')

#get Input from user, keyword, consumerKey, consumerSecret, accessToken, accessSecret and bearerToken
def getInput():
    keyword = input("Enter the keyword you want to search: ")
    #consumer_key = input('Enter your Consumer Key: ')
    #consumer_secret = input('Enter your Consumer Secret: ')
    #access_token = input('Enter your Access Token: ')
    #access_secret = input('Enter your Access Secret: ')
    consumer_key = 'VfK92Z4a2wL3JMw3ueTpCk8tY'
    consumer_secret = 'uF0EY7MVmliEKPOtalIqlN1PpvTKgxoMIV9XEaQk70CTanX8Sz'
    access_token = '1354464657650708490-pTuMK61JAKi6Lja85bjXs7h3IwcM8w'
    access_secret = 'ME5w2wB6DbbJ4YObLs9n3529yPjOMTwJEuBCKevzXe0fa'
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
    tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en",tweet_mode='extended',count=100).items(10)
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





