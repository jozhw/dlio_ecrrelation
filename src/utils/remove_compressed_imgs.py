import os


def remove_compressed_imgs(file_path: str):
    try:
        os.unlink(file_path)
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")
