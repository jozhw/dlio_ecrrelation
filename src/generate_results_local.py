# with root dir as the working dir
import os
import sys
import time

from mpi4py import MPI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ecrr.ecr_relation import ECrRelation

REMOVE_FROM_DIR = "./assets/local/compressed_imgs"
EXTENSIONS = [".jpg", ".npz"]


def main():
    # init MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # path to json file
    JSON_FILE = "assets/local/img_paths/2024-04-01/local_rand_200.json"

    ecrr = ECrRelation(JSON_FILE, "local", ["npz", "jpg"])

    ecrr.load_data()

    start_time = time.time()

    ecrr.calculate()

    ecrr.save_to_csv()

    # synchronize processes
    comm.Barrier()

    # only root process (rank 0) prints the elapsed time
    if rank == 0:
        end_time = time.time()

        elapsed_time = end_time - start_time
        print("Elapsed time for parallel: {:.2f} seconds".format(elapsed_time))

        ecrr.remove_compressed_images(REMOVE_FROM_DIR, EXTENSIONS)

    MPI.Finalize()


if __name__ == "__main__":
    main()
