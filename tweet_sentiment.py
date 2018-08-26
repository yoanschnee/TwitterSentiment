import sys
import json
import os 


def dict_score_from_file(afinnfile):
    # Builds dictionnary of words with sentiment scores from file

    scores = {}
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)
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


def main():
    score_list = []
    tweet_list = []
    with open(sys.argv[1]) as f:
        with open(sys.argv[2]) as g:
            tweet_list, score_list = file_score(f, g)
    for score in score_list:
        print score
   #  with open("score_file.txt", 'wb') as score_file:
   #      score_file.writelines(['%s\n' % str(item) for item in score_list])
   #  with open('tweet_file.txt', 'wb') as tweet_file:
   #      tweet_file.writelines(['%s \n' % item for item in tweet_list])

if __name__ == '__main__':
    main()
