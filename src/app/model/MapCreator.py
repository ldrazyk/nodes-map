import umap
import numpy as np
from numpy import ndarray

class MapCreator:

    def __init__(self, random_state:int=22):

        self.default_random_state = random_state
        

        pass

    def create_map(self, ids:list, embeddings:list[ndarray|list], labels:list[str]=False, images:list[str]=False, clusters:list[int|str]=False, props:dict[str, list]=False,
                   metric:str="cosine", random_state:int=False):

        def get_map_coordinates(embeddings:list[ndarray|list], random_state:int):

            if not random_state:
                random_state = self.default_random_state

            if not isinstance(embeddings[0], ndarray):
                embeddings = [np.array(embedding) for embedding in embeddings]

            reducer = umap.UMAP(n_components=2, metric=metric, random_state=random_state)
            map_coordinates = reducer.fit_transform(embeddings)
            return map_coordinates
        
        def create_nodes(map_coordinates:list[ndarray]):

            nodes = []

            for n in enumerate(ids):

                node = {
                    "id": ids[n],
                    "x": map_coordinates[n][0],
                    "y": map_coordinates[n][1],
                }

                if labels:
                    node["label"] = labels[n]
                if images:
                    node["image"] = images[n]
                if clusters:
                    node["cluster"] = clusters[n]
                if props:
                    for key, prop_list in props.items():
                        node[key] = prop_list[n]

            return nodes



        map_coordinates = get_map_coordinates(embeddings, random_state=random_state)
        nodes = create_nodes(map_coordinates)
        return nodes