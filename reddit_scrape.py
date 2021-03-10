import datetime
import os
import re
import time
import settings
import praw
# import requests
# from bs4 import BeautifulSoup
# import nltk

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
CLIENT_ID = os.environ.get('CLIENT_ID')
SECRET_TOKEN = os.environ.get('SECRET_TOKEN')

headers = {'User-Agent': 'testApp1'}

extract_cards_regex = r"\[\[.*?\]\]"

class My_Submissions():
	verbose = True
	verbose = False

	def __init__(self, praw_submission, max_comments=300, max_depth=20):
		self.praw_submission_object = praw_submission
		
		self.id = praw_submission.id
		self.url = praw_submission.url
		self.upvote_ratio = praw_submission.upvote_ratio
		self.score = praw_submission.score

		self.cards_mentioned = {}
		self.max_comments = max_comments 
		self.max_depth = max_depth


	def eval_submission(self):		
		if My_Submissions.verbose: print(self.praw_submission_object.url)
		
		# Evaluate submission itself
		if self.praw_submission_object.is_self:
			self.eval_textpost()

		# Evaluate replies
		for comment in self.praw_submission_object.comments:
			self.eval_content(comment)

		for card, frequency in self.cards_mentioned.items():
			print(card, frequency)

	def eval_textpost(self):
		opening_post = self.praw_submission_object
		post_time = datetime.datetime.fromtimestamp(opening_post.created_utc)
		if My_Submissions.verbose: print(f'{post_time}\t({opening_post.id} (OP))\t{opening_post.author}:\n[{opening_post.score}: {opening_post.upvote_ratio}]\t{opening_post.selftext}\n~~~')
		cards = [card[2:-2] for card in re.findall(extract_cards_regex, opening_post.selftext)]
		# opening_post.score*opening_post.upvote_ratio to lower the effect of posts being seen by so many people and receiving more upvotes than they should
		# card_score = opening_post.score*(opening_post.upvote_ratio-.5)
		card_score = opening_post.score*opening_post.upvote_ratio if opening_post.score > 0 else -1
		for card in cards:
			self.cards_mentioned[card.lower()] = self.cards_mentioned.get(card.lower(), 0)+card_score


	def eval_content(self, content, level=1):
		if level > self.max_depth:
			print(f'Max depth ({self.max_depth}) on {content.id}.')
			return
		
		# Evaluate the content
		if content.author == 'MTGCardFetcher':
			# This is mostly used for tagging, and I don't really care about responses to it in most cases
			cards = content.body.splitlines()[:-1]
			cards = [line.split(']')[0][1:] for line in cards if line.strip() != '']
			card_list = "\n\t".join(cards)
			if My_Submissions.verbose: print(f'{" "*level}MTGCardFetcher post:\n\t{card_list}\n~~~')
			for card in cards:
				self.cards_mentioned[card.lower()] = self.cards_mentioned.get(card.lower(), 0)
		else:
			# Regular content
			post_time = datetime.datetime.fromtimestamp(content.created_utc)
			if My_Submissions.verbose: print(f'{" "*level}{post_time}\t({content.id})\t{content.author}:\n{" "*level}[{content.score}]\t{content.body}\n~~~')
			cards = [card[2:-2] for card in re.findall(extract_cards_regex, content.body)]
			card_score = content.score if content.score>0 else -1
			for card in cards:
				self.cards_mentioned[card.lower()] = self.cards_mentioned.get(card.lower(), 0) + card_score
			replies = content.replies
		
			# Load replies to the comment
			while len(replies) < self.max_comments:
				try:
					replies.replace_more()
					break
				except PossibleExceptions:
					if My_Submissions.verbose: print(f'Loading more replies to {content.id} (level {level})...')
					time.sleep(.2)
			
			# Recursively evalutate the replies
			for comment in replies:
				if comment is praw.models.MoreComments:
					continue
				self.eval_content(comment, level+1)


def main():
	reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET_TOKEN, user_agent='my_user_agent')

	subreddit_id = 'magicTCG'
	submission_id = 'm0a6w1'
	submission_id = 'lh9nz0'
	submission_id = 'lxrgyw'
	# comment_id = 'gpokujv'

	# mtg_submission = reddit.submission(submission_id)
	# post = My_Submissions(mtg_submission)
	# post.eval_submission()

	mtg_subreddit = reddit.subreddit(subreddit_id)
	for submission in mtg_subreddit.hot(limit=20):
		post = My_Submissions(submission)
		post.eval_submission()
		time.sleep(.2)

	# mtg_comment = reddit.comment(comment_id)

	### Reddit tree:
	# Subreddit
	#  Submissions
	#   Comment Tree
	# 	Comments
	#    Comment Tree
	#    Comments

	#	Comments
	#		Comment.body

	# print('\n\t~~ SUBMISSIONS ~~\n')
	# for submission in mtg_subreddit.hot(limit=5):
		# print(submission.title)


if __name__ == '__main__':
	main()


#for submission in mtg_comment.hot(limit=2:
#	print(submission.title)

# url = 'https://www.reddit.com/r/magicTCG/comments/lxrgyw/just_found_out_a_cool_newb_trick/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
# subreddit_respone = requests.get(subreddit_url)
# time.sleep(.5)
# imagepost_respone = requests.get(imagepost_url)
# time.sleep(.5)

# textpost_respone = requests.get(textpost_url)
# responses = {
	# 'subreddit_respone' : subreddit_respone,
	# 'imagepost_respone' : imagepost_respone, 
	# 'textpost_respone' : textpost_respone
# }
# soups = {}
# for response_name, response in responses.items():
	# print(f'{response_name}:\n\t{response.status_code}')
	# soup = BeautifulSoup(response.text, 'html.parser')
	# print(soup)
	# soups[response_name] = soup
# print(response.status_code)
# print(soup.status_code)