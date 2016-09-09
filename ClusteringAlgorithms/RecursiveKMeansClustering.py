from ClusteringAlgorithms.KMeansClustering import KMeansClustering
import ClusteringAlgorithms.string_tools as st
from tqdm import tqdm


class RecursiveKMeansClustering:

    def __init__(self, preprocessor=st.preprocessor, tokenizer=st.tokenizer):
        self.kmeans = KMeansClustering(preprocessor=preprocessor, tokenizer=tokenizer)
        self.clusters = []

    def cluster(self, tweets, print_progress=False):
        pbar = tqdm(total=len(tweets)) if print_progress else None
        clusters_temp = self.kmeans.cluster(tweets)
        clusters = []
        while len(clusters_temp) is not 0:
            next_step_of_clusters = []
            for cluster_index, cluster in enumerate(clusters_temp):
                if not self.kmeans.is_well_clustered(cluster):
                    try:
                        new_clusters = self.kmeans.cluster(cluster.tweets)
                        next_step_of_clusters.extend(new_clusters)
                    except ValueError:
                        if print_progress:
                            pbar.update(len(cluster.tweets))
                else:
                    if len(cluster.tweets) > 0:
                        clusters.append(cluster)
                        if print_progress:
                            pbar.update(len(cluster.tweets))
            clusters_temp = next_step_of_clusters
        if print_progress:
            pbar.close()
        return clusters
