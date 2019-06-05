#######################################################################
#                            IMPORT SECTION                           #
#######################################################################

import argparse
import cx_Oracle as con
import tweepy as tw
import simplejson as json
from tweepy.streaming import StreamListener
import json
import string
import operator
import ast
import requests
import sys
#######################################################################
#                               LISTENER STARTS                       #
#######################################################################


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            
            #Saving the tweets as JSON locally as DR measure.
            with open('ipltweets.json','a') as f:
                f.write(data)

            # Get all the tweet data
            all_data_json = json.dumps(data)
            all_data = json.loads(data)

            data_j = {}
            data_j['data'] = data
            
            r = requests.post(rest_endpoint,json=data_j)

            print "-%-"
            return True
        except KeyboardInterrupt:
            print "User Interrupt Received."
            print "Stopping the Application Now...."
            print "Application stopped!"
            sys.exit(0)
        except BaseException as e:
            print "Error on_data: %s" % str(e)
        return True

    def on_error(self, status):
        print(status)
        return True


#######################################################################
#                               LISTENER ENDS                         #
#######################################################################


#######################################################################
#               SOME API'S TO EXTRACT USER SPECIFIC INFORMATION       #
#######################################################################
def setAccess(cons_key,cons_sec,access_tok,access_sec):
    auth  = tw.OAuthHandler(cons_key, cons_sec)
    auth.set_access_token(access_tok, access_sec)
    return auth

def streamData(auth, term):
    #twitter_stream = tw.Stream(auth, MyListener())
    twitter_stream = tw.Stream(auth, MyListener())
    twitter_stream.filter(track=[term])

def configure_parameters(file_name):
    config_fp = open(file_name,'r')

    config_par = config_fp.readlines()

    config_params = dict()
    for i in config_par:
        key_value = i.strip('\n').split("=")
        config_params[key_value[0]]=key_value[1]

    key = config_params['keyword']
    twitter_cons_key = config_params['consumer_key']
    twitter_cons_sec = config_params['consumer_secret']
    twitter_access_tok = config_params['access_token']
    twitter_access_sec = config_params['access_secret']
    rest_endpoint = config_params['post_endpoint']

    return key,twitter_cons_key,twitter_cons_sec,twitter_access_tok,twitter_access_sec,rest_endpoint



#MAIN FUNCTION
def main():

    #Authentication and Authorization tokens for twitter application
    consumer_key = consumer_key_tw
    consumer_secret = consumer_secret_tw

    access_token = access_token_tw
    access_secret = access_secret_tw
    
    auth = setAccess(consumer_key,consumer_secret,access_token,access_secret)
    
    # Streaming Tweets
    streamData(auth, keyword)


parser = argparse.ArgumentParser(description='Configure the parameters.')
parser.add_argument('config_file', metavar='config_file', help='The file containing the twitter auth tokens and other configuration parameters.')

args = parser.parse_args()

config = args.config_file
keyword,consumer_key_tw,consumer_secret_tw,access_token_tw,access_secret_tw,rest_endpoint=configure_parameters(config)


#Configuration
tablename = 'TweetData'
main()
