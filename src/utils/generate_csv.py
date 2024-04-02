import csv
import os
from typing import List, Mapping, Optional

from mpi4py import MPI


def gather_results(
    comm: MPI.Comm, results: Mapping[str, Mapping[str, float]]
) -> List[Optional[Mapping[str, Mapping[str, float]]]]:
    """
    Gather results from all processes onto the root process.

    Args:
        comm: MPI communicator.
        results: Local results from each process.

    Returns:
        List of results gathered on the root process.
    """
    rank = comm.Get_rank()
    if rank == 0:
        gathered_results: List[Optional[Mapping[str, Mapping[str, float]]]] = [results]
        for i in range(1, comm.Get_size()):
            gathered_results.append(comm.recv(source=i))
        return gathered_results
    else:
        comm.send(results, dest=0)
        return []


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

    gathered_results = gather_results(comm, results)

    if rank == 0:
        field_names = list(results[next(iter(results))].keys())
        field_names.insert(0, "file_name")

        csv_file = os.path.join(save_path, fname)

        with open(csv_file, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=field_names,
            )

            writer.writeheader()

            for gathered_result in gathered_results:
                if gathered_result is not None:  # Check for None
                    for file_name, values in gathered_result.items():
                        row_data = {"file_name": file_name}
                        row_data.update(
                            {key: str(value) for key, value in values.items()}
                        )
                        writer.writerow(row_data)

        if gathered_results and any(
            gathered_results
        ):  # Check if any non-None value exists
            print("Data saved to", csv_file)
