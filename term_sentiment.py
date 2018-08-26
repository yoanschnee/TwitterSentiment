import json
import os.path
import re
import sys


 
def dict_score_from_file(open_file):
    # Builds dictionary of word and its corresponding sentiment score from file

    scores = {} # initialize an empty dictionary

    for line in open_file:
        word, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[word] = int(score)  # Coniert the score to an integer.

    return scores


def file_score(sent_file, tweet_file):
    dict_scores = dict_score_from_file(sent_file)
    score_list = []
    tweet_list = []

    # load tweets from file
    for line in tweet_file:
        tweet = json.loads(line)
        score_temp = 0

        # if tweet has a key 'text' then analyse tweet sentiment
        if 'text' in tweet.keys():
            tweet_text = tweet['text'].encode('utf-8')

            for key, value in dict_scores.iteritems():
                if key in tweet_text:
                    score_temp += value

            # store score in list as requested
            tweet_list.append(tweet_text)
            score_list.append(score_temp)

    return tweet_list, score_list, dict_scores


def tweet_to_word_list(tweet):
    # Remove punctuations and non-alphanumeric chars from each tweet string

    tweet = re.sub('[^A-Za-z]+', ' ', tweet)
    #print encoded_tweet

    words = tweet.split()

    # Filter unnecessary words
    for w in words:
        if w.startswith("RT") or w.startswith("www") or w.startswith("http"):
            words.remove(w)

    return words


def dict_score_from_file(afinn_file):
    # Builds dictionnary of words with sentiment scores from file
    
    scores = {} # initialize an empty dictionary
    for line in afinn_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Coniert the score to an integer.
    return scores


def main(tweet_list, score_list, dict_AFINN):
    # Builds a new dictonary and corresponding sentiment score of unseen words in the reference dictionary

    d = {}

    for tweet, score in zip(tweet_list, score_list):     # new words appearing in positive or negative tweets

    # For each word in tweets, an array of the sentiment scores of the tweets in which it appears is constructed
        for word in tweet_to_word_list(tweet):
            word = word.lower()

            if (word not in dict_AFINN) and (len(word) > 2):

                if word not in d:
                    d[word] = [float(score)]

                else:
                    d[word].append(float(score))

    # Compute word score, add to dictionary and print out
    for word, score_list in d.iteritems():
        d[word] = float(sum(score_list) / float(len(score_list)))
        print word + ' ', d[word]

    return d

if __name__ == '__main__':


    # Builds two files of tweet (text) list and their corresponding score if they do not exist already
    if not os.path.isfile('tweet_file.txt') or not os.path.isfile('score_file.txt'):
        with open(sys.argv[1]) as f: 
            with open(sys.argv[2]) as g:
                tweet_list, score_list, dict_scores = file_score(f, g)

    # or if they already exist in folder
    else:
        with open('tweet_file.txt') as f:
            tweet_list = f.read().splitlines()
        with open('score_file.txt') as g:
            score_list = g.read().splitlines()

    # Run main()
    main(tweet_list, score_list, dict_scores)

    
