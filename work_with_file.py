import numpy as np

def values_from_file(path: str = None) -> np.ndarray:
    try:
        with open(path) as f:
            return np.loadtxt(f, dtype=np.int8)
            # return values if len(values) != 0 else None
    except FileNotFoundError:
        return None
    except ValueError:
        return None