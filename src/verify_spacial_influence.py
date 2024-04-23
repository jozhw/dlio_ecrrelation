import os

import numpy as np
from PIL import Image

from calculations.calculate_entropy import calculate_entropy, count_occurrences
from utils.remove_compressed_imgs import remove_compressed_imgs


def verify_spacial_influence(path_to_image: str):

    # get file name
    raw_fname = os.path.basename(path_to_image)

    fname = os.path.splitext(raw_fname)[0]

    # load image into numpy array
    image: np.ndarray = np.array(Image.open(path_to_image))

    occurances = count_occurrences(image)

    entropy = calculate_entropy(occurances)

    print(image)

    shape = image.shape

    shuffled_image = image.reshape(-1)

    np.random.shuffle(shuffled_image)

    shuffled_image = np.array(shuffled_image, dtype=np.uint8).reshape(shape)

    print(image)

    np.savez_compressed("shuffled_{}.npz".format(fname), shuffled_image)

    shuffled_size = os.path.getsize("shuffled_{}.npz".format(fname))

    np.savez_compressed("{}.npz".format(fname), image)

    unshuffled_size = os.path.getsize("{}.npz".format(fname))

    remove_compressed_imgs("{}.npz".format(fname))
    remove_compressed_imgs("shuffled_{}.npz".format(fname))

    ratio = shuffled_size / unshuffled_size

    return fname, entropy, ratio


if __name__ == "__main__":
    paths = [
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/9733.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/6400.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/823.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/4217.jpg",
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/3578.jpg",
    ]

    for path in paths:
        print(verify_spacial_influence(path))
