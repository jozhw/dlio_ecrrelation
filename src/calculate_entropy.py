import math
from typing import Dict

import numpy as np

from type_hints import Matrix


def count_occurrences(image_data: np.array) -> Dict:
    occurrences: Dict = {}
    for row in image_data:
        for pixel in row:
            for value in pixel:
                if value in occurrences:
                    occurrences[value] += 1
                else:
                    occurrences[value] = 1
    return occurrences


def calculate_entropy(occurrences: Dict, dimensions: Matrix) -> float:
    file_size: int = dimensions[0] * dimensions[1]
    entropy: float = 0
    for count in occurrences.values():
        if count != 0:
            entropy += -(count / file_size) * math.log2(count / file_size)
    return entropy
