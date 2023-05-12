import numpy as np
import h5py
import os

def values_from_file(path: str = None) -> np.ndarray:
    try:
        with open(path) as f:
            return np.loadtxt(f)
            # return values if len(values) != 0 else None
    except FileNotFoundError:
        return None
    except ValueError:
        return None
    
class with_h5py_matrix:
    def __init__(self, file_name):
        if os.path.exists(file_name):
            self._file_name = file_name
        else:
            raise FileExistsError(F"Не нашли файл: {file_name}")
    
    @property
    def read_data(self):
        with h5py.File(self._file_name, 'r') as f:
            return f["Base_Group/default"]
    
    @property
    def write_data(self):
        with h5py.File(self._file_name, 'w') as f:
            return f['Base_Group/default']
    
    @property
    def shape(self) -> tuple:
        with h5py.File(self._file_name, 'r') as f:
            return f['Base_Group/default'].shape
                       
            
        
    
    