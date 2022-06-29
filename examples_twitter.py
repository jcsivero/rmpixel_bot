import tweepy


bearer_token = "AAAAAAAAAAAAAAAAAAAAAD4RbQEAAAAA9AvdOU0REjsfcJaovDCK%2FtGNAjE%3D3WPL7QCPkYAQQMrBN5xlDxkdmqoMXmRybLo7eGVoG1VVEJyRpc"



client = tweepy.Client(bearer_token)

# You can specify additional Tweet fields to retrieve using tweet_fields
response = client.search_recent_tweets(
    "Tweepy"
)
tweets = response.data
print (tweets)
# You can then access those fields as attributes of the Tweet objects
for tweet in tweets:
    print(tweet.id, tweet.lang)

# Alternatively, you can also access fields as keys, like a dictionary
for tweet in tweets:
    print(tweet["id"], tweet["lang"])

# There’s also a data attribute/key that provides the entire data dictionary
for tweet in tweets:
    print(tweet.data)
    print(tweet)
