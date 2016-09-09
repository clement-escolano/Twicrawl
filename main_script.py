from ClusteringAlgorithms.Indexer import Indexer
from Mongo import Mongo
from ClassificationAlgorithms.Dictionary import Dictionary
from ClusteringAlgorithms.RecursiveKMeansClustering import RecursiveKMeansClustering
from statistics import show_statistics_of_clusters as statistics

# Main script
# It first loads tweets from either a Mongo database or a file
# Then create the clusters with a given clustering method
# Optionally, it can load a dictionary from a file and classify the clusters
# Finally it describes the clusters, show some statistics and save the clusters and the dictionary

use_dictionary = False
from_db = True

if from_db:  # load indexer with tweets via db
    indexer = Indexer(Mongo(name="kw2"))
else:  # load indexer with tweets from file
    indexer = Indexer(filename="data/tweets_extensive_db.pkl")

# create clustering method
clustering_method = RecursiveKMeansClustering()

# launch clustering process
indexer.create_clusters(clustering_method, print_progress=True)

# create raw dictionary from file
dico = Dictionary('computing')
if use_dictionary:
    dico.restore_dictionary(filename="dictionary.pkl")

# Classify from dictionary
if use_dictionary:
    indexer.classify(dico)

# describe clusters and statistics
indexer.describe_clusters()
statistics(indexer.clusters)

# save clusters and dictionary
indexer.save("data/clusters_night_8_reckmeans.pkl")
if use_dictionary:
    dico.save_dictionary(filename="new_dictionary.pkl")
