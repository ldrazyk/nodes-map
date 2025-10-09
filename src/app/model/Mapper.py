from umap import UMAP
from hdbscan import HDBSCAN
import numpy as np
from numpy import ndarray
from pprint import pprint

class Mapper:

    def __init__(self, random_state:int=22, min_cluster_size:int=2, max_cluster_size:int=0, metric:str="euclidean", n_neighbors:int=5, 
                 min_dist:float=0.1, spread:float=1):

        self.default_random_state = random_state
        self.default_min_cluster_size = min_cluster_size
        self.default_max_cluster_size = max_cluster_size
        self.default_metric = metric
        self.default_n_neighbors = n_neighbors
        self.default_min_dist = min_dist
        self.default_spread = spread
        

    def create_map(self, nodes_spec:dict, mapping_spec:dict={}):
        """Creates nodes (dict) map (list).  
        `nodes_spec` must have: `id` and `embedding` or `matrix`, and can have `label`, `image`, `size`, and any other.  
        If `matrix` it should be similarity, not distance.  
        Nodes will have: `x`, `y`, `cluster`, and all props in `nodes_spec` except `embedding` and `matrix`.  

        Args:
            nodes_spec (dict): {`embedding`/`matrix`, id, label, image, cluster, ...}
            mapping_spec (dict): {n_neighbors, metric, random_state}
        
        Returns:
            nodes (list[dict]): Nodes {id, x, y, (label), (cluster), ... }
        """

        def get_coordinates_and_clusters_from_embeddings(embeddings:list[ndarray|list], mapping_spec:dict):

            if not isinstance(embeddings[0], ndarray):
                embeddings = [np.array(embedding) for embedding in embeddings]

            metric = mapping_spec.get("metric", self.default_metric)

            clusterer = HDBSCAN(min_cluster_size=self.default_min_cluster_size,
                                max_cluster_size=self.default_max_cluster_size)
            clusters = clusterer.fit_predict(embeddings)

            reducer = UMAP(n_components=2, 
                            n_neighbors=mapping_spec.get("n_neighbors", self.default_n_neighbors),
                            metric=metric, 
                            random_state=mapping_spec.get("random_state", self.default_random_state))
            
            map_coordinates = reducer.fit_transform(embeddings)
            return map_coordinates, clusters
        
        def get_coordinates_and_clusters_from_matrix(matrix:list[list]|ndarray, mapping_spec:dict):

            if not isinstance(matrix, ndarray):
                matrix = np.array(matrix)

            metric = "precomputed"

            distance_matrix = 1 - matrix

            clusterer = HDBSCAN(min_cluster_size=self.default_min_cluster_size,
                                max_cluster_size=self.default_max_cluster_size,
                                metric=metric)
            clusters = clusterer.fit_predict(distance_matrix)

            reducer = UMAP(n_components=2, 
                            n_neighbors=mapping_spec.get("n_neighbors", self.default_n_neighbors),
                            metric=metric, 
                            random_state=mapping_spec.get("random_state", self.default_random_state),
                            min_dist=self.default_min_dist,
                            spread=self.default_spread)
            
            map_coordinates = reducer.fit_transform(distance_matrix)

            return map_coordinates, clusters
        
        def create_nodes(map_coordinates:list[ndarray], clusters:ndarray, nodes_spec:dict[str, list]):

            map_coordinates = [xy.tolist() for xy in map_coordinates]
            clusters = clusters.tolist()

            nodes = []

            for n, xy in enumerate(map_coordinates):

                node = {
                    "x": xy[0],
                    "y": xy[1],
                    "cluster": clusters[n]
                }

                for key, spec_list in nodes_spec.items():
                    if key not in ("embedding", "matrix"):
                        node[key] = spec_list[n]
                
                nodes.append(node)

            return nodes

        
        if "embedding" in nodes_spec:
            map_coordinates, clusters = get_coordinates_and_clusters_from_embeddings(embeddings=nodes_spec["embedding"], mapping_spec=mapping_spec)
        else:
            map_coordinates, clusters = get_coordinates_and_clusters_from_matrix(matrix=nodes_spec["matrix"], mapping_spec=mapping_spec)

        print("\nmap_coordinates:")
        pprint(map_coordinates)

        print("\nclusters:")
        pprint(clusters)

        nodes = create_nodes(map_coordinates=map_coordinates, clusters=clusters, nodes_spec=nodes_spec)
        return nodes