from Mongo import Mongo
from FileSave import save, load
from Twitter import TwitterStream, Tweet
import keywords as kw


class Crawler:

    def __init__(self, db=None, filename=None, keywords=None, extended_keywords=None, verbose=True):
        self.db = db
        self.filename = filename
        self.store_to_file = filename is not None
        self.tweets = []
        if self.store_to_file:
            try:
                self.tweets = load(filename)
            except FileNotFoundError:
                pass
        self.count = 0
        self.stream = TwitterStream(self.process_tweet)
        self.verbose = verbose
        self.keywords = keywords
        if extended_keywords is None:
            self.extended_keywords = keywords
        else:
            self.extended_keywords = extended_keywords

    def process_tweet(self, data):
        # noinspection PyBroadException
        try:
            tweet = Tweet()
            tweet.parse_data(data)
            if tweet.is_valid(self.extended_keywords):
                if self.store_to_file:
                    self.tweets.append(tweet)
                else:
                    self.db.save_tweet(tweet)
                self.count += 1
                if self.verbose:
                    print('Tweet added   : ' + str(tweet))
            else:
                if self.verbose:
                    print('Tweet dropped : ' + str(tweet))
        except Exception:
            print('Processing of a tweet failed')

    def run(self):
        try:
            print("Beginning of crawling")
            if self.keywords is None:
                self.stream.get_sample()
            else:
                self.stream.get_filter(self.keywords)
        except KeyboardInterrupt:
            if self.store_to_file:
                save(self.tweets, self.filename)
            print("\nEnd of crawling")
            if self.verbose:
                print(str(self.count) + " tweets added this session")
                print(str(self.db.number_of_tweets()) + " tweets in the database")

if __name__ == '__main__':
    keywords = kw.primary_keywords
    db = Mongo(address="mongodb://localhost:27018", name="kw2")
    crawler = Crawler(db=db, keywords=keywords, extended_keywords=kw.all_keywords)
    crawler.run()
