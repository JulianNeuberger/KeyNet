import os
from PIL import Image


def down_sample_image(image: Image, width: int, height: int):
    return image.resize((width, height), Image.ANTIALIAS)


def pre_process_data(data_raw_dir: str, data_processed_dir: str):
    handle_dir(data_raw_dir, '', data_processed_dir)


def handle_dir(data_root, relative_path, save_root):
    for root, dirs, files in os.walk(os.path.join(data_root, relative_path)):
        print("Currently processing directory {} in {}".format(relative_path, data_root))
        image_names = [file for file in files if file.endswith('jpg')]
        for image_name in image_names:
            image = Image.open(os.path.join(root, image_name))
            width, height = 500, 500
            image = down_sample_image(image, width, height)
            current_save_dir = os.path.join(save_root, relative_path)
            os.makedirs(current_save_dir, exist_ok=True)
            image.save(os.path.join(current_save_dir, image_name))
        for directory in dirs:
            print("Stepping down into dir {}".format(directory))
            handle_dir(data_root, os.path.join(relative_path, directory), save_root)


def get_image_size_preserve_ratio(image: Image, width: int = -1, height: int = -1):
    if width is not -1:
        org_width, org_height = image.size
        return width, int(org_height / (org_width / width))
    else:
        org_width, org_height = image.size
        return int(org_width / (org_height / height)), height


pre_process_data('C:\\workspace\\KeyNet\\data\\img\\raw', 'C:\\workspace\\KeyNet\\data\\img\\processed')
