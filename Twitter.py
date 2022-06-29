#!pip install tweepy
#!pip install textblob
#crear cuenta como desarrollador en apps.twitter.com
#Se importa la librería tweepy
import sys
import tweepy

#Se define las variables para el acceso al API de twitter
consumer_key = "Zd3zSeZDxZJi1ls7xOCIIK8tV"
consumer_secret = "iAx845bkLKZS6CTKZLEOPBx3xrDif77kz2DsbRdAcRpP8FNOAN"
access_token = "1512358686227943430-k7GUBBaWl1rYz5qEScASS9Ahg9Bc5M"
access_token_secret = "Hss3iR2UE5NBv4Zb1IwC9e1VtT9yPB3IS6CGwgFfyY7bL" 
bearer_token = "AAAAAAAAAAAAAAAAAAAAAD4RbQEAAAAA9AvdOU0REjsfcJaovDCK%2FtGNAjE%3D3WPL7QCPkYAQQMrBN5xlDxkdmqoMXmRybLo7eGVoG1VVEJyRpc"

#Se autentica en twitter

#auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret,access_token,access_token_secret)
#auth2 = tweepy
#client = tweepy.Client())
#api = tweepy.API(auth)

#time_line = api.home_timeline()

#for tweet in time_line:
#   print(f'{tweet.user.screen_name}:\n{tweet.text}\n{"*"*60}')

#se verifica que el usuario conectado en twitter es de uno
#print(api.me().name)

client = tweepy.Client(bearer_token=bearer_token)


tweets2 = {
    "data": [
        {
            "referenced_tweets": [
                {
                    "type": "replied_to",
                    "id": "1532688756939141122"
                }
            ],
            "id": "1532688835137753089",
            "text": "@alu0100585704 esta es mi segunda respuesta desde jcsiverio",
            "conversation_id": "1532687900604776452"
        },
        {
            "referenced_tweets": [
                {
                    "type": "replied_to",
                    "id": "1532687900604776452"
                }
            ],
            "id": "1532688309578866690",
            "text": "@alu0100585704 de que vas desde jcsiverio",
            "conversation_id": "1532687900604776452"
        }
    ],
    "includes": {
        "tweets": [
            {
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1532688309578866690"
                    }
                ],
                "id": "1532688756939141122",
                "text": "@Jcsiverio de lo que me da la gana",
                "conversation_id": "1532687900604776452"
            },
            {
                "id": "1532687900604776452",
                "text": "@Jcsiverio Hola desde alu0100",
                "conversation_id": "1532687900604776452"
            }
        ]
    },
    "meta": {
        "newest_id": "1532688835137753089",
        "oldest_id": "1532688309578866690",
        "result_count": 2
    }
}
# Replace with your own search query
#conversation_id:1532687900604776452
query = 'from:Jcsiverio -is:retweet is:reply'
#suhemparack
# tweet_fields=['context_annotations', 'created_at'],
#,"attachments","author_id","lang","in_reply_to_user_id","referenced_tweets"
tweets = client.search_recent_tweets(query=query, tweet_fields=['conversation_id', 'created_at',"attachments","author_id","lang","in_reply_to_user_id","referenced_tweets"], max_results=10,expansions="referenced_tweets.id")


#preparo lista con identificadores  conversaciones
hilos = []
for id in reversed(tweets.data):
    print (id.conversation_id,"\n")
    if not id.conversation_id in hilos:
        hilos.append(id.conversation_id)

print (hilos)

for conversation in reversed(hilos):
    query = 'conversation_id:' + str(conversation)
    tweets_hilo = client.search_recent_tweets(query=query, tweet_fields=['conversation_id', 'created_at',"attachments","author_id","lang","in_reply_to_user_id","referenced_tweets"], max_results=10,expansions="referenced_tweets.id")
    print (len(tweets_hilo.includes["tweets"]))
    for i in range(len(tweets_hilo.includes["tweets"]),0,-1):
    #reversed(tweets_hilo.includes["tweets"]):                
        print (tweets_hilo.includes["tweets"][i-1])
        print (tweets_hilo.data[i-1])
        

#for tweet in reversed(tweets2["includes"]["tweets"]):
    #if tweet.in_reply_to_user_id != None:
        
        #print (tweet["text"])
        #print (len(tweets2.includes["tweets"]))

        #print(tweet.id, tweet.text, tweet.in_reply_to_user_id, tweet.conversation_id,tweet.created_at,tweet.author_id, "\n")
        #print (tweet.text)
        #query = 'conversation_id:' + str(tweet.conversation_id)                
        #hilo = client.search_recent_tweets(query=query, tweet_fields=['conversation_id', 'created_at',"attachments","author_id","lang","in_reply_to_user_id","referenced_tweets"], max_results=10,expansions="referenced_tweets.id")        
        #print (hilo.data)

    #if len(tweet.context_annotations) > 0:
        #print(tweet.context_annotations)


