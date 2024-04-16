from typing import Dict

"""
Returns rounded mean intensity value to the nearest integer
"""


def calculate_mean(occurances: Dict) -> int:

    total_sum = 0
    total_count = 0

    for key, value in occurances.items():

        total_sum += key * value
        total_count += value

        if total_count == 0:
            return 0

    return round(total_sum / total_count)
