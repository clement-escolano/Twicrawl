from Mongo import Mongo
# noinspection PyUnresolvedReferences
from math import log
import FileSave


MAX_SCORE = 5.0
ON_TOPIC_THRESHOLD = 3


class Dictionary:

    def __init__(self, name="unknown"):
        self.dictionary = dict()
        self.name = name

    def register_word(self, word, score=MAX_SCORE):
        self.dictionary[word] = score

    def register_words(self, words, score=MAX_SCORE):
        for word in words:
            self.register_word(word, score=score)

    def add_word(self, word, diff=0.5):
        if word in self.dictionary.keys():
            self.dictionary[word] += diff
        else:
            self.register_word(word, score=diff)

    def exclude_word(self, word):
        self.add_word(word, diff=-0.2)

    def save_dictionary(self, db=Mongo(), filename=None):
        if filename is None:
            for word in self.dictionary.keys():
                score = self.dictionary[word]
                db.save_word(word, score)
        else:
            FileSave.save(self.dictionary, filename)

    def restore_dictionary(self, db=Mongo(), filename=None):
        if filename is None:
            words = db.get_words()
            for word in words:
                self.register_word(word['word'], score=word['score'])
        else:
            self.dictionary = FileSave.load(filename)

    def get_score_per_word(self, word):
        if word in self.dictionary:
            raw_score = self.dictionary[word]
            if raw_score > 0:
                return log(1 + min(MAX_SCORE, raw_score))
            if raw_score < 0:
                return -log(1 + min(MAX_SCORE, -raw_score))
        return 0

    def get_score(self, words):
        score = 0
        for word in words:
            score += self.get_score_per_word(word)
        return score

    def is_on_topic(self, words):
        score = self.get_score(words)
        return score > ON_TOPIC_THRESHOLD

    def update_dictionary(self, words, is_on_topic):
        if is_on_topic:
            for word in words:
                self.add_word(word)
            return True
        else:
            for word in words:
                self.exclude_word(word)
            return False

    def __str__(self):
        return str(self.dictionary)
