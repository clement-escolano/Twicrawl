from ClusteringAlgorithms.KMeansClustering import KMeansClustering, NUMBER_OF_CLUSTERS
import ClusteringAlgorithms.string_tools as st
from tqdm import tqdm


class IterativeKMeansClustering:

    def __init__(self, preprocessor=st.preprocessor, tokenizer=st.tokenizer):
        self.kmeans = KMeansClustering(preprocessor=preprocessor, tokenizer=tokenizer)
        self.clusters = []

    def cluster(self, tweets, print_progress=False):
        pbar = tqdm(total=len(tweets)) if print_progress else None
        clusters = []
        num_clusters = NUMBER_OF_CLUSTERS
        well_clustered = False
        while not well_clustered:
            new_clusters = 0
            well_clustered = True
            clusters = self.kmeans.cluster(tweets, num_clusters=num_clusters)
            for cluster in clusters:
                if not self.kmeans.is_well_clustered(cluster):
                    new_clusters += 1
            if print_progress:
                pbar.update(1)
            if new_clusters * 50 > num_clusters:
                well_clustered = False
                num_clusters += new_clusters
        if print_progress:
            pbar.close()
        return clusters
