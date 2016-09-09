from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import ClusteringAlgorithms.string_tools as st
from ClusteringAlgorithms.Cluster import Cluster
from tqdm import tqdm


NUMBER_OF_CLUSTERS = 10


class KMeansClustering:

    def __init__(self, preprocessor=st.preprocessor, tokenizer=st.tokenizer):
        self.preprocessor = preprocessor
        self.tokenizer = tokenizer
        self.tfidf_vectorizer = TfidfVectorizer(max_df=0.1, max_features=10000, lowercase=False,
                                                min_df=3, preprocessor=self.preprocessor,
                                                use_idf=True, tokenizer=self.tokenizer, ngram_range=(1, 3))
        self.tfidf_vectorizer_flexible = TfidfVectorizer(max_df=0.7, max_features=10000, lowercase=False,
                                                         min_df=3, preprocessor=self.preprocessor,
                                                         use_idf=True, tokenizer=self.tokenizer, ngram_range=(1, 3))
        self.labels = []
        self.clusters = []

    @staticmethod
    def is_well_clustered(cluster):
        most_common_words = cluster.get_most_common_words()
        well_clustered = True
        if len(most_common_words) > 6:
            well_clustered = well_clustered and most_common_words[6][1] / len(cluster.tweets) > 0.5
        if len(most_common_words) > 3:
            well_clustered = well_clustered and most_common_words[3][1] / len(cluster.tweets) > 0.7
        return well_clustered

    def cluster(self, tweets, num_clusters=NUMBER_OF_CLUSTERS, already_got_error=False, print_progress=False):
        pbar = tqdm(total=len(tweets)) if print_progress else None
        try:
            self.labels = []
            self.clusters = []
            if already_got_error:
                tfidf_matrix = self.tfidf_vectorizer_flexible.fit_transform(tweets)
            else:
                tfidf_matrix = self.tfidf_vectorizer.fit_transform(tweets)
            kmeans = KMeans(n_clusters=num_clusters)
            kmeans.fit(tfidf_matrix)
            self.labels = kmeans.labels_.tolist()
            self.clusters = [Cluster() for _ in range(num_clusters)]
            for index, label in enumerate(self.labels):
                self.clusters[label].add_tweet(tweets[index])
        except ValueError:
            if not already_got_error:
                # if this is the first error, try with a higher max_df
                self.clusters = self.cluster(tweets, num_clusters=num_clusters, already_got_error=True)
            else:
                # If there is an error with no terms remaining, then throws an error
                raise ValueError("Impossible to cluster")
        if print_progress:
            pbar.update(len(tweets))
            pbar.close()
        return self.clusters
