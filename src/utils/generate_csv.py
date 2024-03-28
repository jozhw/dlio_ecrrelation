import csv
import os
from typing import List, Mapping


def generate_csv(
    save_path: str, fname: str, results: Mapping[str, Mapping[str, float]]
):
    # extract field names
    field_names: List[str] = list(results[next(iter(results))].keys())
    field_names.insert(0, "file_name")
    # save to csv file
    csv_file: str = os.path.join(save_path, fname)

    # write to csv_file
    with open(csv_file, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=field_names,
        )

        writer.writeheader()
        for file_name, values in results.items():
            row_data = {"file_name": file_name}
            row_data.update({key: str(value) for key, value in values.items()})
            writer.writerow(row_data)

    print("Data saved to", csv_file)
