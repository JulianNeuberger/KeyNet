import os

import numpy
from PIL import Image

processed_images_dir = os.path.join('C:\\', 'workspace', 'KeyNet', 'data', 'img', 'processed')
valid_directories = ['qLSuLZD']
invalid_directories = ['EuTp2eO']  # 'TYBDakN', '4g2jIUE'


def get_all():
    x = []
    y = []
    for valid_dir in valid_directories:
        valid_image_dir = os.path.join(processed_images_dir, valid_dir)
        for file_name in os.listdir(valid_image_dir):
            if not os.path.isdir(file_name):
                image = Image.open(os.path.join(valid_image_dir, file_name))
                pixels = image.getdata()
                pixels = numpy.array(pixels)
                pixels = numpy.reshape(pixels, (500, 500, 3))
                x.append(pixels)
                y.append([0, 1])

    for invalid_dir in valid_directories:
        invalid_image_dir = os.path.join(processed_images_dir, invalid_dir)
        for file_name in os.listdir(invalid_image_dir):
            if not os.path.isdir(file_name):
                image = Image.open(os.path.join(invalid_image_dir, file_name))
                pixels = image.getdata()
                pixels = numpy.array(pixels)
                pixels = numpy.reshape(pixels, (500, 500, 3))
                x.append(pixels)
                y.append([1, 0])

    return numpy.array(x), numpy.array(y)
