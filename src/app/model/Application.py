from .Mapper import Mapper

class Application:

    def __init__(self):

        self.mapper = Mapper()

    def get_map(self):

        return


    def get_map_example(self, id:str):

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