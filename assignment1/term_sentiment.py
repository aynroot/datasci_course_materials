import sys
import json
import string
from collections import defaultdict

def get_tweets(tweet_filename):
    with open(tweet_filename) as f:
        for line in f:
            tweet = json.loads(line.strip())
            yield tweet


def get_words_sentiments(filename):
    result = {}
    with open(filename) as f:
        for line in f:
            word, value = line.strip().split('\t')
            result[word] = int(value)
    return result


words_pos_characteristics = defaultdict(int)
words_neg_characteristics = defaultdict(int)

def process_tweet(tweet, sentiments):   
    text = tweet.get('text', None)
    if text:
        words = [word.lower().strip(string.punctuation) for word in text.split()]
        tweet_pos_sentiment = 0
        tweet_neg_sentiment = 0
        for word in words:
            if word in sentiments:
                if sentiments[word] > 0:
                    tweet_pos_sentiment += sentiments[word]
                else:
                    tweet_neg_sentiment += abs(sentiments[word])
        for word in words:
            if word not in sentiments:
                words_pos_characteristics[word] += tweet_pos_sentiment
                words_neg_characteristics[word] += tweet_neg_sentiment


def get_new_words_sentiments():
    new_words_sentiments = {}
    for word in words_pos_characteristics:
        a = words_pos_characteristics[word] - words_neg_characteristics[word]
        b = words_pos_characteristics[word] + words_neg_characteristics[word]
        new_words_sentiments[word] = float(a) / b if b != 0 else 0
    return new_words_sentiments


def main():
    sentiments_filename = sys.argv[1]
    tweet_filename = sys.argv[2]
    words_sentiments = get_words_sentiments(sentiments_filename)    
    for tweet in get_tweets(tweet_filename):
        process_tweet(tweet, words_sentiments)        
    new_words_sentiments = get_new_words_sentiments()
    for word, sentiment in new_words_sentiments.iteritems():
        print '%s %f' % (word, sentiment)


if __name__ == '__main__':
    main()
