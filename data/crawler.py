import json
from collections import namedtuple
import os
from typing import List

import requests
import time


class ImageDao:
    def __init__(self, url, data, name, extension):
        self.url = url
        self.data = data
        self.name = name
        self.extension = extension


class Crawler:
    def crawl(self) -> List[ImageDao]:
        raise NotImplementedError

    @staticmethod
    def persist(image: ImageDao):
        os.makedirs('img', exist_ok=True)
        with open(os.path.join('img', image.name + image.extension), mode='wb') as file:
            file.write(image.data)

    def run(self):
        images = self.crawl()
        for image in images:
            self.persist(image)


class ImgurCrawler(Crawler):
    gallery_base = 'https://imgur.com/ajaxalbums/getimages/{}/hit.json'
    image_base = 'https://i.imgur.com/{}{}'

    def crawl(self) -> List[ImageDao]:
        gallery_id = 'EFqYnTc'
        print('Loading images from gallery {}'.format(gallery_id))
        gallery_url = ImgurCrawler.gallery_base.format(gallery_id)
        gallery_info = requests.request('get', gallery_url, params={'all': True})
        print('Request finished with status {}'.format(gallery_info.status_code))
        if gallery_info.status_code == requests.codes.OK:
            gallery_info = json.loads(gallery_info.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            gallery_info = gallery_info.data
            print('Request ok, fetching {} images...'.format(gallery_info.count))
            seconds_per_image = 0
            ret = []
            for index, image in enumerate(gallery_info.images):
                start = time.time()
                ret.append(self.crawl_single_image(image))
                time_took = time.time() - start
                seconds_per_image = (seconds_per_image * index + time_took) / (index + 1)
                eta = seconds_per_image * (gallery_info.count - index)
                print('Fetched image {} in {:.3f} seconds, eta {:.1f} seconds'.format(
                    image.hash,
                    time_took,
                    eta
                ))
            return ret

    @staticmethod
    def crawl_single_image(image):
        return ImageDao(
            url=ImgurCrawler.image_base.format(image.hash, image.ext),
            name=image.hash,
            extension=image.ext,
            data=requests.request('get', ImgurCrawler.image_base.format(image.hash, image.ext)).content
        )


ImgurCrawler().run()
