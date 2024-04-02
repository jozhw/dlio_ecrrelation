import matplotlib.pyplot as plt
import pandas as pd


def generate_npz_ecrr_plot(results_path: str, path_to_save_results_plot: str):

    df = pd.read_csv(results_path)

    entropy = df["entropy"]
    compression_ratio = df["npz_compression_ratio"]
    num_rows = df.shape[0]

    plt.figure(figsize=(12, 8))
    plt.scatter(entropy, compression_ratio, color="blue", alpha=0.5)
    plt.title(
        "Entropy vs. Compression Ratio for {} NPZ Compressed Images".format(num_rows)
    )
    plt.xlabel("entropy")
    plt.ylabel("compression_ratio")
    plt.grid(True)

    plt.savefig(
        "{}/npz_entropy_compression_ratio_plot.png".format(path_to_save_results_plot)
    )

    plt.show()


def generate_jpg_ecrr_plot(results_path: str, path_to_save_results_plot: str):

    df = pd.read_csv(results_path)

    entropy = df["entropy"]
    compression_ratio = df["jpg_compression_ratio"]
    num_rows = df.shape[0]

    plt.figure(figsize=(12, 8))
    plt.scatter(entropy, compression_ratio, color="blue", alpha=0.5)
    plt.title(
        "Entropy vs. Compression Ratio for {} JPG Compressed Images".format(num_rows)
    )
    plt.xlabel("entropy")
    plt.ylabel("jpg_compression_ratio")
    plt.grid(True)

    plt.savefig(
        "{}/jpg_entropy_compression_ratio_plot.png".format(path_to_save_results_plot)
    )

    plt.show()
