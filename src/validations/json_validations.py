import re


def validate_json_img_path(regex_date_pattern: str, json_img_path: str):
    if not re.match(regex_date_pattern, json_img_path):
        raise ValueError(
            """
            Invalid input for json_img_path. The path does not contain date
            in YYYY-MM-DD format
            """
        )


def validate_json_extension(json_img_path: str):
    image_path_type = json_img_path.split(".")[-1].lower()
    if image_path_type != "json":
        raise ValueError(
            "json_img_path is supposed to be a json file, but got {}".format(
                image_path_type
            )
        )
