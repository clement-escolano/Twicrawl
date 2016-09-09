from random import random
import ClusteringAlgorithms.string_tools as st
from tqdm import tqdm
from ClusteringAlgorithms.Cluster import Cluster
from operator import mul as multiply, add as addition
from functools import reduce

alpha = 0.1
beta = 0.01
number_of_iterations = 10


class GSDMMClustering:
    def __init__(self, number_of_clusters=None):
        self.tweets = []
        self.documents = []
        self.cluster_labels = []
        self.number_of_clusters = number_of_clusters

        self.vocabulary = dict()
        self.number_of_documents_per_cluster = []
        self.number_of_words_per_cluster = []
        self.number_of_occurences_of_word_per_cluster = []

    def initialise(self, tweets):
        self.tweets = tweets
        self.documents = []
        for tweet in tweets:
            self.documents.append(st.unique_words(st.tokenizer(st.preprocessor(tweet))))
        self.cluster_labels = [0 for _ in range(len(tweets))]
        if self.number_of_clusters is None:
            self.number_of_clusters = int(len(tweets) / 3)

        self.number_of_documents_per_cluster = [0 for _ in range(self.number_of_clusters)]
        self.number_of_words_per_cluster = [0 for _ in range(self.number_of_clusters)]
        self.number_of_occurences_of_word_per_cluster = [dict() for _ in range(self.number_of_clusters)]

        for (index, document) in enumerate(self.documents):
            cluster_label = self.get_random_cluster()
            self.cluster_labels[index] = cluster_label
            self.move_document_to_cluster(document, cluster_label)
            for word in document:
                self.vocabulary[word] = True

    def move_document_to_cluster(self, document, cluster_label):
        self.number_of_documents_per_cluster[cluster_label] += 1
        self.number_of_words_per_cluster[cluster_label] += len(document)
        for word in document:
            self.add_word_to_cluster(word, cluster_label)

    def add_word_to_cluster(self, word, cluster_label):
        dictionary = self.number_of_occurences_of_word_per_cluster[cluster_label]
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1

    def remove_document_from_cluster(self, document, cluster_label):
        self.number_of_documents_per_cluster[cluster_label] -= 1
        self.number_of_words_per_cluster[cluster_label] -= len(document)
        for word in document:
            self.substract_word_from_cluster(word, cluster_label)

    def substract_word_from_cluster(self, word, cluster_label):
        dictionary = self.number_of_occurences_of_word_per_cluster[cluster_label]
        if word in dictionary:
            dictionary[word] -= 1
        else:
            dictionary[word] = 0
            print("Error. Number of occurences of word " + word + " should be existing if we try to substract it.")

    def cluster(self, tweets, print_progress=False):
        self.initialise(tweets)
        pbar = tqdm(total=number_of_iterations * len(self.documents)) if print_progress else None
        for _ in range(number_of_iterations):
            for (index, document) in enumerate(self.documents):
                cluster_label = self.cluster_labels[index]
                self.remove_document_from_cluster(document, cluster_label)
                cluster_label = self.get_cluster_label_from_document(document)
                self.move_document_to_cluster(document, cluster_label)
                pbar.update(1)
        if print_progress:
            pbar.close()
        return self.build_clusters_from_labels()

    def build_clusters_from_labels(self):
        clusters = [Cluster() for _ in range(self.number_of_clusters)]
        for (tweet, cluster_label) in zip(self.tweets, self.cluster_labels):
            clusters[cluster_label].add_tweet(tweet)
        return clusters

    def get_random_cluster(self):
        number = random()
        integer = int(number * self.number_of_clusters)
        return integer

    def get_cluster_label_from_document(self, document):
        probabilities = [self.cluster_probability_for_document(document, cluster_label)
                         for cluster_label in range(self.number_of_clusters)]
        total = reduce(addition, probabilities, 0)
        probabilities = [p / total for p in probabilities]
        cumulative_probabilities = [0]
        for p in probabilities:
            cumulative_probabilities.append(cumulative_probabilities[-1] + p)
        cumulative_probabilities[-1] = 1
        picked = random()
        for (index, cumulative_probability) in enumerate(cumulative_probabilities):
            if picked < cumulative_probability:
                return index - 1
        return len(probabilities) - 1

    def get_number_of_occurences_of_word_in_cluster(self, word, cluster_label):
        if word in self.number_of_occurences_of_word_per_cluster[cluster_label]:
            return self.number_of_occurences_of_word_per_cluster[cluster_label][word]
        else:
            return 0

    def cluster_probability_for_document(self, document, cluster_label):
        first_term = (self.number_of_documents_per_cluster[cluster_label] + alpha) / (len(self.documents) - 1 +
                                                                                      self.number_of_clusters * alpha)

        second_term = reduce(multiply, [self.get_number_of_occurences_of_word_in_cluster(word, cluster_label) + beta
                                        for word in document], 1)
        third_term = reduce(multiply, [self.number_of_words_per_cluster[cluster_label] + len(self.vocabulary) * beta
                                       + i - 1 for i in range(len(document))], 1)
        return first_term * second_term / third_term
