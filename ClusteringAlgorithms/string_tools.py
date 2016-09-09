import nltk
import re


def tokenizer(text, stem=True):
    stemmer = nltk.stem.snowball.SnowballStemmer('english')
    stopwords = nltk.corpus.stopwords.words('english')
    tokens = nltk.word_tokenize(text)
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-z]', token) and token not in stopwords:
            filtered_tokens.append(stemmer.stem(token) if stem else token)
    return filtered_tokens


def preprocessor(tweet):
    text = tweet['text'].lower()
    if text[0:3] == "rt ":
        text = text[3:]
    text = text.replace('\/', '/')
    text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = text.replace('\'', '')
    text = text.replace('\n', ' ')
    return text


def unique_words(words):
    return list(set(words))


def new_extended_list(*args):
    new_list = []
    for arg in args:
        new_list.extend(arg)
    return new_list


def check_intersection_non_empty(words, other_words):
    for word in words:
        if word in other_words:
            return True
    return False


def get_intersection(words, other_words):
    intersection = []
    for word in words:
        if word in other_words:
            intersection.append(word)
    return intersection


def get_extra_words(words, keywords):
    extra_words = []
    for word in words:
        if not word in keywords:
            extra_words.append(word)
    return extra_words
