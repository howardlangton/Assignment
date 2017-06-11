import sys
import json


def states(isitastate):
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
    isitastate = isitastate.strip()
    if ( (isitastate in states)):
        return isitastate
    else:
        return 'UNKNOWN'

def lines(fp):
    print str(len(fp.readlines()))

def getSentiment(sentiment_file):
    try:
        s_fd = open(sentiment_file,'r')
        myscores = {}
        for each_line in s_fd:
            term, score = each_line.split("\t")
            myscores[term] = int(score)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Cannot find " + sentiment_file
        sys.exit()
    except: #handle other exceptions
        print "Unexpected error:", sys.exc_info()[0]
        sys.exit()
    return myscores

def getTweetSentiment(mytweet_text,myscores_dict):
    tweet_score = 0
    for each_item in mytweet_text:
        try:
            if each_item in myscores_dict:
                tweet_score = tweet_score + myscores_dict[each_item]
        except:
            pass
    #print tweet_score
    return tweet_score

def getUSstate(mytweet_json):
    full_name = []
    state_name = 'UNKNOWN'
    if 'place' in mytweet_json:
        place_data = mytweet_json[u'place']
        if place_data is not None:
            country_code = mytweet_json[u'place'][u'country_code']
            if country_code == 'US':
               full_name = mytweet_json[u'place'][u'full_name'].split(',')
               state_name = full_name[1].strip()
               state_name = states(state_name)
               #print full_name
    return state_name

def addStateScore(mystate, mytweet_score, mystate_scores):
    if mystate in state_scores:
        state_scores[mystate] = state_scores[mystate] + mytweet_score
    else:
        state_scores[mystate] = mytweet_score
    #print state_scores
 
def main():
    sent_file = sys.argv[1]         #AFINN-111.txt sentiment file
    tweet_file = open(sys.argv[2])  #output.txt tweet file

    scores = getSentiment(sent_file)
    tweet_text = []
    global state_scores
    state_scores = {}
    for each_line in tweet_file:
        try:
            tweet_json = json.loads(each_line)
            state = getUSstate(tweet_json)
            if state != 'UNKNOWN':
                #print state
                tweet_text = tweet_json['text'].split()
                tweet_score = getTweetSentiment(tweet_text,scores)
                #print state,' ',tweet_score
                addStateScore(state, tweet_score, state_scores)
        except:
            pass
    #print state_scores
    happiest_state_score, happiest_state = max(zip(state_scores.values(), state_scores.keys()))
    #print happiest_state, happiest_state_score
    print happiest_state

if __name__ == '__main__':
    main()
