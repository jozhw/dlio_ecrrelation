import os
from typing import Dict, List


def generate_compressed_img_save_paths(
    accepted_file_types: List[str],
    compressed_file_types: List[str],
    save_dir: str,
    date: str,
) -> Dict[str, str]:

    compressed_file_save_paths: Dict[str, str] = {}

    for accepted_file_type in accepted_file_types:
        if accepted_file_type in compressed_file_types:
            # create path
            save_path: str = "./assets/{}/compressed_imgs/{}/{}".format(
                save_dir, accepted_file_type, date
            )
            # generate path
            os.makedirs(save_path, exist_ok=True)
            # save path to dict with file type as key
            compressed_file_save_paths[accepted_file_type] = save_path
        else:
            continue

    return compressed_file_save_paths


def generate_save_result_data_path(save_dir: str, date: str) -> str:
    save_path: str = "./results/{}/data/{}".format(save_dir, date)

    os.makedirs(save_path, exist_ok=True)
    return save_path


def generate_save_result_plot_path(save_dir: str, date: str) -> str:
    save_path: str = "./results/{}/plots/{}".format(save_dir, date)

    os.makedirs(save_path, exist_ok=True)
    return save_path
