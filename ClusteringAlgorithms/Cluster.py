from collections import Counter
import ClusteringAlgorithms.string_tools as st


class Cluster:

    def __init__(self):
        self.tweets = []
        self.most_common_words = []
        self.topic = "unknown"
        self.detected_topic = "unknown"
        self.processed = False

    def __str__(self):
        return str(len(self.tweets))

    def add_tweet(self, tweet):
        self.tweets.append(tweet)

    def reset(self):
        self.tweets = []

    def get_most_common_words(self, words_only=False, minimum_proportion=0.0):
        cluster_size = len(self.tweets)
        if len(self.most_common_words) is 0:
            words = []
            for tweet in self.tweets:
                words.extend(st.tokenizer(st.preprocessor(tweet), stem=False))
            self.most_common_words = Counter(words).most_common(15)
        if words_only:
            return [word for (word, count) in self.most_common_words if count / cluster_size > minimum_proportion]
        else:
            return [(word, count) for (word, count) in self.most_common_words
                    if count / cluster_size > minimum_proportion]

    def topic_is_corresponding_to(self, dictionary):
        if dictionary is None:
            return False
        most_common_words = [word for (word, count) in self.most_common_words]
        return dictionary.is_on_topic(most_common_words)

    def detect_topic(self, dictionary):
        is_on_topic = self.topic_is_corresponding_to(dictionary)
        if is_on_topic:
            self.detected_topic = dictionary.name
        else:
            self.detected_topic = "not " + dictionary.name
        return is_on_topic

    def describe(self, number=None, short_description=False):
        if len(self.tweets) is 0:
            return
        if not short_description and number is not None:
            print("Cluster " + str(number))
        most_common_words = self.get_most_common_words()
        print("Most common words : " +
              ", ".join([word + " (" + str(count) + ")" for (word, count) in most_common_words]))
        print("The first tweet is : " + self.tweets[0]['text'])
        if not short_description:
            print("Number of tweets in the cluster : " + str(len(self.tweets)))
            print("The topic is " + self.topic + " and the detected topic is : " + self.detected_topic)
            print()

    def is_similar_to(self, other_cluster):
        min_proportion = 0.5
        min_proportion_overlap = 0.8
        other_most_common_words = other_cluster.get_most_common_words(words_only=True, minimum_proportion=min_proportion)
        most_common_words = self.get_most_common_words(words_only=True, minimum_proportion=min_proportion)
        common_size = min(len(most_common_words), len(other_most_common_words))
        count = 0
        for word in other_most_common_words:
            if word in most_common_words:
                count += 1
        is_similar = count / common_size > min_proportion_overlap
        new_words = []
        if is_similar:
            for word in most_common_words:
                if word not in other_most_common_words:
                    new_words.append(word)
        return is_similar, new_words
