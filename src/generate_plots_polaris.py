# with root dir as the working dir
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ecrr.ecr_relation import ECrRelation

REMOVE_FROM_DIR = "./assets/polaris/compressed_imgs"
EXTENSIONS = [".jpg", ".npz"]


def main():
    # path to json file

    JSON_FILE: str = "assets/polaris/img_paths/2024-04-04/imagenet_rand_300000.json"

    ecrr = ECrRelation(JSON_FILE, "polaris", ["npz", "jpg"])

    ecrr.load_data()

    start_time = time.time()

    ecrr.gen_npz_ecrr_plot()
    # ecrr.gen_jpg_ecrr_plot()
    # ecrr.gen_entropy_uncompressed_plot()
    # ecrr.gen_entropy_compressed_jpg_npz_plot()

    # End the timer
    end_time = time.time()

    # Calculate and print elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: {:.2f} seconds".format(elapsed_time))


if __name__ == "__main__":
    main()
