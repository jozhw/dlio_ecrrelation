from typing import Dict


def calculate_mean(occurances: Dict):

    total_sum = 0
    total_count = 0

    for key, value in occurances.items():

        total_sum += key * value
        total_count += value

        if total_count == 0:
            return 0

    return total_sum / total_count
