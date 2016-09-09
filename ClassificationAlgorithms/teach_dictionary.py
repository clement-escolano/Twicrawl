from ClassificationAlgorithms.NaiveBayesDictionary import NaiveBayesDictionary as Dictionary
from FileSave import load, save
import ClusteringAlgorithms.string_tools as st

topic = "computing"
blacklist = ['laptop', 'smartphone', 'samsung']


def ask_user_input(dictionary, clusters, minimum_size=1, skip_already_processed=False):
    topic = dictionary.name
    for index, cluster in enumerate(clusters):
        if len(cluster.tweets) < minimum_size or (skip_already_processed and getattr(cluster, 'processed', False)):
            continue
        if st.check_intersection_non_empty(blacklist, cluster.get_most_common_words(words_only=True)):
            cluster.processed = True
            cluster.topic = "not " + topic
            dictionary.update_dictionary(cluster.get_most_common_words(words_only=True), False)
            continue
        print("Cluster : " + str(index) + " / " + str(len(clusters)))
        cluster.describe(short_description=True)
        answer = input("Cluster of tweets about " + topic + " ? ").strip()
        print()
        if len(answer) is 0:
            cluster.processed = True
            about_computing = False
        elif answer.lower()[0] == 'y':
            about_computing = True
            cluster.topic = topic
            cluster.processed = True
        elif answer.lower()[0] == 'e':
            break
        else:
            cluster.processed = True
            about_computing = False
            cluster.topic = "not " + topic
        dictionary.update_dictionary(cluster.get_most_common_words(words_only=True), about_computing)


def process_clusters(dictionary, clusters):
    for cluster in clusters:
        if getattr(cluster, 'processed', False):
            dictionary.update_dictionary(cluster.get_most_common_words(words_only=True),
                                         cluster.topic == dictionary.name)


if __name__ == '__main__':
    clusters = load("data/clusters_night_8_rec_kmeans_classified.pkl")
    dico = Dictionary("computing")
    # dico.restore_dictionary(filename="data/naive_bayes_dictionary.pkl")

    # ask_user_input(dico, clusters, minimum_size=1, skip_already_processed=False)
    process_clusters(dico, clusters)

    save(clusters, filename="data/clusters_test_db_recursive_kmeans_with_topic.pkl")
    dico.save_dictionary(filename="data/dictionary_trained_1.pkl")
