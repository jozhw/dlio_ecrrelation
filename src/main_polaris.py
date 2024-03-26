# with root dir as the working dir

import csv
import json
import os
import re
from typing import Dict, Tuple

import numpy as np
from PIL import Image

from calculate_compression_ratio import calculate_compression_ratio

# import calculation modules
from calculate_entropy import calculate_entropy, count_occurrences

# path to json file
JSON_FILE: str = "assets/polaris/img_paths/2024-03-26/imagenet_rand_5000.json"

# regular expression to get the date of imagenet image path gen
pattern: str = r"\b\d{4}-\d{2}-\d{2}\b"

date: str = re.findall(pattern, JSON_FILE)[0]

# make the directory to store all of the npz compressed images
# relative to the root dir
path_to_npz_save: str = "./assets/polaris/npz/{}".format(date)

os.makedirs(path_to_npz_save, exist_ok=True)

# make the directory to store all of the data points for entropy and
# compression ratio

path_to_data_save: str = "./results/polaris/data/{}".format(date)

os.makedirs(path_to_data_save, exist_ok=True)

# store results data
results: Dict = {}

# read json file
with open(JSON_FILE) as f:
    data: Dict = json.load(f)

# keep track of iterations

iter: int = 0

for path in data["paths"]:

    # set image path
    image_path: str = os.path.join(os.path.expanduser("~"), "..", "..", path)

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

    # set up compressed image save
    compressed_image_path: str = os.path.join(path_to_npz_save, f"{fname}.npz")

    # compress and save the image
    np.savez_compressed(compressed_image_path, image)

    # calculate the entropy
    entropy: float = calculate_entropy(occurances, dimensions)

    # calculate the compression ratio
    compression_ratio: float = calculate_compression_ratio(
        compressed_image_path, dimensions
    )

    # store to results dict
    results[fname] = {"entropy": entropy, "compression_ratio": compression_ratio}

    # add to iteration completed
    iter += 1

    print(
        "Completed iteration - {} for {}: entropy={}, compression_ratio={} \n".format(
            iter, fname, entropy, compression_ratio
        )
    )

# save to csv file
csv_file = os.path.join(path_to_data_save, "results.csv")

# write to csv_file
with open(csv_file, "w", newline="") as file:
    writer = csv.DictWriter(
        file, fieldnames=["file_name", "entropy", "compression_ratio"]
    )
    writer.writeheader()
    for file_name, values in results.items():
        writer.writerow(
            {
                "file_name": file_name,
                "entropy": values["entropy"],
                "compression_ratio": values["compression_ratio"],
            }
        )

print("Data saved to", csv_file)
