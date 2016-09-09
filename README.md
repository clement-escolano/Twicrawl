# Installation of the program

## Libraries

The program is written in python and requires some modules to work as intended.
These libraries should be installed : `nltk`, `pymongo`, `tweepy`, `tqdm`, `sklearn.

To work properly, the `nltk` package needs to download the data that will be used in the project.
It can be done by launching the `ntlk` download manager via the command line : `nltk.download()`.
The data required for this program are the `stopwords`, the `punkt` and the `snowball_data` in the
 *All packages* tab.

## Twitter API tokerns

To work properly, you must get the different tokens from Twitter to access the Twitter API.
Everything can be done through the Twitter website here :
[Lien pour s'enregistrer sur Twitter](https://apps.twitter.com/app/new)

# Code structure

## Crawler

The `Crawler.py` is the main script for crawling data from Twitter.
The keywords used for crawling are described in `keywords.py` and
can be modified. Currently, the structure of the keywords is divided to
have primary keywords useful for the streaming API and the other keywords
that will help determine if a cluster is security-related or not, and detect
which software and the type of attack for every vulnerability.

The crawler takes as parameter a MongoDB database if the tweets
are to be stored into a MongoDB server, or a filename if the
tweets are to be stored into a file. It is also taking keywords,
and eventually a verbose parameter.

## Clustering algorithms

The `ClusteringAlgorithms` folder has the different algorithms
for clustering the tweets. It contains the indexer which is the main
interface to the clustering algorithms. The main parameters of the K-means
clustering algorithm are inside the `KMeansClustering.py` file.
Similarly, the parameters for the GSDMM algorithm is in the `GSDMMClustering.py` file.

To launch a clustering process, the `main_script.py` script gathers every step.
The database is informed but loading from a file is possible by setting the
variable `from_db` to `False`. The different filenames are here to load or save
the tweets, the clusters and the dictionary.

It is also possible to show some statistics with the function
`show_statistics_of_clusters` from the `statistics.py` file.

## Classification algorithms

The `ClassificationAlgorithms` folder has the different algorithms for
classifying the tweets as well as some scripts to create it.

In order to create a `Dictionary` with keywords, one can use the `create_dictionary.py`
 script. The list of URLs can be modified as well as the tags. The tags must be in
 hierarchical order an no tag can be missed.

To train the dictionary, the script `teach_dictionary.py` loads some clusters and
then ask for human input. The answer must start with `y` if the described cluster
is about the topic, everything else (even nothing) otherwise. The training can be
stopped by entering `exit`. The `blacklist` variable is a list of words which are
automatically classified as off topic for the clusters. The parameter
`skip_already_process` of the function `ask_user_input` is useful if the training
is done in several times. The parameter `minimum_size` skips clusters with a small size.

The elements of the confusion matrix derived from the clusters and the topic can
be displayed with the function `show_statistics_on_topic` in the file `statistics.py`.

Everything can be done at once with the `classifying_script.py` script. If the user
input is required (no previous training or limited training at the beginning)
the variable `ask_user` should be set to `True`.

## Overall server

Every part of the program is combined into a single script : `server.py`.
The parameters for the database, the keywords used, the interval between every
clustering step, and the window of time for clustering. The detected vulnerabilities
are displayed automatically but it should appear for the first time after two hours
as there is not enough tweets at the beginning. They are also saved into a file
specified in the file.