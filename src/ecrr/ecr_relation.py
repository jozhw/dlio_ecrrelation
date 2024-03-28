"""
ECrRelation stands for entropy and compression ratio relationship. This class
will be used to handle all calculations associated to calculate the
relationship.
"""

import json
import os
import re
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image

from src.calculations.calculate_cr_by_file_type import calculate_cr_by_file_type
from src.calculations.calculate_entropy import calculate_entropy, count_occurrences
from src.plotting.generate_ecrr_plot import generate_npz_ecrr_plot
from src.plotting.generate_entropy_uncompressed_plot import (
    generate_entropy_uncompressed_plot,
)
from src.utils.generate_csv import generate_csv
from src.utils.generate_save_paths import (
    generate_compressed_img_save_paths,
    generate_save_result_data_path,
    generate_save_result_plot_path,
)
from src.utils.set_img_path import set_img_path
from src.validations.file_type_validations import validate_compressed_file_type
from src.validations.json_validations import (
    validate_json_extension,
    validate_json_img_path,
)


class ECrRelation:
    """
    To Initate:

    json_img_path must contain a dir indicating the date in YYYY-MM_DD format.

    save_dir is important since it is used to determine how the image path is set
    the reason why this exists is because of calculations on polaris

    """

    ACCEPTED_FILE_TYPES = ["npz", "jpg"]

    def __init__(
        self, json_img_path: str, save_dir: str, compressed_file_types: List[str]
    ):

        self.json_img_path: str = json_img_path
        self.save_dir: str = save_dir
        self.compressed_file_types: List[str] = compressed_file_types
        # init save the results
        self.results: Dict = {}

        # regular expression to get the date of imagenet image path gen
        self.regex_date_pattern: str = r"\b\d{4}-\d{2}-\d{2}\b"

        # if json_img_path is incorrect format, return value error
        validate_json_img_path(self.regex_date_pattern, self.json_img_path)

        # check to see if a json file was given
        validate_json_extension(self.json_img_path)

        # check to see if a valid compressed_file_type was given
        validate_compressed_file_type(
            ECrRelation.ACCEPTED_FILE_TYPES, self.compressed_file_types
        )

        # set date
        self.date: str = re.findall(self.regex_date_pattern, self.json_img_path)[0]

        # set save path
        self.paths_to_save_compressed_imgs: Dict[str, str] = (
            generate_compressed_img_save_paths(
                ECrRelation.ACCEPTED_FILE_TYPES,
                self.compressed_file_types,
                self.save_dir,
                self.date,
            )
        )
        # set save results path
        self.path_to_save_results_data: str = generate_save_result_data_path(
            self.save_dir, self.date
        )
        # set save plot path
        self.path_to_save_results_plot: str = generate_save_result_plot_path(
            self.save_dir, self.date
        )

    def load_data(self):
        with open(self.json_img_path) as f:
            self.data: Dict = json.load(f)

    def calculate(self):
        # keep track of iterations

        num_iter: int = 0

        for path in self.data["paths"]:

            image_path: str = set_img_path(path, self.save_dir)

            # load image into numpy array
            image: np.ndarray = np.array(Image.open(image_path))

            # get dimensions
            dimensions: Tuple = image.shape[:2]

            # calculate occurances
            # since we are using rgb, avoid grayscale
            if len(image.shape) == 2 or image.shape[2] != 3:
                continue

            occurances: Dict = count_occurrences(image)

            # calculate the entropy
            entropy: float = calculate_entropy(occurances, dimensions)

            # get file name
            fname, _ = os.path.splitext(os.path.basename(path))

            # want also to store the uncompressed size and the npz compressed size
            uncompressed_size: int = dimensions[0] * dimensions[1] * 3

            # store to results dict
            self.results[fname] = {
                "entropy": entropy,
                "uncompressed_size": uncompressed_size,
            }

            # get compression ratio calculations and compressed file sizes
            # based on file type and then store in results obj
            cr_calculations: Dict[str, Dict[str, float]] = calculate_cr_by_file_type(
                fname,
                image,
                dimensions,
                self.compressed_file_types,
                self.paths_to_save_compressed_imgs,
            )

            for key in cr_calculations:
                for skey, svalue in cr_calculations[key].items():
                    self.results[fname][skey] = svalue

            # add to iteration completed
            num_iter += 1

            print(
                "Completed iteration - {} for {}: entropy={}, compression_ratio={} \n".format(
                    num_iter,
                    fname,
                    entropy,
                    cr_calculations["npz"]["npz_compression_ratio"],
                )
            )

    def save_to_csv(self):
        generate_csv(self.path_to_save_results_data, "results.csv", self.results)

    def gen_npz_ecrr_plot(self):
        generate_npz_ecrr_plot(
            os.path.join(self.path_to_save_results_data, "results.csv"),
            self.path_to_save_results_plot,
        )

    def gen_entropy_uncompressed_plot(self):
        generate_entropy_uncompressed_plot(
            os.path.join(self.path_to_save_results_data, "results.csv"),
            self.path_to_save_results_plot,
        )
