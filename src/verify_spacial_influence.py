import os

import cv2
import numpy as np
from PIL import Image

from calculations.calculate_entropy import calculate_entropy, count_occurrences
from utils.remove_compressed_imgs import remove_compressed_imgs


def new_verify_lossy_spatial_influence(path_to_image: str):
    raw_fname = os.path.basename(path_to_image)
    fname = os.path.splitext(raw_fname)[0]

    # Load the image using OpenCV
    image = cv2.imread(path_to_image)

    # Convert the image to a NumPy array
    image_array = np.array(image)

    occurrences = count_occurrences(image_array)
    entropy = calculate_entropy(occurrences)
    shape = image_array.shape

    print(shape)

    # Shuffle the pixels
    shuffled_image_array = image_array.reshape(-1)
    np.random.shuffle(shuffled_image_array)
    shuffled_image_array = shuffled_image_array.reshape(shape)

    # Save the shuffled image using OpenCV
    cv2.imwrite(
        "shuffled_{}.jpg".format(fname),
        shuffled_image_array,
        [int(cv2.IMWRITE_JPEG_QUALITY), 100],
    )

    # Save the original image using OpenCV
    cv2.imwrite(
        "{}.jpg".format(fname), image_array, [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    )

    shuffled_size = os.path.getsize("shuffled_{}.jpg".format(fname))
    unshuffled_size = shape[0] * shape[1] * 3

    saved_unshuffled_size = os.path.getsize("{}.jpg".format(fname))

    ratio1 = unshuffled_size / shuffled_size
    ratio2 = unshuffled_size / saved_unshuffled_size

    remove_compressed_imgs("shuffled_{}.jpg".format(fname))
    remove_compressed_imgs("{}.jpg".format(fname))

    return fname, entropy, ratio1, ratio2


def verify_lossy_spacial_influence(path_to_image: str):
    # get file name
    raw_fname = os.path.basename(path_to_image)

    fname = os.path.splitext(raw_fname)[0]

    # load image into numpy array
    image: np.ndarray = np.array(Image.open(path_to_image))

    occurances = count_occurrences(image)

    entropy = calculate_entropy(occurances)

    shape = image.shape

    print(shape)

    shuffled_image = image.reshape(-1)

    np.random.shuffle(shuffled_image)

    shuffled_image = np.array(shuffled_image, dtype=np.uint8).reshape(shape)

    shuffled_img = Image.fromarray(
        shuffled_image.astype("uint8"),
        "RGB",
    )

    shuffled_img.save("shuffled_{}.jpg".format(fname))
    shuffled_size = os.path.getsize("shuffled_{}.jpg".format(fname))

    # second shuffle
    np.random.shuffle(shuffled_image)

    shuffled_image_2 = np.array(shuffled_image, dtype=np.uint8).reshape(shape)

    shuffled_img_2 = Image.fromarray(shuffled_image_2.astype("uint8"), "RGB")

    shuffled_img_2.save("shuffled_{}_2.jpg".format(fname), quality=95)

    shuffled_size_2 = os.path.getsize("shuffled_{}_2.jpg".format(fname))

    img = Image.fromarray(image.astype("uint8"), "RGB")

    img.save("{}.jpg".format(fname))

    saved_unshuffled_size = os.path.getsize("{}.jpg".format(fname))
    unshuffled_size = shape[0] * shape[1] * 3

    # noticed that there is an issue with the os.path.getsize of original
    # vs the bit calculation

    remove_compressed_imgs("{}.jpg".format(fname))
    remove_compressed_imgs("shuffled_{}.jpg".format(fname))
    remove_compressed_imgs("shuffled_{}_2.jpg".format(fname))

    ratio = unshuffled_size / shuffled_size
    ratio2 = unshuffled_size / shuffled_size_2

    ratio3 = unshuffled_size / saved_unshuffled_size
    return fname, entropy, ratio, ratio2, ratio3


def verify_lossless_spacial_influence(path_to_image: str):

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
    import glob

    paths = glob.glob(
        "/Users/johnz.wu/Projects/Code/dlio_ecrrelation/assets/local/uncompressed_imgs/jpg/*.jpg"
    )[:100]

    for path in paths:
        # print(verify_lossless_spacial_influence(path))
        print(verify_lossy_spacial_influence(path))
        # print(new_verify_lossy_spatial_influence(path))
