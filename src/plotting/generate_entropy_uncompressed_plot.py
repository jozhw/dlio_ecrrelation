import matplotlib.pyplot as plt
import pandas as pd


def generate_entropy_uncompressed_plot(
    results_path: str, path_to_save_results_plot: str
):

    df = pd.read_csv(results_path)

    entropy = df["entropy"]
    uncompressed_size = df["uncompressed_size"]
    num_rows = df.shape[0]

    plt.figure(figsize=(12, 8))
    plt.scatter(entropy, uncompressed_size, color="blue", alpha=0.5)
    plt.title(
        "Entropy vs. Uncompressed Size for {}  of JPEG Images in ImageNet".format(
            num_rows
        )
    )
    plt.xlabel("entropy")
    plt.ylabel("uncompressed_size")
    plt.grid(True)

    plt.savefig("{}/entropy_uncompressed_plot.png".format(path_to_save_results_plot))

    plt.show()
