import FileSave
from datetime import datetime


class Indexer:

    def __init__(self, db=None, filename=None, hour_range=None):
        self.db = db
        if db is not None:
            self.tweets = db.search_tweets()
        if filename is not None:
            self.tweets = FileSave.load(filename)
        self.hour_range = hour_range
        self.clusters = []
        self.already_clustered = False

    def create_clusters(self, clustering_method, print_progress=False):
        tweets = self.get_tweets_to_process()
        if len(tweets) < 100:
            print("Not enough tweets to process")
            return
        self.clusters = clustering_method.cluster(tweets, print_progress=print_progress)

    def update_db(self):
        if self.db is not None:
            self.tweets = self.db.search_tweets()

    def get_tweets_to_process(self):
        if self.hour_range is not None:
            timestamp_window = datetime.now().timestamp() - (self.hour_range * 3600)
            timestamp_window_ms = timestamp_window * 1000
            recent_tweets = []
            for tweet in self.tweets:
                if int(tweet['timestamp_ms']) > timestamp_window_ms:
                    recent_tweets.append(tweet)
            return recent_tweets
        else:
            return self.tweets

    def describe_clusters(self, minimum_size=1):
        for number, cluster in enumerate(self.clusters):
            if len(cluster.tweets) >= minimum_size:
                cluster.describe(number)

    def classify(self, dictionary, skip_processed=False):
        for cluster in self.clusters:
            if not skip_processed or (not cluster.processed and skip_processed):
                cluster.detect_topic(dictionary)

    def delete_cluster(self, cluster_number):
        cluster = self.clusters[cluster_number]
        self.db.delete_tweets(cluster)
        del self.clusters[cluster_number]

    def save(self, filename):
        FileSave.save(self.clusters, filename)

    def load(self, filename=None):
        self.clusters = FileSave.load(filename)
        self.already_clustered = True

    def get_relevant_clusters(self, topic, minimum_size=1):
        clusters = []
        for cluster in self.clusters:
            if cluster.topic == topic and len(cluster.tweets) >= minimum_size:
                clusters.append(cluster)
        return clusters
