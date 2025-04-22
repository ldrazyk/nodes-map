import os

class Model:
    
    def __init__(self):
        
        return
    
    def get_node_files_list(self):
        
        files = os.listdir("../data/nodes/")
        print(files)
        return files
    
    