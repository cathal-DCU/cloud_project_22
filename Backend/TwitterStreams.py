import os
import re
import time
import json
import socket

import tweepy
from tweepy import Stream


# Documentation - https://docs.tweepy.org/en/stable/streaming.html
# Inherits from the Stream in tweepy - provides additional functionality
class TweetStream(Stream):
    
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, client_connection=None, rate_limit_delay=None, time_limit=None, tweet_limit=None, message_Handler=None, batch_size=None, batch_handler=None):
        
        # Set client connection
        self.client_connection = client_connection

        # Set rate limt
        self.rate_limit_delay = rate_limit_delay

        # Set time limit
        self.start_time = time.time()
        self.time_limit = time_limit
        
        # Set tweet limit
        self.tweet_limit = tweet_limit
        self.tweet_count = 0

        # Set batching
        self.batch_size = batch_size
        self.batch_handler = batch_handler
        self.batch = []

        # Set message handler
        self.message_handler = message_Handler
        
        # Initialize super
        super(TweetStream, self).__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        
    def check_continue_time_limit(self):
        
        # Check time limit if set
        if self.time_limit is not None:
            if (time.time() - self.start_time) > self.time_limit:
                return False
        return True
    
    def check_continue_tweet_limit(self):
        # Check tweet limit if set
        if self.tweet_limit is not None:
            if self.tweet_limit <= self.tweet_count :
                return False
        return True

    def close_connections(self):
        
        # Process batch before disconnecting
        self.process_batch(is_disconnecting=True)

        print("Disconnecting...")

        # Disconnect client connection if provided
        if self.client_connection is not None:
           self.client_connection.close()

        # Disconnect stream
        self.disconnect()

        print("Disconnected.")


    def send_to_client(self, data):

        if self.client_connection is not None:
            # Send tweet data to client connection
            self.client_connection.send(data)

            # Send new line delimiter to client connection
            self.client_connection.send(str('\n').encode('utf-8'))


    def process_batch(self, is_disconnecting=False):
        if self.batch_size is not None:
            if len(self.batch) == self.batch_size or (is_disconnecting == True and len(self.batch) > 0):
                # Write to batch handler if provided
                if self.batch_handler is not None:
                    self.batch_handler(self.batch)
            
                # Write to client connection if provided
                self.send_to_client(self.batch)

                # Clear batch
                self.batch.clear()


    def on_data(self, data):
        try:
            
            # Check for time limit
            if self.check_continue_time_limit() is False:
                print('Time limit hit.')
                self.close_connections()
                return False

            # Check for tweet limit
            if self.check_continue_tweet_limit() is False:
                print('Tweet limit hit.')
                self.close_connections()
                return False
            
            # Check for limit message from twitter
            if '{"limit":' in str(data):
                print('Twitter rate limit - {}'.format(str(data)))
                return True

            # Process batch
            if self.batch_size is not None:
                self.batch.append(data)
                self.process_batch()

            # Write to message handler if provided
            if self.message_handler is not None:
                self.message_handler(data)

            # Write to client connection if provided
            if self.client_connection is not None:
                self.send_to_client(data)

            # Update tweet count
            self.tweet_count = self.tweet_count + 1

            # Check for rate limit delay
            if self.rate_limit_delay is not None:
                time.sleep(self.rate_limit_delay)
                
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            self.close_connections()
            return False
        
        return True

    def if_error(self, status):
        print(status)
        return True