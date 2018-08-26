import sys
import json
import os
from collections import Counter


def extract_hashtags(tweet):
    # Get hashtags from tweet

    hashtags = []

    if 'entities' in tweet.keys() and tweet['entities'] != None:
        if 'hashtags' in tweet['entities'].keys() and tweet['entities']['hashtags'] != None:
            try:
                for d in  tweet['entities']['hashtags']:
                    hashtags.append(d['text'].encode('utf-8'))  #
            except:
                pass
    return hashtags


def most_used_hashtags(tweet_file):

    hashtags_list = []

    # load tweets from file
    for line in tweet_file:
        tweet = json.loads(line)
        hashtags = extract_hashtags(tweet)

        # add hashtags of this tweet to the full list
        hashtags_list.extend(hashtags)


    return Counter(hashtags_list).most_common(10)


def main():

    with open(sys.argv[1]) as f:
        top_ten = most_used_hashtags(f)
        sys.stdout.writelines('{0} {1}.0\n'.format(*hash) for hash in top_ten)

if __name__ == '__main__':
    main()
