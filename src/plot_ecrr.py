import os
import re

import matplotlib.pyplot as plt
import pandas as pd

RESULTS_PATH = "./results/polaris/data/2024-03-26/results.csv"
PLOTS_PATH = "./results/polaris/plots"

df = pd.read_csv(RESULTS_PATH)

# create a dir with date under plots
pattern: str = r"\b\d{4}-\d{2}-\d{2}\b"

date: str = re.findall(pattern, RESULTS_PATH)[0]

path_to_plot_save: str = "{}/{}".format(PLOTS_PATH, date)

os.makedirs(path_to_plot_save, exist_ok=True)

entropy = df["entropy"]
compression_ratio = df["compression_ratio"]
num_rows = df.shape[0]

plt.figure(figsize=(8, 6))
plt.scatter(entropy, compression_ratio, color="blue", alpha=0.5)
plt.title("Entropy vs. Compression Ratio for {} Images in ImageNet".format(num_rows))
plt.xlabel("entropy")
plt.ylabel("compression_ratio")
plt.grid(True)

plt.savefig("{}/entropy_compression_plot.png".format(path_to_plot_save))

plt.show()
