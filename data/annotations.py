import os


def generate_empty_annotation(for_image_name: str, in_dir_path: str):
    complete_file_path = os.path.join(for_image_name, in_dir_path)
    if os.path.isfile(complete_file_path):
        pass


def generate_empty_annotations(for_dir_path: str):
    for file_name in os.listdir(for_dir_path):
        generate_empty_annotation(file_name, for_dir_path)
