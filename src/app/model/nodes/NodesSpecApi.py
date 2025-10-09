class NodesSpecApi:

    def __init__(self):
        
        self.nodes_spec = {
            "countries": {
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

    def get_nodes_spec(self, id:str):

        return self.nodes_spec.get(id)