import numpy as np
from typing import List


def cosine(a: List[float], b: List[float]) -> float:
    a1 = np.array(a)
    b1 = np.array(b)
    denom = (np.linalg.norm(a1) * np.linalg.norm(b1))
    if denom == 0:
        return 0.0
    return float(a1 @ b1 / denom)
