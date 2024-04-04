# with root dir as the working dir
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from plotting.generate_ecrr_combined_plot import generate_combined_npz_ecrr_plot

POLARIS_RESULTS_PATH = "./results/polaris/data/2024-04-03/results.csv"
LOCAL_RESULTS_PATH = "./results/local/data/2024-04-02/results.csv"
SAVE_PLOT_PATH = "./results/combined/plots/2024-04-03"


def main():

    start_time = time.time()

    generate_combined_npz_ecrr_plot(
        POLARIS_RESULTS_PATH, SAVE_PLOT_PATH, LOCAL_RESULTS_PATH
    )

    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Elapsed time: {:.2f} seconds".format(elapsed_time))


if __name__ == "__main__":
    main()
