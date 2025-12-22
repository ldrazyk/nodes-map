from umap import UMAP
from hdbscan import HDBSCAN
import numpy as np
from numpy import ndarray
from pprint import pprint

class Mapper:

    def __init__(self):

        pass
        

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

        def get_coordinates_and_clusters(nodes_spec:dict, mapping_spec:dict):

            def get_X_and_X_type(nodes_spec:dict):

                if "embedding" in nodes_spec:
                    X = np.asarray(nodes_spec["embedding"])
                    X_type = "embeddings"
                elif "matrix" in nodes_spec:
                    X = 1 - np.asarray(nodes_spec["matrix"])
                    X_type = "matrix"
                
                return X, X_type
            
            def get_clusters(X:ndarray, X_type:str, mapping_spec:dict):

                if X_type == "matrix":
                    metric = "precomputed"
                else:
                    metric = "euclidean"

                clusterer = HDBSCAN(min_cluster_size=mapping_spec.get("min_cluster", 5),
                                    max_cluster_size=mapping_spec.get("max_cluster", 0),
                                    metric=metric)
                
                clusters = clusterer.fit_predict(X)
                return clusters
            
            def get_coordinates(X:ndarray, X_type:str, mapping_spec:dict):

                if X_type == "matrix":
                    metric = "precomputed"
                else:
                    metric = mapping_spec.get("metric", "euclidean")

                print(metric)

                reducer = UMAP(n_components=2, 
                                n_neighbors=mapping_spec.get("n_neighbors", 15),
                                metric=metric, 
                                random_state=mapping_spec.get("random_state"),
                                min_dist=mapping_spec.get("min_distance", 0.1),
                                spread=mapping_spec.get("spread", 1))
            
                coordinates = reducer.fit_transform(X)
                return coordinates


            X, X_type = get_X_and_X_type(nodes_spec)
            clusters = get_clusters(X, X_type, mapping_spec)
            coordinates = get_coordinates(X, X_type, mapping_spec)

            return coordinates, clusters
            
        
        def create_nodes(coordinates:list[ndarray], clusters:ndarray, nodes_spec:dict[str, list]):

            coordinates = [xy.tolist() for xy in coordinates]
            clusters = clusters.tolist()

            nodes = []

            for n, xy in enumerate(coordinates):

                node = {
                    "x": xy[0],
                    "y": xy[1],
                    "cluster": clusters[n]
                }

                absent_keys = ["matrix", "coo", "feature_scale"]

                if "embedding" in nodes_spec and len(nodes_spec["embedding"][0]) > 32:
                    absent_keys.append("embedding")

                for key, spec_list in nodes_spec.items():
                    if key not in absent_keys:
                        try:
                            node[key] = spec_list[n]
                        except Exception as e:
                            print("Exception type:", type(e).__name__)
                            print("Exception message:", e)
                            print(f"key: {key}, n: {n}")
                
                nodes.append(node)

            return nodes
        
        coordinates, clusters = get_coordinates_and_clusters(nodes_spec=nodes_spec, mapping_spec=mapping_spec)

        def test():

            # print("\ncoordinates:")
            # pprint(coordinates)

            print("\nclusters:")
            pprint(clusters)

        test()

        nodes = create_nodes(coordinates=coordinates, clusters=clusters, nodes_spec=nodes_spec)

        return nodes