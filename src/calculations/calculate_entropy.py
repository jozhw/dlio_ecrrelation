import math
from typing import Dict, Tuple

import numpy as np


def count_occurrences(image_data: np.ndarray) -> Dict:
    occurrences: Dict = {}
    for row in image_data:
        for pixel in row:
            for value in pixel:
                if value in occurrences:
                    occurrences[value] += 1
                else:
                    occurrences[value] = 1
    return occurrences


def count_each_rgb_occurrences(image_data: np.ndarray) -> Tuple[Dict, Dict, Dict]:
    r_occurances = {}
    g_occurances = {}
    b_occurances = {}

    for row in image_data:
        for pixel in row:
            r_value = pixel[0]
            g_value = pixel[1]
            b_value = pixel[2]

            if r_value in r_occurances:
                r_occurances[r_value] += 1
            else:
                r_occurances[r_value] = 1

            if g_value in g_occurances:
                g_occurances[g_value] += 1
            else:
                g_occurances[g_value] = 1

            if b_value in b_occurances:
                b_occurances[b_value] += 1
            else:
                b_occurances[b_value] = 1

    return r_occurances, g_occurances, b_occurances


def calculate_entropy(occurrences: Dict) -> float:
    # the summation of all the occurrences for each intensity value will
    # give you the image size
    file_size: int = 0
    for value in occurrences.values():
        file_size += value

    entropy: float = 0
    for count in occurrences.values():
        if count != 0:
            entropy += -(count / file_size) * math.log2(count / file_size)
    return entropy
