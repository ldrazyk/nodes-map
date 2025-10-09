import numpy as np
from numpy import ndarray
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.decomposition import PCA


class Preprocessor:

    def __init__(self, random_state:int=33):
        
        self.random_state = random_state

    def __embeddings_to_list(self, embeddings:list[ndarray]):

        return [embedding.tolist() for embedding in embeddings]
    
    def __embeddings_to_ndarray(self, embeddings:list[list|ndarray]):

        if isinstance(embeddings[0], (list, tuple)):
            return np.array(embeddings)
        else:
            return embeddings

    def combine_embeddings(self, embeddings_models:list[list[list|ndarray]], input_reduction_size:int=False, final_size:int=False, 
                                normalize_input:bool=True, normalize_output:bool=True, to_lists:bool=False):


        if isinstance(embeddings_models[0][0], (list, tuple)):
            embeddings_models = np.array(embeddings_models)
            # embeddings_models = [[np.array(embedding) for embedding in model] for model in embeddings_models]
        
        if normalize_input:
            embeddings_models = [normalize(model) for model in embeddings_models]

        if input_reduction_size:
            embeddings_models = [PCA(n_components=input_reduction_size, random_state=self.random_state).fit_transform(model) for model in embeddings_models]

        combined = np.concatenate(embeddings_models, axis=1)
        
        if final_size:
            combined = PCA(n_components=final_size, whiten=True, random_state=self.random_state).fit_transform(combined)
        
        if normalize_output:
            combined = normalize(combined)
        
        if to_lists:
            combined = self.__embeddings_to_list(combined)

        return combined
    

    def normalize_embeddings(self, embeddings:list[list|ndarray], to_lists:bool=False):

        embeddings = self.__embeddings_to_ndarray(embeddings)

        embeddings = normalize(embeddings)

        if to_lists:
            embeddings = self.__embeddings_to_list(embeddings)
        
        return embeddings
    

    def reduce_embeddings(self, embeddings:list[list|ndarray], reduction_size:int, normalize_input:bool=True, normalize_output:bool=True, to_lists:bool=False):

        embeddings = self.__embeddings_to_ndarray(embeddings)

        if normalize_input:
            embeddings = normalize(embeddings)
        
        embeddings = PCA(n_components=reduction_size, random_state=self.random_state).fit_transform(embeddings)

        if normalize_output:
            embeddings = normalize(embeddings)

        if to_lists:
            embeddings = self.__embeddings_to_list(embeddings)

        return embeddings

    def scale_features(self, embeddings:list[list|ndarray], to_lists:bool=False):

        embeddings = self.__embeddings_to_ndarray(embeddings)

        scaler = StandardScaler()
        embeddings = scaler.fit_transform(embeddings)

        if to_lists:
            embeddings = self.__embeddings_to_list(embeddings)

        return embeddings