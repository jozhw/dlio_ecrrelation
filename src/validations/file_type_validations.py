from typing import List


def validate_compressed_file_type(
    accepted_file_types: List[str], compressed_file_types: List[str]
):
    for compressed_file_type in compressed_file_types:
        if compressed_file_type not in accepted_file_types:
            raise ValueError(
                f"Invalid file type - {compressed_file_type}. Accepted file types are: {', '.join(accepted_file_types)}"
            )
