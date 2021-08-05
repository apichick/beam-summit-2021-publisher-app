# Copyright 2021 @apichick
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from google.cloud import pubsub_v1
import argparse
import configparser
import json
import tweepy
from google.auth import jwt

class TweetPublisherClient:

    def __init__(self, topic, key_file = None):
        if key_file:
            service_account_info = json.load(open(key_file))
            audience = 'https://pubsub.googleapis.com/google.pubsub.v1.Publisher'
            credentials = jwt.Credentials.from_service_account_info(
                service_account_info, audience=audience
            )
            self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        else:
            self.publisher = pubsub_v1.PublisherClient()
        self.topic = topic

    def publish(self, data):
        future = self.publisher.publish(self.topic, data.encode('utf-8'))
        return future.result()

class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, api, topic, key_file = None):
        super().__init__(api)
        self.publisher = TweetPublisherClient(topic, key_file)

    def on_status(self, status):
        print('Tweet received')
        self.publisher.publish(json.dumps(status._json))
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

def parse_list(s):
    return [float(item) for item in s.split(',')]

def main(args):
    config = configparser.ConfigParser()
    config.read(args.config_file)
    auth = tweepy.OAuthHandler(config['twitter']['api_key'], config['twitter']['api_key_secret'])
    auth.set_access_token(config['twitter']['access_token'], config['twitter']['access_token_secret'])
    api = tweepy.API(auth)
    listener = TweetStreamListener(api, config['pubsub']['topic'], config['pubsub']['key_file'])
    twitterStream = tweepy.Stream(api.auth, listener)
    twitterStream.filter(locations=args.locations)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--locations', help='Locations', type=parse_list, required=True)
    parser.add_argument('--config-file', help='Configuration file')
    args = parser.parse_args()
    main(args)

