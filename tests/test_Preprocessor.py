from src.app.model import Preprocessor
from pprint import pprint

preprocessor = Preprocessor()

def test_Preprocessor():

    countries_emb = [
        [38, 0.31, 125, 0.98],
        [84, 0.35, 241, 4.74],
        [144, 16.38, 9, 2.08],
        [347, 9.15, 38, 30.51],
        [1416, 9.39, 151, 19.23],
        [1464, 2.97, 492, 4.19]
    ]

    def test_scale_and_normalise():

        def test(emb):

            emb_normalized = preprocessor.normalize_embeddings(emb)
            emb_scaled = preprocessor.scale_features(emb)
            emb_scaled_normalized = preprocessor.normalize_embeddings(emb_scaled)

            print("embeddings:")
            pprint(emb)
            print("normalized:")
            pprint(emb_normalized)
            print("scaled:")
            pprint(emb_scaled)
            print("scaled & normalized:")
            pprint(emb_scaled_normalized)

        test(countries_emb)

    test_scale_and_normalise()
