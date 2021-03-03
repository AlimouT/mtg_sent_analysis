import praw
import os
import requests
import settings

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
CLIENT_ID = os.environ.get('CLIENT_ID')
SECRET_TOKEN = os.environ.get('SECRET_TOKEN')

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'testApp1'}


# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
# here we pass our login method (password), username, and password

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET_TOKEN,
	user_agent='my_user_agent')



# get 10 hot posts from the MachineLearning subreddit
# reddit.subreddit('all').hot(limit=10)
hot_posts = reddit.subreddit('magicTCG/').hot(limit=10)
for post in hot_posts:
    print(post.title)