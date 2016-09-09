from FileSave import save, load
# noinspection PyUnresolvedReferences
from math import log

LAPLACE_SMOOTHING = 1


class NaiveBayesDictionary:
    def __init__(self, name="some topic"):
        self.name = name
        self.on_topic_related_words = dict()
        self.off_topic_related_words = dict()
        self.on_topic_related_count = LAPLACE_SMOOTHING
        self.off_topic_related_count = LAPLACE_SMOOTHING

    def on_topic_train(self, words):
        self.on_topic_related_count += 1
        for word in words:
            if word in self.on_topic_related_words.keys():
                self.on_topic_related_words[word] += 1
            else:
                self.on_topic_related_words[word] = 1 + LAPLACE_SMOOTHING
                self.off_topic_related_words[word] = LAPLACE_SMOOTHING

    def off_topic_train(self, words):
        self.off_topic_related_count += 1
        for word in words:
            if word in self.off_topic_related_words.keys():
                self.off_topic_related_words[word] += 1
            else:
                self.on_topic_related_words[word] = LAPLACE_SMOOTHING
                self.off_topic_related_words[word] = 1 + LAPLACE_SMOOTHING

    def update_dictionary(self, words, on_topic):
        if on_topic:
            self.on_topic_train(words)
        else:
            self.off_topic_train(words)

    def get_on_topic_probability(self, word):
        if word in self.on_topic_related_words.keys():
            total = self.on_topic_related_words[word] + self.off_topic_related_words[word]
            probability = self.on_topic_related_words[word] / total
            return probability
        else:  # if there is no information about the word
            return 0.5

    def is_on_topic(self, words):
        on_topic_score = 1
        off_topic_score = 1
        for word in words:
            probability = self.get_on_topic_probability(word)
            on_topic_score += log(probability)
            off_topic_score += log(1 - probability)
        return on_topic_score > off_topic_score

    def save_dictionary(self, filename):
        object_to_save = [self.on_topic_related_words, self.on_topic_related_count,
                          self.off_topic_related_words, self.off_topic_related_count]
        save(object_to_save, filename)

    def restore_dictionary(self, filename):
        self.on_topic_related_words, self.on_topic_related_count, \
        self.off_topic_related_words, self.off_topic_related_count = load(filename)
