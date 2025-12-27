from src.app.model import Mapper, Preprocessor
import numpy as np
import pprint

mapper = Mapper(random_state=11, min_cluster_size=2, max_cluster_size=0, n_neighbors=5, metric="cosine", min_dist=0.5, spread=2.0)
processor = Preprocessor()

def test_Mapper():

    def test_create_map():

        def test(nodes_spec, umap_spec, embeddings=False, matrix=False):

            if embeddings:
                embeddings = processor.normalize_embeddings(embeddings=embeddings)
                pprint.pprint(embeddings)
                nodes_spec["embedding"] = embeddings
            else:
                nodes_spec["matrix"] = matrix

            map = mapper.create_map(nodes_spec=nodes_spec, umap_spec=umap_spec)
            pprint.pprint(map)

        def test_emb_countries():

            countries_embeddings = [
                [38.5, 0.313, 123.3, 11.1],
                [46.7, 0.604, 77.4, 5.4],
                [82.4, 0.357, 230.9, 27.6],
                [127.4, 0.377, 337.4, 28.2],
                [142.9, 17.1, 8.4, 8.9],
                [298.4, 9.63, 31.0, 37.8],
                [1314, 9.60, 136.9, 5.0],
                [0.28, 0.0, 649.5, 15.7],
                [0.29, 0.023, 12.5, 4.9],
                [0.91, 0.018, 49.6, 5.8],
                [1095, 3.29, 333.2, 2.9],
                [107.4, 1.97, 54.4, 9.0],
            ]

            countries_spec = {
                "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                "label": [
                    "Poland",
                    "Ukraine",
                    "Germany",
                    "Japan",
                    "Russia",
                    "USA",
                    "China",
                    "Barbados",
                    "Belize",
                    "Fiji",
                    "India",
                    "Mexico",
                ],
                "image": [
                    "POL.png",
                    "UKR.png",
                    "GER.png",
                    "JPN.png",
                    "RUS.png",
                    "USA.png",
                    "CHN.png",
                    "BRB.png",
                    "BLZ.png",
                    "FIJ.png",
                    "IND.png",
                    "MEX.png",
                ]
            }

            umap_spec = {
                # "metric": "euclidean",
                # "n_neighbors": 2,
                # "random_state": 56
            }

            test(nodes_spec=countries_spec, umap_spec=umap_spec, embeddings=countries_embeddings)

        def test_matrix_animals():

            animals_spec = {
                "id": [1, 2, 3, 4, 5, 6, 7, 8],
                "label": [
                    "Ant",
                    "Spider",
                    "Fish",
                    "Frog",
                    "Snake",
                    "Bird",
                    "Horse",
                    "Whale"
                ],
                "size": [
                    0.01,
                    0.05,
                    0.3,
                    0.2,
                    0.3,
                    0.2,
                    0.6,
                    1.0
                ]
            }

            animals_matrix = [
                [1, 0.8, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
                [0.8, 1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
                [0.2, 0.2, 1, 0.5, 0.5, 0.5, 0.5, 0.5],
                [0.2, 0.2, 0.5, 1, 0.7, 0.7, 0.7, 0.7],
                [0.2, 0.2, 0.5, 0.7, 1, 0.9, 0.8, 0.8],
                [0.2, 0.2, 0.5, 0.7, 0.9, 1, 0.8, 0.8],
                [0.2, 0.2, 0.5, 0.7, 0.8, 0.8, 1, 0.9],
                [0.2, 0.2, 0.5, 0.7, 0.8, 0.8, 0.9, 1],
            ]

            umap_spec = {
                # "n_neighbors": 2,
                # "random_state": 56
            }

            test(nodes_spec=animals_spec, umap_spec=umap_spec, matrix=animals_matrix)

        test_emb_countries()
        test_matrix_animals()

    test_create_map()