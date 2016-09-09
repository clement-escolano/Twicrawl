# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import ClusteringAlgorithms.string_tools as st

# Import necessary methods for tweet handling
from json import loads as jsonify

# Variables that contains the user credentials to access Twitter API
access_token = "some_token"
access_token_secret = "some_secret"
consumer_key = "some_key"
consumer_secret = "some_secret"

# Keys stored in the database
keys = ['timestamp_ms', 'lang', 'text']
user_keys = ['id', 'name', 'screen_name', 'followers_count', 'verified', 'statuses_count']


class CustomListener(StreamListener):

    def __init__(self, action_on_data):
        super(CustomListener, self).__init__()
        self.action_on_data = action_on_data

    def on_data(self, data):
        try:
            self.action_on_data(data)
        except Exception as e:
            print(e)
        return True

    def on_error(self, status):
        print(status)


class TwitterStream:

    def __init__(self, action_on_data):
        # This handles Twitter authentication and the connection to Twitter Streaming API
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        # Create the stream to listen to Twitter tweets
        listener = CustomListener(action_on_data)
        self.stream = Stream(auth, listener)

    def get_filter(self, keywords):
        self.stream.filter(track=keywords)

    def get_sample(self):
        self.stream.sample()

    def get_user(self, user_ids):
        self.stream.filter(follow=user_ids)


class Tweet:

    def __init__(self, tweet=None, db=None):
        self.tweet = tweet
        if tweet is not None and db is not None:
            self.user = db.find_user(tweet['user'])
        else:
            self.user = None

    def parse_data(self, data):
        data = jsonify(data)
        tweet = self.filter_keys(data, keys)
        tweet['urls'] = [self.filter_keys(url, ['expanded_url']) for url in data['entities']['urls']]
        user = self.filter_keys(data['user'], user_keys)
        tweet['user'] = user['id']
        tweet['text'] = tweet['text'].replace('\n', ' ')
        self.tweet = tweet
        self.user = user

    @staticmethod
    def filter_keys(dict_to_filter, keys):
        result = dict()
        for key in keys:
            if key in dict_to_filter:
                result[key] = dict_to_filter[key]
        return result

    def is_valid(self, keywords):
        # Check if tweet is in english or not
        if self.tweet['lang'] != 'en':
            return False
        # Check if keywords are indeed in the tweet
        tweet_words = st.tokenizer(st.preprocessor(self.tweet), stem=False)
        if not st.check_intersection_non_empty(tweet_words, keywords):
            return False
        return True

    def __str__(self):
        return self.tweet['text']
