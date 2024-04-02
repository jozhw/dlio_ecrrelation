# with root dir as the working dir
import os
import sys
import time

from mpi4py import MPI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ecrr.ecr_relation import ECrRelation


def main():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # path to json file

    JSON_FILE: str = "assets/polaris/img_paths/2024-03-26/imagenet_rand_5000.json"

    # Create an instance of ECrRelation
    ecrr = ECrRelation(JSON_FILE, "local", ["npz", "jpg"])

    # Load data
    ecrr.load_data()

    # Start the timer
    start_time = time.time()

    # Run the calculate function in parallel
    ecrr.calculate()

    # Save results
    ecrr.save_to_csv()

    # Synchronize processes
    comm.Barrier()

    # Only root process (rank 0) prints the elapsed time
    if rank == 0:
        # End the timer
        end_time = time.time()

        # Calculate and print elapsed time
        elapsed_time = end_time - start_time
        print("Elapsed time for parallel: {:.2f} seconds".format(elapsed_time))

    # Finalize MPI
    MPI.Finalize()


if __name__ == "__main__":
    main()
