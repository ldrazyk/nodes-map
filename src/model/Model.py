import os
from myfiles.MyFile import MyFile

class Model:
    
    def __init__(self):
        
        self.nodes_dir = "../data/nodes/"
        
    
    def get_node_files_list(self):
        
        files = os.listdir(self.nodes_dir)
        print(files)
        return files
    
    
    def get_nodes_data(self, file):
        
        def convert_xy(data):
            
            for node in data:
                node["x"] = float(node["x"])
                node["y"] = float(node["y"])
        
        my_file = MyFile(dir=self.nodes_dir, file=file, print_info=True)
        if my_file.exists():
            ext = my_file.get_ext()
            data = my_file.read(data_type=ext[1:], dict=True)
            convert_xy(data)
            return data
        else:
            return False
        
    def get_extremes(self, nodes):
        
        x = []
        y = []
        
        for node in nodes:
            
            x.append(node['x'])
            y.append(node['y'])
            
        return {
            "min_x": min(x),
            "max_x": max(x),
            "min_y": min(y),
            "max_y": max(y),
        }