def show_statistics_of_clusters(clusters):
    cluster_with_size_1 = 0
    cluster_with_size_2 = 0
    cluster_about_computing = 0
    big_clusters_about_computing = 0
    number_of_clusters = len(clusters)
    number_of_tweets = 0
    number_of_tweets_about_computing = 0
    number_of_processed_clusters = 0

    for cluster in clusters:
        number_of_tweets += len(cluster.tweets)
        try:
            if cluster.processed:
                number_of_processed_clusters += 1
        except AttributeError:
            pass
        if len(cluster.tweets) is 1:
            cluster_with_size_1 += 1
        if len(cluster.tweets) is 2:
            cluster_with_size_2 += 1
        if cluster.topic == "computing":
            cluster_about_computing += 1
            number_of_tweets_about_computing += len(cluster.tweets)
            if len(cluster.tweets) > 2:
                big_clusters_about_computing += 1

    for cluster in clusters:
        if cluster.topic == "computing":
            cluster.describe()

    print("Number of cluster with only one tweet " + str(cluster_with_size_1))
    print("Number of cluster with only two tweets " + str(cluster_with_size_2))
    print("Clusters about computing : " + str(cluster_about_computing) +
          " (" + str(number_of_tweets_about_computing) + ")")
    print("Among which " + str(cluster_about_computing) + " of clusters with more than 3 tweets")
    print("Number of clusters " + str(number_of_clusters) + " (" + str(number_of_tweets) + ")")
    print("Number of processed cluster " + str(number_of_processed_clusters))


def show_statistics_on_topic(clusters, topic):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for cluster in clusters:
        if cluster.detected_topic == topic:
            if cluster.topic == topic:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if cluster.topic == topic:
                false_negative += 1
            else:
                true_negative += 1
    print("There are " + str(true_positive) + " true positives.")
    print("There are " + str(true_negative) + " true negatives.")
    print("There are " + str(false_positive) + " false positives.")
    print("There are " + str(false_negative) + " false negatives.")
