import matplotlib.pyplot as plt
import pandas as pd


def generate_entropy_compressed_jpg_npz_plot(
    results_path: str, path_to_save_results_plot: str
):

    df = pd.read_csv(results_path)

    entropy = df["entropy"]
    npz_compressed_size = df["npz_compressed_image_size"]
    jpg_compressed_size = df["jpg_compressed_image_size"]
    jpg_npz_compressed_size_ratio = jpg_compressed_size / npz_compressed_size
    num_rows: int = df.shape[0]

    plt.figure(figsize=(12, 8))
    plt.scatter(entropy, jpg_npz_compressed_size_ratio, color="blue", alpha=0.5)
    plt.title(
        "Entropy vs. JPG/NPZ Compressed Size Ratio for {} of JPEG Images in ImageNet".format(
            num_rows
        )
    )
    plt.xlabel("entropy")
    plt.ylabel("JPG/NPZ Compressed Size Ratio")
    plt.grid(True)

    plt.savefig(
        "{}/entropy_compressed_jpg_npz_plot.png".format(path_to_save_results_plot)
    )

    plt.show()
