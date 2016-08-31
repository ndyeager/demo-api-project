import tweepy

auth = tweepy.OAuthHandler('09mB3DUJsg9agik4sGw4DJ0jA', 'wM4focfIFuE8Gz3f2EX3dM3EHox4BVRNbedjNdchM24vRlRObL')

auth.set_access_token('1559211414-3ApuTjxIy7Ivr25Vn6GXHUNSEjYa8SE9H6yCbLR', 'FosDpZ9S0pSU0omTfnbpCG8rF14S85VRVJ1wb2ngdNhgc')

api = tweepy.API(auth)

public_tweets = api.user_timeline(screen_name="EleanorNorton", count=20)

for tweet in public_tweets:
    print tweet.text
