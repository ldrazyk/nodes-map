import numpy as np
from numpy import ndarray
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA


def combine_embeddings_models(embeddings_models:list[list[list|ndarray]], input_reduction_size:int=False, final_size:int=False, 
                              normalize_input:bool=True, normalize_output:bool=True, to_lists:bool=False):


    if isinstance(embeddings_models[0][0], (list, tuple)):
        embeddings_models = [[np.array(embedding) for embedding in model] for model in embeddings_models]
    
    if normalize_input:
        embeddings_models = [normalize(model) for model in embeddings_models]

    if input_reduction_size:
        embeddings_models = [PCA(n_components=input_reduction_size, random_state=33).fit_transform(model) for model in embeddings_models]

    combined = np.concatenate(embeddings_models, axis=1)
    
    if final_size:
        combined = PCA(n_components=final_size, whiten=True, random_state=33).fit_transform(combined)
    
    if normalize_output:
        combined = normalize(combined)
    
    if to_lists:
        combined = [embedding.tolist() for embedding in combined]

    return combined