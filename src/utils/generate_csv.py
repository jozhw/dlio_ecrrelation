import csv
import os
from typing import Mapping

from mpi4py import MPI


def generate_csv(
    save_path: str, fname: str, results: Mapping[str, Mapping[str, float]]
):
    """
    Write results to CSV files in chunks.

    Args:
        save_path: Path to the directory where the CSV files will be saved.
        fname: Base name of the CSV files.
        results: Mapping of file names to result dictionaries.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Define chunk size
    CHUNK_SIZE = 100000

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

            # Split merged results into chunks
            chunks = [
                list(merged_results.items())[i : i + CHUNK_SIZE]
                for i in range(0, len(merged_results), CHUNK_SIZE)
            ]

            # Write each chunk to a separate CSV file
            for i, chunk in enumerate(chunks):
                csv_file = os.path.join(save_path, f"{fname}_{i}.csv")
                with open(csv_file, "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=field_names)
                    writer.writeheader()
                    for file_name, values in chunk:
                        row_data = {"file_name": file_name}
                        row_data.update(
                            {key: str(value) for key, value in values.items()}
                        )
                        writer.writerow(row_data)

                print(f"Chunk {i+1} saved to {csv_file}")
