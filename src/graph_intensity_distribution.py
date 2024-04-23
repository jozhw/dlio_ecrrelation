import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from calculations.calculate_entropy import count_occurrences


def graph_intensity_distribution(
    path_to_image: str,
    path_to_data: str = "results/local/data/2024-04-23/synthetic_imgs_results.csv",
    save_path="results/local/intensity_distributions/",
):

    # get entropy and compression loss ratio
    df = pd.read_csv(path_to_data)

    # get file name
    raw_fname = os.path.basename(path_to_image)
    fname = os.path.splitext(raw_fname)[0]
    synthetic_name = "synthetic_{}.0".format(fname)

    fname_row_match = df[df["file_name"] == synthetic_name]

    if not fname_row_match.empty:
        entropy = fname_row_match.iloc[0]["entropy"]
        npz_compressed_synthetic_original_ratio = fname_row_match.iloc[0][
            "npz_compressed_synthetic_original_ratio"
        ]
    else:
        raise ValueError("No matching row found for {}".format(synthetic_name))

    # save path
    save_path = save_path + "{}.png".format(fname)

    # load image into numpy array
    image: np.ndarray = np.array(Image.open(path_to_image))

    occurances = count_occurrences(image)

    # Extract keys and values
    keys = list(range(256))
    values = [occurances.get(key, 0) for key in keys]

    plt.figure(figsize=(12, 8))
    plt.bar(keys, values, color="blue", alpha=0.7)
    plt.xlabel("Intensity Value")
    plt.ylabel("Frequency")
    plt.title(
        "Intensity Distribution for {} \nwith a NPZ Compressed Synthetic to Original Ratio of {} and Entropy of {}".format(
            fname, npz_compressed_synthetic_original_ratio, entropy
        )
    )
    plt.grid(True)

    plt.savefig(save_path)
    plt.show()


if __name__ == "__main__":
    paths = [
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/9733.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/6400.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/823.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/4217.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/3578.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/10321.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/2666.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/5109.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/11981.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/10447.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/2100.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/11759.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/4571.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/7078.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/12250.jpg",
    ]

    for path in paths:
        graph_intensity_distribution(path)
