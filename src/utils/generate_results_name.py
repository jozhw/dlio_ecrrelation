import re

"""
Returns the file name with extension for the result csv file.
"""


def generate_results_name(path: str) -> str:
    regex_pattern: str = r"\/([^\/]+)\.json$"
    match = re.search(regex_pattern, path)
    if match:
        fname: str = "results_" + match.group(1) + ".csv"
        return fname
    else:
        raise ValueError("No name found from json image path file.")
