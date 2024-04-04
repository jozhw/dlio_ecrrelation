import matplotlib.pyplot as plt
import pandas as pd


def generate_combined_npz_ecrr_plot(
    polaris_results_path: str, path_to_save_results_plot: str, local_results_path: str
):

    polaris_df = pd.read_csv(polaris_results_path)
    local_df = pd.read_csv(local_results_path)

    num_rows = polaris_df.shape[0] + local_df.shape[0]

    plt.figure(figsize=(12, 8))
    plt.scatter(
        polaris_df["entropy"],
        polaris_df["npz_compression_ratio"],
        color="blue",
        alpha=0.5,
        label="Polaris Compression Ratios",
    )

    # local scatter plot
    plt.scatter(
        local_df["entropy"],
        local_df["npz_compression_ratio"],
        color="red",
        alpha=0.5,
        label="Local Compression Ratios",
    )

    plt.title(
        "Entropy vs. Compression Ratio for {} NPZ Compressed Images for Local and Polaris".format(
            num_rows
        )
    )
    plt.xlabel("entropy")
    plt.ylabel("compression_ratio")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        "{}/npz_combined_entropy_compression_ratio_plot.png".format(
            path_to_save_results_plot
        )
    )

    plt.show()
