from myfiles import Repository
import numpy as np

class NodesSpecApi:

    def __add_code_spec(self):

        spec = {
            "countries0": {
                "id": ["pol", "rus", "ger", "usa", "chn", "ind"],
                "label": ["Poland", "Russia", "Germany", "USA", "China", "India"],
                "embedding": [
                    [38, 0.31, 125, 0.98],
                    [144, 16.38, 9, 2.08],
                    [84, 0.35, 241, 4.74],
                    [347, 9.15, 38, 30.51],
                    [1416, 9.39, 151, 19.23],
                    [1464, 2.97, 492, 4.19]
                ]
            }
        }

        self.nodes_spec.update(spec)


    def __init__(self, storage, files_manager, text_editor):
        
        self.repository = Repository(dir="data/nodes_spec",
                                     dir_id="nodes_spec",
                                     storage=storage,
                                     files_manager=files_manager,
                                     text_editor=text_editor)
        self.nodes_spec = {}
        self.__add_code_spec()
        self.ids = list(self.nodes_spec.keys()) + self.repository.get_item_ids()

    def get_nodes_spec(self, id:str):

        def get_spec_from_sv_file(id):

            def get_columns_and_data():

                data = self.repository.get_item(id, to_dicts=False)

                columns = data[0]
                data = data[1:]

                return columns, data
            
            def parse_key_and_feature_scale(column_name:str):

                if column_name[0] in ["$", "&", "%", "#"]:

                    scale = float(column_name[1:4])

                    if column_name[0] in ["$", "%"]:

                        key = column_name[4:]
                    else:
                        key = False
                else:
                    key = column_name
                    scale = False

                return key, scale

            def parse_percenile_convert(column_name:str):

                 if column_name[0] in ["%", "#"]:
                    return True

            def get_percentiles(data, j, key):

                print(f"\nGetting percentiles for key '{key}'")

                arr = np.array([row[j] for row in data], dtype=float)
                print(arr)
                percentiles = np.searchsorted(np.sort(arr), arr) / (len(arr) - 1) * 100
                print(percentiles)
                return percentiles

            columns, data = get_columns_and_data()

            spec = {"embedding": [], "feature_scale": []}

            for j, column_name in enumerate(columns):

                key, feature_scale = parse_key_and_feature_scale(column_name)
                percentile_convert = parse_percenile_convert(column_name)

                if key:
                    spec[key] = []

                if feature_scale:
                    spec["feature_scale"].append(feature_scale)

                if percentile_convert:
                    percentiles = get_percentiles(data, j, key)

                for i, array in enumerate(data):
                    
                    if j == 0:
                        spec["embedding"].append([])

                    value = array[j]

                    if percentile_convert:
                        value = percentiles[i]
                    elif feature_scale:
                        value = float(value)

                    if feature_scale:
                        spec["embedding"][i].append(value)

                    if key:
                        spec[key].append(value)

            return spec
        
        def get_spec_from_json_file(id):

            return False
        

        if id in self.nodes_spec:
            return self.nodes_spec.get(id)
        elif id in self.ids:
            if id[-2:] == "sv":
                return get_spec_from_sv_file(id)
            else:
                return get_spec_from_json_file(id)
    
    def get_ids(self):

        return self.ids