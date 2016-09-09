from ClassificationAlgorithms.Dictionary import Dictionary as Dictionary
from ClusteringAlgorithms.Indexer import Indexer
from FileSave import load
from statistics import show_statistics_on_topic
from ClassificationAlgorithms.teach_dictionary import ask_user_input, process_clusters


# Classifying script
# First, the dictionary is created
# Then, the indexer is created and loads previous clusters
# Optionally, the dictionary is trained
# Clusters are classified
# Finally, statistics are showed and dictionary and clusters are caved

topic = "computing"
ask_user = False
train_only = False

# Create indexer and loads clusters
indexer = Indexer()
indexer.clusters = load("data/clusters_night_8_rec_kmeans_classified.pkl")

# Create dictionary from a file
dico = Dictionary(topic)
if train_only:
    process_clusters(dico, indexer.clusters)
    indexer.classify(dico)
    show_statistics_on_topic(indexer.clusters, topic)
    dico.save_dictionary(filename="data/dictionary.pkl")
    exit()
if not ask_user:  # restore the dictionary if no input
    dico.restore_dictionary(filename="data/raw_dictionary.pkl")
else:  # train the dictionary if input wanted
    ask_user_input(dico, indexer.clusters, skip_already_processed=True)

# Classify the data
indexer.classify(dico)
# Show statistics
show_statistics_on_topic(indexer.clusters, topic)

# Save dictionary and clusters
# indexer.save("data/clusters_night_8_rec_kmeans_classified.pkl")
if ask_user:
    dico.save_dictionary(filename="data/naive_bayes_dictionary.pkl")
