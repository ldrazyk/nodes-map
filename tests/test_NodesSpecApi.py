from src.app.model import NodesSpecApi
from pprint import pprint
from myfiles import Storage, FilesManager
from mytext import TextEditor

storage = Storage()
text_editor = TextEditor()
files_manager = FilesManager(text_editor)

api = NodesSpecApi(storage=storage, files_manager=files_manager, text_editor=text_editor)

def test_NodesSpecApi():

    def test_get_ids():

        print(api.get_ids())

    def test_get_nodes_spec():

        def test(id):
            
            print(f"'{id}' nodes spec:")
            pprint(api.get_nodes_spec(id=id))

        test("countries.tsv")

    test_get_ids()
    test_get_nodes_spec()