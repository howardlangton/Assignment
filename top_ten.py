import sys
import json
import operator

def main():
    tweet_file = open(sys.argv[1])  #output.txt tweet file
    frequency_dict = {}
    tweet_text = []    
    for each_line in tweet_file:
        try:
            tweet_json = json.loads(each_line)
            #for key in tweet_json.keys():
            #    print key
            tweet_text = tweet_json[u'entities'][u'hashtags']
            if tweet_text:
                for hash_tag in tweet_text:
                    if hash_tag['text'] not in frequency_dict:
                        frequency_dict[hash_tag['text']] = 1
                    else:
                        frequency_dict[hash_tag['text']] = frequency_dict[hash_tag['text']] + 1
                    #print hash_tag['text']
        except:
            pass
    sorted_frequency_dict = sorted(frequency_dict.items(), key=operator.itemgetter(1),reverse=True)
    count = 0
    for key, value in sorted_frequency_dict:
         print key,' ',value
         count += 1
         if count == 10:
             break
'''
        for each_word in tweet_text:
            if each_word not in frequency_dict:
                frequency_dict[each_word.encode('utf-8')] = 1
            else:
                frequency_dict[each_word.encode('utf-8')] = frequency_dict[each_word.encode('utf-8')] +1

    for key, value in  frequency_dict.items():
        print key," ",value
'''            

if __name__ == '__main__':
    main()

