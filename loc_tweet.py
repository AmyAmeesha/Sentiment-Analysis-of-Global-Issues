# import sys
# import tweepy

# access_key = "910096003847438336-Xng5wxcVdT3ECD1EJXARRkjx5fOwz6U"
# access_secret = "GuqdUhmsiq39bF5OKZlUh5haQ64KamXF0Qhx10aC8RLcI"
# consumer_key = "DGA6Hxjrezz1OgIFbFf94Roqr"
# consumer_secret = "4hYZwFGEYNG2KVSYGj3PtRgPVlzcyzPiwaPCA4qKmQunnzdyxu"


# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_key, access_secret)
# api = tweepy.API(auth)


# class CustomStreamListener(tweepy.StreamListener):
#     def on_status(self, status):
#         print status.text

#     def on_error(self, status_code):
#         print >> sys.stderr, 'Encountered error with status code:', status_code
#         return True # Don't kill the stream

#     def on_timeout(self):
#         print >> sys.stderr, 'Timeout...'
#         return True # Don't kill the stream

# sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
# sapi.filter(track=['manchester united'])

import tweepy
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
import io
import csv


pd.options.display.max_columns = 50
pd.options.display.max_rows= 50
pd.options.display.width= 120

consumer_key = "DGA6Hxjrezz1OgIFbFf94Roqr"
consumer_secret = "4hYZwFGEYNG2KVSYGj3PtRgPVlzcyzPiwaPCA4qKmQunnzdyxu"

auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)
results = api.search(q="Terrorism")

print len(results)
file = io.open("eurocup_tweets.txt", "a", encoding='utf8')
# csvfile = io.open('terrorism_tweets.csv', 'w', encoding='utf8')
# csvwriter = csv.writer(csvfile, delimiter=' ')
num=1
def print_tweet(tweet):
	file.write("\n@%s - %s (%s, %s)\n" % (tweet.user.screen_name, tweet.user.name, tweet.created_at,tweet.user.location))
	# csvwriter.writerow("\n@%s - %s (%s, %s)\n" % (tweet.user.screen_name, tweet.user.name, tweet.created_at,tweet.user.location))
    # data = tweet.text.encode("utf-8")
    # file.write(data)
	file.write(tweet.text)

tweet=results[1]
# print tweet
# print_tweet(tweet)

tweet=results[2]

# for param in dir(tweet):
#     if not param.startswith("_"):
#         print "%s : %s\n" % (param, eval("tweet." + param))
results = []
for tweet in tweepy.Cursor(api.search, q="eurocup", geo="").items(8000):
    results.append(tweet)


for item in results:
	file.write(unicode("Tweet number:")) 
	file.write(unicode(num))
	num=num+1
	print_tweet(item)    

file.close()
def process_results(results):
    id_list = [tweet.id for tweet in results]
    data_set = pd.DataFrame(id_list, columns=["id"])

#     # Processing Tweet Data

    data_set["text"] = [tweet.text for tweet in results]
    data_set["created_at"] = [tweet.created_at for tweet in results]
#     data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
#     data_set["favorite_count"] = [tweet.favorite_count for tweet in results]
#     data_set["source"] = [tweet.source for tweet in results]
#     # data_set["coordinates"] = [tweet.coordinates.geoJSON  for tweet in results]
    data_set["place"] = [tweet.user.location for tweet in results]
#     # Processing User Data
#     # data_set["user_id"] = [tweet.author.id for tweet in results]
#     # data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
#     # data_set["user_name"] = [tweet.author.name for tweet in results]
#     # data_set["user_created_at"] = [tweet.author.created_at for tweet in results]
#     # data_set["user_description"] = [tweet.author.description for tweet in results]
#     # data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
#     # data_set["user_friends_count"] = [tweet.author.friends_count for tweet in results]
#     data_set["user_location"] = [tweet.author.location for tweet in results]
#     data_set["timezone"] = [tweet.author.time_zone for tweet in results]
    return data_set
data_set = process_results(results)

# for item in dataset:
# 	print item
sources = data_set["place"].value_counts()
sources.to_csv('loc_count_eurocup.csv', encoding='utf-8')

# file = open("terrorism_country_count.txt", "w")
# for item in sources:
# 	file.write(item)
# file.close()
# plt.barh(xrange(len(sources)), sources.values)
# plt.yticks(np.arange(len(sources)), sources.index)
# plt.show()
