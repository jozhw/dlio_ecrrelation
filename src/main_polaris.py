# with root dir as the working dir
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ecrr.ecr_relation import ECrRelation

# path to json file
JSON_FILE: str = "assets/polaris/img_paths/2024-03-26/imagenet_rand_5000.json"

ecrr = ECrRelation(JSON_FILE, "polaris", ["npz"])

ecrr.load_data()
ecrr.calculate()
ecrr.save_to_csv()
ecrr.gen_npz_ecrr_plot()
ecrr.gen_entropy_uncompressed_plot()
