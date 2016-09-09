import threading
from Crawler import Crawler
from Mongo import Mongo
from ClusteringAlgorithms.Indexer import Indexer
from ClassificationAlgorithms.Dictionary import Dictionary
from FileSave import save
from ClusteringAlgorithms.RecursiveKMeansClustering import RecursiveKMeansClustering
import keywords as kw
from ClusteringAlgorithms.string_tools import get_intersection, get_extra_words

keywords = kw.primary_keywords
db_name = "prod1"
db_address = "mongodb://localhost:27018"
indexing_interval = 2 * 3600  # seconds
window_range = 24  # hours


db = Mongo(address=db_address, name=db_name)

crawler = Crawler(db, keywords=keywords, verbose=False)

indexer = Indexer(db=db, hour_range=window_range)
clustering_method = RecursiveKMeansClustering()

dico = Dictionary('computing')
dico.restore_dictionary(filename="data/raw_dictionary.pkl")

detected_vulnerabilities = []


def process_cluster(cluster, verbose=False):
    is_new_vulnerability = True
    for stored_cluster in detected_vulnerabilities:
        is_similar, new_words = cluster.is_similar_to(stored_cluster)
        if is_similar:
            is_new_vulnerability = False
            print("New keywords for vulnerability : " + str(new_words))
            print("Previous vulnerability :")
            stored_cluster.describe()
    if is_new_vulnerability:
        detected_vulnerabilities.append(cluster)
        if verbose:
            print("New potential vulnerability detected")
            words = cluster.get_most_common_words(words_only=True)
            name = get_intersection(words, kw.program_names)
            attack = get_intersection(words, kw.attack_types)
            extra = get_extra_words(words, kw.all_keywords)
            if len(name) > 0:
                print("The affected software : " + name)
            if len(attack) > 0:
                print("The type of attack : " + attack)
            if len(extra) > 0:
                print("Other information : " + extra)
            cluster.describe()


def detect_vulnerabilities():
    print("Indexing recent tweets")
    indexer.create_clusters(clustering_method)
    indexer.classify(dico)
    clusters = indexer.get_relevant_clusters('computing')
    for cluster in clusters:
        process_cluster(cluster)
    print("End of indexing. Next step in " + str(indexing_interval) + " seconds")
    threading.Timer(indexing_interval, detected_vulnerabilities)


threading.Thread(target=crawler.run).start()

# noinspection PyBroadException
try:
    detect_vulnerabilities()
except Exception:
    print("Process interrupted. Saving vulnerabilities...")
    save(detected_vulnerabilities, "data/detected_vulnerabilities.pkl")
    print("End of the program")
    exit()
