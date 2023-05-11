import numpy as np
import h5py

def values_from_file(path: str = None) -> np.ndarray:
    try:
        with open(path) as f:
            return np.loadtxt(f)
            # return values if len(values) != 0 else None
    except FileNotFoundError:
        return None
    except ValueError:
        return None
    
def open_h5py(path):
    with h5py.File(path, 'r') as f:
        return np.array(f['Base_Group/default'])
   
def save_h5py(path: str, data: np.ndarray) -> None:
    with h5py.File(path, 'w') as f:
        g = f.create_group('Base_Group')
        g.create_dataset('default', data=data)
        