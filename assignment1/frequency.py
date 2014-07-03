import sys
import json
import string
from collections import defaultdict

class FrequencyCounter(object):
	def __init__(self, tweet_filename):
		self.tweet_filename = tweet_filename		
		self.unique_words = defaultdict(int)

	def process_words(self):
		with open(self.tweet_filename) as f:
			for line in f:
				tweet = json.loads(line.strip())
				text = tweet.get('text', None)
				if text:
					words = [word.lower().strip(string.punctuation) for word in text.split()]
					for w in words:
						self.unique_words[w] += 1

	def get_frequencies(self):
		all_words_cnt = sum(self.unique_words.values())
		for word, count in self.unique_words.iteritems():			
			print '%s %f' % (word.encode('utf-8'), count / all_words_cnt)


def main():
	tweet_filename = sys.argv[1]
	fc = FrequencyCounter(tweet_filename)
	fc.process_words()
	fc.get_frequencies()


if __name__ == '__main__':
	main()