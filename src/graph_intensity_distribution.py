import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from calculations.calculate_entropy import count_occurrences


def graph_intensity_distribution(
    path_to_image: str, save_path="results/local/intensity_distributions/"
):

    # get file name
    raw_fname = os.path.basename(path_to_image)

    fname = os.path.splitext(raw_fname)[0]

    # save path
    save_path = save_path + "{}.png".format(fname)

    # load image into numpy array
    image: np.ndarray = np.array(Image.open(path_to_image))

    occurances = count_occurrences(image)

    values = [occurances.get(key, 0) for key in range(256)]
    plt.hist(values, bins=50, color="blue", alpha=0.7)
    plt.xlabel("Intensity Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Intensity Values for {}".format(fname))
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
    ]

    for path in paths:
        graph_intensity_distribution(path)
