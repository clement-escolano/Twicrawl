from sklearn.externals import joblib


def save(object_to_save, filename):
    joblib.dump(object_to_save, filename)


def load(filename):
    return joblib.load(filename)
