import sys
import json


def main():
    tweet_file = open(sys.argv[1])  #output.txt tweet file
    tweet_text = []
    frequency_dict = {}
    for each_line in tweet_file:
        try:
            tweet_json = json.loads(each_line)
            tweet_text = tweet_json['text'].split()
        except:
            pass

        for each_word in tweet_text:
            if each_word not in frequency_dict:
                frequency_dict[each_word.encode('utf-8')] = 1
            else:
                frequency_dict[each_word.encode('utf-8')] = frequency_dict[each_word.encode('utf-8')] +1

    for key, value in  frequency_dict.items():
        print key," ",value
            

if __name__ == '__main__':
    main()

