import os
from typing import Dict, List, Tuple

import numpy as np

from src.calculations.calculate_compression_ratio import calculate_compression_ratio

"""
return compression_ratio and file_size for each compressed_file_type
"""


def calculate_cr_by_file_type(
    fname: str,
    image: np.ndarray,
    dimensions: Tuple,
    compressed_file_types: List[str],
    compressed_save_paths: Dict[str, str],
) -> Dict[str, Dict[str, float]]:
    cr_calculations: Dict[str, Dict[str, float]] = {}

    for file_type in compressed_file_types:

        key_size: str = "{}_compressed_image_size".format(file_type)
        key_cr: str = "{}_compression_ratio".format(file_type)

        compressed_image_path: str = os.path.join(
            compressed_save_paths[file_type],
            f"{fname}.{file_type}",
        )

        if file_type == "npz":
            # lossless compression
            np.savez_compressed(compressed_image_path, image)
        else:
            # put other compression algorithms here
            pass

        # calculate the compression ratio
        compression_ratio: float = calculate_compression_ratio(
            compressed_image_path, dimensions
        )

        compressed_file_size: int = os.path.getsize(compressed_image_path)

        cr_calculations[file_type] = {
            key_cr: compression_ratio,
            key_size: compressed_file_size,
        }

    return cr_calculations
