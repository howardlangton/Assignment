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
    # return tuple of negative,positive values in tweet
    tweet_score_pos = 0
    tweet_score_neg = 0
    for each_item in mytweet_text:
        try:
            if each_item in myscores_dict:
                if myscores_dict[each_item] > 0:
                    tweet_score_pos = tweet_score_pos + myscores_dict[each_item]
                else:
                    tweet_score_neg = tweet_score_neg + myscores_dict[each_item]
        except:
            pass
    #print tweet_score_neg, tweet_score_pos
    return tweet_score_neg, tweet_score_pos

def main():
    sent_file = sys.argv[1]         #AFINN-111.txt sentiment file
    tweet_file = open(sys.argv[2])  #output.txt tweet file
    
    noterms = {}
    scores_dict = getSentiment(sent_file) # dict containing word:value
    #print scores.items()
    tweet_text = []
    for each_line in tweet_file:
        try:
            tweet_json = json.loads(each_line)			#load each line in the tweet file
            tweet_text = tweet_json['text'].split()		#put each word into a list
            tweet_score_neg, tweet_score_pos = getTweetSentiment(tweet_text,scores_dict)  #get neg,pos scors efor the tweet
            #print ("tweet score is " + tweet_score)
            #now we have a score fo rthe tweet we need to creat a score for each word that isn't assigned one in the term file
            
            if (tweet_score_neg == 0) and (tweet_score_pos == 0):
                continue
            
            for each_word in tweet_text:
                if each_word not in scores_dict:
                    if each_word not in noterms:
                        noterms[each_word]={}
                        noterms[each_word]['positive'] = 0.0
                        noterms[each_word]['negative'] = 0.0
                        noterms[each_word]['value'] = 0.0
                    
                noterms[each_word]['positive'] = noterms[each_word]['positive'] + tweet_score_pos
                noterms[each_word]['negative']=  noterms[each_word]['negative'] + tweet_score_neg
        except:
            pass
        for each_item in noterms: 
            posval = noterms[each_item]['positive']
            negval = noterms[each_item]['negative']
            if posval == 0:
                posval = 1
            if negval == 0:
                negval = -1
            if abs(posval) >= abs(negval):
                noterms[each_item]['value'] = float(posval) / float(abs(negval))
            else: 
                noterms[each_item]['value'] = float(negval) / float(abs(posval))
            print each_item.encode('utf-8').strip()," ",str(noterms[each_item]['value']).strip()

if __name__ == '__main__':
    main()
