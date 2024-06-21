import os
import glob
    
    
class Media:
    @classmethod
    def save(cls, file, path):
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        
        for file_path in glob.glob(dir_path + "/*"):
            os.remove(file_path)
            
        with open(file=path, mode="wb") as file_output:
            file_output.write(file.read())

    @classmethod
    def clean(cls, path):
        dir_path = os.path.dirname(path)
   
        for file_path in glob.glob(dir_path + "/*"): 
            os.remove(file_path)