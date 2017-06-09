import sys
import json

def hw():
    print 'Hello, world!'

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
    print tweet_score

def main():
    sent_file = sys.argv[1]         #AFINN-111.txt sentiment file
    tweet_file = open(sys.argv[2])  #output.txt tweet file
    #hw()
    #lines(sent_file)
    #lines(tweet_file)

    scores = getSentiment(sent_file)
    #print scores.items()
    tweet_text = []
    for each_line in tweet_file:
        try:
            tweet_json = json.loads(each_line)
            tweet_text = tweet_json['text'].split()
            tweet_score = getTweetSentiment(tweet_text,scores)
        except:
            pass
if __name__ == '__main__':
    main()
