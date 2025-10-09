from myfiles import Storage, FilesManager, Repository
from mytext import TextEditor
from .Mapper import Mapper
from .Preprocessor import Preprocessor
from .nodes import NodesSpecApi
import requests
from requests import Response
from pprint import pprint

class Application:

    def __init__(self):

        self.storage = Storage()
        self.text_editor = TextEditor()
        self.files_manager = FilesManager(self.text_editor)

        self.mapper = Mapper()
        self.preprocessor = Preprocessor()
        self.nodes_spec_api = NodesSpecApi()
        self.maps_repository = Repository(dir="data/maps", 
                                          dir_id="maps_repo", 
                                          storage=self.storage, 
                                          files_manager=self.files_manager, 
                                          text_editor=self.text_editor)

    def __get_data_from_response(self, response:Response):

        if response.status_code == 200:
            try:
                data = response.json()
                print("Got json data from response.")
                return data
            except ValueError:
                print("Response content is not valid JSON")
        else:
            print(f"Request failed with status code {response.status_code}")

    def create_map(self, spec:dict):
        """Creates map from api url and stores in repository.

        Args:
            spec (dict): { map_name, api, preprocess, mapping }
        
        Returns:
            id (str): Maps id
        """

        def get_nodes_spec(api_spec:dict):
            
            params = {}

            id=api_spec.get("id")
            if id:
                params["id"] = id
                
            response = requests.get(url=api_spec["url"], params=params)
            pprint(response)
            return self.__get_data_from_response(response)
        
        def preprocess(nodes_spec:dict, preprocess_spec:dict):

            def scale_features(nodes_spec:dict):
                
                nodes_spec["embedding"] = self.preprocessor.scale_features(nodes_spec["embedding"])

            def normalize_embeddings(nodes_spec:dict):

                nodes_spec["embedding"] = self.preprocessor.normalize_embeddings(nodes_spec["embedding"])
            
            def reduce_embeddings(nodes_spec:dict, preprocess_spec:dict):

                nodes_spec["embedding"] = self.preprocessor.reduce_embeddings(embeddings=nodes_spec["embedding"],
                                                                                reduction_size=preprocess_spec["reduction_size"],
                                                                                normalize_input=preprocess_spec.get("normalize_reduce_input"),
                                                                                normalize_output=preprocess_spec.get("normalize_reduce_output"))

            def combine_embeddings(nodes_spec:dict, preprocess_spec:dict):

                nodes_spec["embedding"] = self.preprocessor.combine_embeddings(embeddings_models=nodes_spec["embedding"],
                                                                                input_reduction_size=preprocess_spec["input_reduction_size"],
                                                                                final_size=preprocess_spec["output_reduction_size"],
                                                                                normalize_input=preprocess_spec.get("normalize_combine_input"),
                                                                                normalize_output=preprocess_spec.get("normalize_combine_output"))
            
            if "embedding" in nodes_spec:

                print("Preprocessing embeddings...")

                if "scale_features" in preprocess_spec:
                    scale_features(nodes_spec)

                if "combine" in preprocess_spec:
                    combine_embeddings(nodes_spec, preprocess_spec)
                elif "reduce" in preprocess_spec:
                    reduce_embeddings(nodes_spec, preprocess_spec)
                elif "normalize" in preprocess_spec or "scale_features" in preprocess_spec:
                    normalize_embeddings(nodes_spec)

        def create(nodes_spec:dict, mapping_spec:dict):

            print("Creating nodes...")

            return self.mapper.create_map(nodes_spec=nodes_spec, mapping_spec=mapping_spec)

        
        def store_map(name:str, data:dict):

            return self.maps_repository.store_item(name=name, ext="json", data=data)


        print("Creating map...")

        api_spec = spec["api"]
        preprocess_spec = spec["preprocess"]
        mapping_spec = spec["mapping"]
        map_name = spec["map_name"]

        nodes_spec = get_nodes_spec(api_spec)
        
        if nodes_spec:

            preprocess(nodes_spec, preprocess_spec)
            nodes = create(nodes_spec, mapping_spec)
            id = store_map(map_name, {"nodes": nodes, "spec": spec})
            if id:
                print(f"Map with id: '{id}' stored.")
            return id
        
        else:
            print(f"Could not find nodes_spec in url: '{api_spec["url"]}'")
    
    def get_map_ids(self):

        return self.maps_repository.get_item_ids()

    def get_map(self, id:str):

        return self.maps_repository.get_item(id)

    def get_map_example(self, id:str):
        # test

        examples = {
            "countries": [
                {
                    'cluster': 1,
                    'id': 1,
                    'image': 'POL.png',
                    'label': 'Poland',
                    'x': 18.280168533325195,
                    'y': 25.909019470214844
                },
                {
                    'cluster': 1,
                    'id': 2,
                    'image': 'UKR.png',
                    'label': 'Ukraine',
                    'x': 17.806306838989258,
                    'y': 26.555574417114258
                },
                {
                    'cluster': 1,
                    'id': 3,
                    'image': 'GER.png',
                    'label': 'Germany',
                    'x': 18.745168685913086,
                    'y': 26.335153579711914
                },
                {
                    'cluster': 1,
                    'id': 4,
                    'image': 'JPN.png',
                    'label': 'Japan',
                    'x': 18.288522720336914,
                    'y': 26.75434684753418
                },
                {
                    'cluster': 0,
                    'id': 5,
                    'image': 'RUS.png',
                    'label': 'Russia',
                    'x': -10.483757972717285,
                    'y': 16.344135284423828
                },
                {
                    'cluster': 0,
                    'id': 6,
                    'image': 'USA.png',
                    'label': 'USA',
                    'x': -10.892544746398926,
                    'y': 16.211212158203125
                },
                {
                    'cluster': 0,
                    'id': 7,
                    'image': 'CHN.png',
                    'label': 'China',
                    'x': -10.799576759338379,
                    'y': 15.647771835327148
                },
                {
                    'cluster': 1,
                    'id': 8,
                    'image': 'BRB.png',
                    'label': 'Barbados',
                    'x': 19.17897605895996,
                    'y': 25.615243911743164
                },
                {
                    'cluster': 1,
                    'id': 9,
                    'image': 'BLZ.png',
                    'label': 'Belize',
                    'x': 18.981752395629883,
                    'y': 25.27176856994629
                },
                {
                    'cluster': 1,
                    'id': 10,
                    'image': 'FIJ.png',
                    'label': 'Fiji',
                    'x': 19.603906631469727,
                    'y': 25.899328231811523
                },
                {
                    'cluster': 0,
                    'id': 11,
                    'image': 'IND.png',
                    'label': 'India',
                    'x': -10.399707794189453,
                    'y': 15.35216236114502
                },
                {
                    'cluster': 0,
                    'id': 12,
                    'image': 'MEX.png',
                    'label': 'Mexico',
                    'x': -9.994535446166992,
                    'y': 15.759873390197754
                }
            ],
            "animals": [
                {
                    'cluster': 0,
                    'id': 1,
                    'label': 'Ant',
                    'x': 2.4962680339813232,
                    'y': -36.414344787597656
                },
                {
                    'cluster': 0,
                    'id': 2,
                    'label': 'Spider',
                    'x': 3.9534926414489746,
                    'y': -35.974952697753906
                },
                {
                    'cluster': 1,
                    'id': 3,
                    'label': 'Fish',
                    'x': 2.8412554264068604,
                    'y': -38.76316452026367
                },
                {
                    'cluster': 1,
                    'id': 4,
                    'label': 'Frog',
                    'x': 4.640581130981445,
                    'y': -39.1514778137207
                },
                {
                    'cluster': 1,
                    'id': 5,
                    'label': 'Snake',
                    'x': 5.762447834014893,
                    'y': -37.792884826660156
                },
                {
                    'cluster': 1,
                    'id': 6,
                    'label': 'Bird',
                    'x': 6.621478080749512,
                    'y': -39.617469787597656
                },
                {
                    'cluster': 1,
                    'id': 7,
                    'label': 'Horse',
                    'x': 3.271048069000244,
                    'y': -40.76041793823242
                },
                {
                    'cluster': 1,
                    'id': 8,
                    'label': 'Whale',
                    'x': 5.1712422370910645,
                    'y': -41.23802947998047
                }
            ]
        }
        
        if id in examples:
            return examples[id]
        else:
            print(f"No map example with id: '{id}'")

    def get_nodes_spec(self, id:str):

        return self.nodes_spec_api.get_nodes_spec(id)
    
    def combine_embeddings(self, embeddings_models:list[list[list]], input_reduction_size:int=False, final_size:int=False, 
                            normalize_input:bool=True, normalize_output:bool=True, to_lists:bool=False):
        
        return self.preprocessor.combine_embeddings(embeddings_models=embeddings_models, 
                                                            input_reduction_size=input_reduction_size,
                                                            final_size=final_size, 
                                                            normalize_input=normalize_input, 
                                                            normalize_output=normalize_output, 
                                                            to_lists=to_lists)
    
    def normalize_embeddings(self, embeddings:list[list], to_lists:bool=False):

        return self.preprocessor.normalize_embeddings(embeddings=embeddings, to_lists=to_lists)
    
    def reduce_embeddings(self, embeddings:list[list], reduction_size:int, normalize_input:bool=True, normalize_output:bool=True, to_lists:bool=False):

        return self.preprocessor.reduce_embeddings(embeddings=embeddings,
                                                           reduction_size=reduction_size,
                                                           normalize_input=normalize_input,
                                                           normalize_output=normalize_output,
                                                           to_lists=to_lists)