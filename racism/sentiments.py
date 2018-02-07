# as3:/usr/local/lib/python2.7/site-packages# cat sitecustomize.py
# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import tweepy
import re
from textblob import TextBlob
import matplotlib.pyplot as plt

def cleanTweetText(tweet):
	retweet_rx = re.compile(r'RT @\w+:\s') 
	url_rx     = re.compile(r'https://\w\.\w+/\w+')
	hashtag_rx = re.compile(r'#\w+\s')
	to_user_rx = re.compile(r'@\w+\s')
	regex      = [retweet_rx, url_rx, hashtag_rx, to_user_rx]
	for rx in regex:
		tweet = re.sub(rx, '', tweet)
	return tweet

def getTweetSentiment():
	file = open("South Africa.txt",'r')
	for line in file:
		print line
		cleaned_tweet = cleanTweetText(line)
		print cleaned_tweet
		tweet_sentiment = TextBlob(cleaned_tweet).sentiment
		print tweet_sentiment
		yield tweet_sentiment

def plotSentiment():
	polarity = []
	subjectivity = []
	for sentiment in getTweetSentiment():
		polarity.append(sentiment.polarity)
		subjectivity.append(sentiment.subjectivity)

	plt.scatter(polarity, subjectivity, c=polarity, s=100, cmap='RdYlGn')
	plt.xlabel('Tweet polarity')
	plt.ylabel('Tweet subjectivity')
	plt.xlim(-1.1, 1.1)
	plt.ylim(-0.1, 1.1)
	plt.show()

	positive_polarity = [p for p in polarity if p>0]
	negative_polarity = [n for n in polarity if n<0]
	neutral_polarity = [r for r in polarity if r==0]

	total_size = len(positive_polarity) + len(negative_polarity) + len(neutral_polarity)
	n_size = len(negative_polarity)/total_size
	p_size = len(positive_polarity)/total_size
	r_size = len(neutral_polarity)/total_size
	print r_size, p_size, n_size
	labels = ['Neutral tweets', 'Positive tweets', 'Negative tweets']
	sizes = [r_size, p_size, n_size]
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')
	plt.show()

plotSentiment()