"""
ECrRelation stands for entropy and compression ratio relationship. This class
will be used to handle all calculations associated to calculate the
relationship.
"""

import json
import os
import re
from typing import Dict, List

from mpi4py import MPI

from src.ecrr.process_image import process_image
from src.plotting.generate_ecrr_plot import (
    generate_jpg_ecrr_plot,
    generate_npz_ecrr_plot,
)
from src.plotting.generate_entropy_compressed_jpg_npz_plot import (
    generate_entropy_compressed_jpg_npz_plot,
)
from src.plotting.generate_entropy_uncompressed_plot import (
    generate_entropy_uncompressed_plot,
)
from src.utils.generate_csv import generate_csv
from src.utils.generate_save_paths import (
    generate_compressed_img_save_paths,
    generate_save_result_data_path,
    generate_save_result_plot_path,
)
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

    def process_images(self):
        num_iter = 0
        comm = MPI.COMM_WORLD
        rank: int = comm.Get_rank()
        size: int = comm.Get_size()

        # only the 0th rank can load the data
        if rank == 0:
            self.load_data()
            paths = self.data["paths"]
        else:
            paths = None

        # broadcast paths to all nodes
        paths = comm.bcast(paths, root=0)

        # distribute the paths across processes
        paths_per_process = [[] for _ in range(size)]
        for i, path in enumerate(paths):
            paths_per_process[i % size].append(path)

        # to prevent duplications
        local_results: Dict = {}

        # each process works on its assigned paths
        for path in paths_per_process[rank]:
            result = process_image(
                path,
                self.save_dir,
                self.compressed_file_types,
                self.paths_to_save_compressed_imgs,
            )
            if result is not None:
                fname, data = result
                local_results[fname] = data
                num_iter += 1
                # print(
                #    "Process {}, Completed iteration - {} for {}: entropy={}, compression_ratio={}".format(
                #        rank,
                #        num_iter,
                #        fname,
                #        data["entropy"],
                #        data["npz_compression_ratio"],
                #    )
                # )

        # gather results from all processes
        all_results = comm.gather(local_results, root=0)

        if rank == 0 and all_results is not None:
            # merge results from all processes
            for res in all_results:
                self.results.update(res)

    def save_to_csv(self):
        generate_csv(self.path_to_save_results_data, "results.csv", self.results)

    def gen_npz_ecrr_plot(self):
        generate_npz_ecrr_plot(
            os.path.join(self.path_to_save_results_data, "results.csv"),
            self.path_to_save_results_plot,
        )

    def gen_jpg_ecrr_plot(self):
        generate_jpg_ecrr_plot(
            os.path.join(self.path_to_save_results_data, "results.csv"),
            self.path_to_save_results_plot,
        )

    def gen_entropy_uncompressed_plot(self):
        generate_entropy_uncompressed_plot(
            os.path.join(self.path_to_save_results_data, "results.csv"),
            self.path_to_save_results_plot,
        )

    def gen_entropy_compressed_jpg_npz_plot(self):
        generate_entropy_compressed_jpg_npz_plot(
            os.path.join(self.path_to_save_results_data, "results.csv"),
            self.path_to_save_results_plot,
        )
