
import os
import sys
import time
import json
import socket

import TwitterCredentials
import TwitterStreams

def message_handler(data):
    print('Message Handler...')
    message = json.loads( data )
    print(message)

def batch_handler(batch):
    print('Batch Handler...')
    print(batch)

def send_tweets_to_client_connection(client_connection, topic):
    # Create twitter stream
    twitter_stream = TwitterStreams.TweetStream(\
        TwitterCredentials.consumer_key\
        , TwitterCredentials.consumer_secret\
        , TwitterCredentials.access_token\
        , TwitterCredentials.access_token_secret\
        , client_connection\
        , message_Handler=message_handler\
        #, rate_limit_delay=1\
        #, tweet_limit=10\
        #, time_limit=5\
        #, batch_size=5\
        #, batch_handler=batch_handler\
        )
    
    # Filter for topic
    twitter_stream.filter(track=topic, languages=["en"])


def start_client_connection_server(topic):
     # Get host name and port number for service.
     host = socket.gethostname()
     port = 5555
    
     # Initialize a socket
     s = socket.socket()
     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
     # Binding host and port
     s.bind((host, port))

     print("Listening on port {} with topic {}:".format(port,topic))

     # Waiting for client connection
     s.listen(5)
    
     # Establish connection with client
     client_connection, addr = s.accept()  

     # Start streaming tweets to client
     with client_connection:
         print("Connected with client: " + str(addr))

         # Send tweets to client through the socket connection
         send_tweets_to_client_connection(client_connection, topic)


if __name__ == "__main__":
    
    # Get topic from args
    args = sys.argv[1:]
    if len(args) == 0:
        # Start client connection server - with test data
        topic = 'batman'
        #print("Topic = {}".format(args))
        start_client_connection_server(topic)
        # time.sleep(10)
        # print("Finished.")
    else:
        # Start client connection server
        topic = args
        #print("Topic = {}".format(args))
        start_client_connection_server(topic)
        # time.sleep(5)
        # print("Finished.")

    