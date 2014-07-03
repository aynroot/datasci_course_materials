import sys
import json
import string
from collections import defaultdict

class TopTenHashtagsGetter(object):
	def __init__(self, tweet_filename):
		self.tweet_filename = tweet_filename
		self.unique_hashtags = defaultdict(int)

	def process_hashtags(self):
		with open(self.tweet_filename) as f:
			for line in f:
				tweet = json.loads(line.strip())
				entities = tweet.get('entities', None)
				hashtags = entities.get('hashtags', []) if entities else []
				if hashtags:					
					for hashtag in hashtags:
						self.unique_hashtags[hashtag['text']] += 1

	def get_top_ten(self):
		all_hashtags_cnt = sum(self.unique_hashtags.values())
		sorted_hashtags = sorted(self.unique_hashtags.iteritems(), key=lambda x: x[1], reverse=True)
		for hashtag, count in sorted_hashtags[:10]:
			print '%s %f' % (hashtag.encode('utf-8'), float(count))


def main():
	tweet_filename = sys.argv[1]
	tt_getter = TopTenHashtagsGetter(tweet_filename)
	tt_getter.process_hashtags()
	tt_getter.get_top_ten()

if __name__ == '__main__':
	main()