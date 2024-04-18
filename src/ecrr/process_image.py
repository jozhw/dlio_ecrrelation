"""
Serves as the most superficial wrapper for all of the compression and 
calculation functionalities.
"""

import os
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

from src.calculations.calculate_entropy import (
    calculate_entropy,
    count_each_rgb_occurrences,
    count_occurrences,
)
from src.calculations.calculate_mean import calculate_mean
from src.calculations.calculate_results import calculate_results
from src.utils.set_img_path import set_img_path


def process_image(
    path: str,
    save_dir: str,
    compressed_file_types: List[str],
    paths_to_save_compressed_imgs: Dict[str, str],
) -> Optional[Tuple[str, Dict[str, float]]]:
    image_path: str = set_img_path(path, save_dir)
    # load image into numpy array
    image: np.ndarray = np.array(Image.open(image_path))

    # get dimensions
    dimensions: Tuple = image.shape[:2]

    # calculate occurances
    # since we are using rgb, avoid grayscale
    if len(image.shape) == 2 or image.shape[2] != 3:
        return None

    occurances: Dict = count_occurrences(image)
    mean: int = calculate_mean(occurances)
    entropy: float = calculate_entropy(occurances)

    r_occurances, g_occurances, b_occurances = count_each_rgb_occurrences(image)

    r_mean: int = calculate_mean(r_occurances)
    r_entropy: float = calculate_entropy(r_occurances)

    g_mean: int = calculate_mean(g_occurances)
    g_entropy: float = calculate_entropy(g_occurances)

    b_mean: int = calculate_mean(b_occurances)
    b_entropy: float = calculate_entropy(b_occurances)

    fname, _ = os.path.splitext(os.path.basename(path))
    uncompressed_size: int = dimensions[0] * dimensions[1] * 3

    result: Dict[str, float] = {
        "entropy": entropy,
        "uncompressed_size": uncompressed_size,
        "uncompressed_width": dimensions[0],
        "uncompressed_height": dimensions[1],
        "mean_intensity_value": mean,
        "red_mean_intensity_value": r_mean,
        "green_mean_intensity_value": g_mean,
        "blue_mean_intensity_value": b_mean,
        "red_entropy_intensity_value": r_entropy,
        "green_entropy_intensity_value": g_entropy,
        "blue_entropy_intensity_value": b_entropy,
    }

    cr_calculations: Dict[str, Dict[str, float]] = calculate_results(
        fname,
        image,
        dimensions,
        compressed_file_types,
        paths_to_save_compressed_imgs,
    )

    for key in cr_calculations:
        for skey, svalue in cr_calculations[key].items():
            result[skey] = svalue

    return fname, result
