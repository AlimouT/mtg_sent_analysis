import os
import json
import requests
import nltk
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from pprint import pprint

nltk.download('punkt')
nltk.download('twitter_samples')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# to_keep_card_info = {
	# 'card_info': ['name', 'oracle_id'],
	# 'pricing_info': ['type_line', 'legalities', 'reserved','cmc', 'released_at'],
	# 'printing_info': ['booster', 'full_art', 'prices', 'rarity', 'promo', 'reprint', 'set', 'set_type'],
	# 'extra_info': ['oracle_text', 'mana_cost', 'edhrec_rank', 'colors', 'card_faces']
# }
	
def test():
	positive_tweets = twitter_samples.strings('positive_tweets.json')
	negative_tweets = twitter_samples.strings('negative_tweets.json')
	text = twitter_samples.strings('tweets.20150430-223406.json')
	tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

	print(tweet_tokens[0])
	
def main():
	pass

if __name__ == "__main__":
	main()

	test()