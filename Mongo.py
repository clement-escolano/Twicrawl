from pymongo import MongoClient, TEXT, errors

# Address and name of database
default_address = 'mongodb://localhost:27018'
default_name = 'test'


class Mongo:

    def __init__(self, address=default_address, name=default_name):
        client = MongoClient(address)
        self.db = client[name]
        try:
            self.db.tweets.create_index([('text', TEXT)])
        except errors.OperationFailure:
            print("Indexes and research won't work with Mongo 2.")

    def save_tweet(self, tweet):
        if tweet.tweet is not None:
            self.db.tweets.insert_one(tweet.tweet)
        if tweet.user is not None:
            if self.db.users.find({'id': tweet.user['id']}).count() == 0:
                self.db.users.insert_one(tweet.user)

    def save_word(self, word, score):
        if self.db.dictionary.find_one({'word': word}) is None:
            self.db.dictionary.insert_one({'word': word, 'score': score})
        else:
            self.db.dictionary.update_one({'word': word}, {
                '$set': {
                    'score': score
                }
            })

    def get_words(self):
        return self.db.dictionary.find()

    def search_tweets(self, query='', user=''):
        mongo_query = {}
        if query != '':
            mongo_query['$text'] = {'$search': query}
        if user != '':
            mongo_query['user'] = user
        return list(self.db.tweets.find(mongo_query))

    def search_users(self, user_id=''):
        mongo_query = {}
        if user_id != '':
            mongo_query['id'] = user_id
        return list(self.db.users.find(mongo_query))

    def popular_users(self):
        return list(self.db.users.find().sort("on_topic_counter", 1))

    def delete_tweet(self, tweet):
        self.db.tweets.remove({"_id": tweet['_id']})

    def delete_tweets(self, cluster):
        tweets = cluster.tweets
        for tweet in tweets:
            self.delete_tweet(tweet)

    def find_user(self, user_id):
        return self.db.users.find({id: user_id})

    def number_of_tweets(self):
        return self.db.tweets.count()
