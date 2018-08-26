import sys
import json
import os

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def dict_score_from_file(afinnfile):
    # Builds dictionary of words with sentiment scores from file

    scores = {}
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)
    return scores


def tweet_loc_and_text(tweet):
    # Get location and text from tweet

    # if 'coordinates' in tweet.keys() and tweet['coordinates'] != None:
    #     location = tweet['coordinates']['coordinates']
    location = None
    if 'place' in tweet.keys() and tweet['place'] != None:
        if tweet['place']['country_code'] == 'US':
            location = tweet['place']['full_name'].split()[-1]

            # change from abreviated state to its full name
            # if location in states.keys():
            #     location =  states[location]

    # check if tweet has text, ignore otherwise
    if 'text' in tweet.keys():
        tweet_text = tweet['text'].encode('utf-8')
    else:
        return None, None

    return location, tweet_text


def file_score_and_location(sent_file, tweet_file):
    dict_scores = dict_score_from_file(sent_file)
    dict_state_score = {}

    # load tweets from file
    for line in tweet_file:
        tweet = json.loads(line)
        score_temp = 0
        location, tweet_text = tweet_loc_and_text(tweet)

        # if tweet has a key 'location' and 'text' then calculate tweet sentiment score
        if location:
            for key, value in dict_scores.iteritems():
                if key in tweet_text:
                    score_temp += value

            # build dictionary of state scores
            if location in dict_state_score:
                dict_state_score[location] += score_temp
            else:
                dict_state_score[location] = score_temp

    # max states scores
    max = 0.0
    for state in dict_state_score:
        if dict_state_score[state] > max:
            happiest_state = state
            max = dict_state_score[state]

    return happiest_state


def main():

    with open(sys.argv[1]) as f:
        with open(sys.argv[2]) as g:
            happiest_state = file_score_and_location(f, g)

    print happiest_state


if __name__ == '__main__':
    main()
