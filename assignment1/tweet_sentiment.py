import sys
import json
import string


def count_lines(fp):
    print str(len(fp.readlines()))


def get_words_sentiments(filename):
    result = {}
    with open(filename) as f:
        for line in f:
            word, value = line.strip().split('\t')
            result[word] = int(value)
    return result


def get_tweet_sentiment(tweet, sentiments):
    text = tweet.get('text', None)
    if text:
        words = [word.lower().strip(string.punctuation) for word in text.split()]                
        result = sum([sentiments.get(word, 0) for word in words])
        return result
    return 0


def main():
    words_sentiments_filename = sys.argv[1]
    tweet_filename = sys.argv[2]

    words_sentiments = get_words_sentiments(words_sentiments_filename)        
    with open(tweet_filename) as f:
        for line in f:
            tweet = json.loads(line)            
            ts = get_tweet_sentiment(tweet, words_sentiments)
            print ts

    
if __name__ == '__main__':
    main()
