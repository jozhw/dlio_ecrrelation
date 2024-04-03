import csv
import os
from typing import List, Mapping, Optional

from mpi4py import MPI


def generate_csv(
    save_path: str, fname: str, results: Mapping[str, Mapping[str, float]]
):
    """
    Write results to a CSV file.

    Args:
        save_path: Path to the directory where the CSV file will be saved.
        fname: Name of the CSV file.
        results: Mapping of file names to result dictionaries.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Each process contributes its local results to the root process
    gathered_results = comm.gather(results, root=0)

    if rank == 0:
        # Merge all gathered results into a single dictionary
        merged_results = {}
        if gathered_results is not None:
            for result in gathered_results:
                merged_results.update(result)

            field_names = list(merged_results[next(iter(merged_results))].keys())
            field_names.insert(0, "file_name")

            # Collect all rows from all processes
            all_rows = []
            for file_name, values in merged_results.items():
                row_data = {"file_name": file_name}
                row_data.update({key: str(value) for key, value in values.items()})
                all_rows.append(row_data)

            csv_file = os.path.join(save_path, fname)

            with open(csv_file, "w", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=field_names,
                )
                writer.writeheader()
                writer.writerows(all_rows)  # Write all rows in bulk

            print("Data saved to", csv_file)
