import glob
import os
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon
from PIL import Image

from rareplanes.xmls import parse_xml_image, get_polygon


class Visualizer:

    def __init__(self, data_dir, segmentation='none', figsize=(15, 10)):
        """ load the data in data_dir and create observation triplets"""
        xmls = glob.glob(os.path.join(data_dir, 'xmls') + '/*.xml')
        # create triplets xml, image, mask
        self.data = []
        for path in xmls:
            xml_name = os.path.basename(path)
            im_name = xml_name.replace('xml', 'png')
            mask_name = xml_name.replace('.xml', '_mask.png')
            im_path = os.path.join(data_dir, 'images', im_name)
            mask_path = os.path.join(data_dir, 'masks', mask_name)
            if os.path.isfile(im_path) and os.path.isfile(mask_path):
                self.data.append([path, im_path, mask_path])
        print(f'{data_dir} contains {len(self.data)} valid observations')
        self.figsize = figsize
        self.segmentation = segmentation

    def display(self, index):
        """ display a particular observation using its index """
        self._plot(self.data[index])

    def display_random(self, n=10):
        """ display N random samples from data"""
        for _ in range(n):
            sample = random.choice(self.data)
            self._plot(sample)

    def _plot(self, observation):
        """ plot single image """
        xmlpath, impath, maskpath = observation
        image = Image.open(impath)
        mask = np.array(Image.open(maskpath))
        df = parse_xml_image(xmlpath)

        # get bboxes
        bboxes = np.array([df['xmin'], df['ymin'], df['xmax'], df['ymax']]).transpose()

        # plot
        f, ax = plt.subplots(1, figsize=self.figsize)
        ax.imshow(image)
        for idx, bb in enumerate(bboxes):
            x1, y1, w, h = bb[0], bb[1], bb[2]-bb[0], bb[3]-bb[1]
            rec = Rectangle((x1, y1), w, h, facecolor='none', edgecolor='r', linewidth=2)
            ax.add_patch(rec)
            if self.segmentation == 'simple':
                polygon = np.array(df['segmentation'][idx])
                polygon = polygon.reshape(int(len(polygon) / 2), 2)
                poly = Polygon(polygon, edgecolor='b', alpha=0.5, linewidth=2)
                ax.add_patch(poly)
            elif self.segmentation == 'full':
                color = df['object_mask_color_rgba'][idx]
                polygon = np.array(get_polygon(color, mask))
                polygon = polygon.reshape(int(len(polygon) / 2), 2)
                poly = Polygon(polygon, edgecolor='b', alpha=0.5, linewidth=2)
                ax.add_patch(poly)
        plt.title(os.path.basename(xmlpath))
        plt.axis('off')
        plt.show()







