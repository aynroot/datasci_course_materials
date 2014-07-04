import sys
import json
import string
from collections import defaultdict

from tweet_sentiment import get_words_sentiments, get_tweet_sentiment
from states import states


def get_tweets(tweet_filename):
    with open(tweet_filename) as f:
        for line in f:
            tweet = json.loads(line.strip())
            yield tweet


def check_coordinates(tweet_filename):
    tweets_cnt = 0
    coords_cnt = 0
    for tweet in get_tweets(tweet_filename):
        if tweet.get('text'):
            tweets_cnt += 1
            coords = tweet.get('coordinates')
            if coords and coords.get('coordinates'):
                coords_cnt += 1
    print coords_cnt, '/', tweets_cnt
    print '%.2f' % (coords_cnt / float(tweets_cnt))


def check_place(tweet_filename):
    tweets_cnt = 0
    place_cnt = 0
    for tweet in get_tweets(tweet_filename):
        if tweet.get('text'):
            tweets_cnt += 1
            place = tweet.get('place')
            if place:
                full_name = place.get('full_name')
                name = place.get('name')
                attributes = place.get('attributes')
                if full_name or name or attributes:
                    place_cnt += 1            
    print place_cnt, '/', tweets_cnt
    print '%.2f' % (place_cnt / float(tweets_cnt))


def check_if_has_state_name(location):
    words = [word.strip(string.punctuation) for word in location.split()]    
    for word in words:        
        if len(word) == 2 and word in states:
            return word
    return False


def get_states_sentiments(tweet_filename, sentiments):    
    states_sentiments = defaultdict(list)
    for tweet in get_tweets(tweet_filename):
        if tweet.get('text'):
            user = tweet.get('user')
            location = user.get('location')
            if location:
                state = check_if_has_state_name(location)
                if state:
                    states_sentiments[state].append(get_tweet_sentiment(tweet, sentiments))
    for state, sentiments in states_sentiments.iteritems():
        final_result = float(sum(sentiments)) / len(sentiments)
        states_sentiments[state] = final_result
    return states_sentiments


def get_happiest_state(states_sentiments):
    max_sentiment = -100000
    happiest_state = ''
    for state, sentiment in states_sentiments.iteritems():
        if sentiment > max_sentiment:
            max_sentiment = sentiment
            happiest_state = state
    return happiest_state


def main():
    sentiments_filename = sys.argv[1]
    tweet_filename = sys.argv[2]
    words_sentiments = get_words_sentiments(sentiments_filename)    
    states_sentiments = get_states_sentiments(tweet_filename, words_sentiments)
    state = get_happiest_state(states_sentiments)    
    print state
    

if __name__ == '__main__':
    main()
