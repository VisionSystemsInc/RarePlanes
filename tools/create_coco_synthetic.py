import argparse
import glob
import json
import logging
import os

import cv2
import numpy as np
import pandas as pd

from rareplanes.xmls import parse_xml_image, get_polygon


def create_coco_annotations(data_dir, segmentation, output_path, category_attribute):
    """ parse the geojson files and create the coco annotations file
    Args:
        - image_dir (str): directory containing the tiled images
        - geojson_dir (str): directory containing the geojson files
        - output_path (str): json file containing the coco annotations
        - category_attribute (str):
    Returns
        - annotations (list): list of coco annotations
    """
    # load the conversion table. we can get the planes attributes from their names
    conversion_table = pd.read_csv('synthetic_to_observed_conversion_table.csv')

    # here we decide of the mapping
    if category_attribute is None:
        categories = [{'id': 1, 'name': 'aircraft'}]
    else:
        categories = set(conversion_table[category_attribute])
        categories = [{'id': i, 'name': n} for i, n in enumerate(categories)]
        cat2id = {k['name']: k['id'] for k in categories}
        make2id = {'_'.join(make.split(' ')): cat2id[cat] for make, cat in
                   zip(conversion_table['reverie_make'], conversion_table[category_attribute]) if isinstance(make, str)}

    logger = logging.getLogger(__name__)
    assert segmentation in ['none', 'simple', 'full'], 'Wrong segmentation type.'

    xml_paths = glob.glob(data_dir + '/*.xml')
    logger.info(f'Now processing {len(xml_paths)} files')

    ann_id = 0
    images = []
    annotations = []
    for i, path in enumerate(xml_paths):
        # get path of corresponding image and mask
        im_path = path.replace('xml', 'png')
        mask_path = path.replace('.xml', '_mask.png')
        if not os.path.isfile(im_path):
            logger.info(f'Missing image for {os.path.basename(path)} file')
            continue
        if not os.path.isfile(mask_path):
            logger.info(f'Missing mask for {os.path.basename(path)} file')
            continue

        # parse the xml file
        df = parse_xml_image(path)

        if df is None:
            continue

        # get the bboxes
        bboxes = np.array([df['xmin'], df['xmax'], df['ymin'], df['ymax']]).transpose()

        # get the segmentation
        colors = None
        if segmentation == 'simple':
            polygons = df['segmentation']
        elif segmentation == 'full':
            mask = cv2.imread(mask_path)[..., ::-1]
            colors = df['object_mask_color_rgba']

        # create images metadata
        width, height = 1920, 1080  # default resolution of the synthetic images
        im_name = os.path.basename(path)
        im_id = i+1
        image_dic = {'width': width,
                     'height': height,
                     'file_name': im_name,
                     'date_captured': None,
                     'coco_url': None,
                     'flickr_url': None,
                     'license': None,
                     'id': im_id}
        images.append(image_dic)

        # create the annotations
        for idx, bb, in enumerate(bboxes):
            # get the plane make
            make = df['make'][idx]
            cat_id = 1 if category_attribute is None else make2id[make]

            x1, x2, y1, y2 = bb.tolist()
            ann_dic = {'bbox': [x1, y1, x2 - x1, y2 - y1],
                       'area': (x2 - x1) * (y2 - y1),
                       'category_id': cat_id,
                       'image_id': im_id,
                       'iscrowd': 0,
                       'id': ann_id
                       }
            if segmentation == 'simple':
                ann_dic['segmentation'] = [polygons[idx]]
            elif segmentation == 'full':
                color = colors[idx]
                seg = get_polygon(color, mask)
                ann_dic['segmentation'] = [seg]
            ann_id += 1
            annotations.append(ann_dic)

    coco = {}
    coco['images'] = images
    coco['annotations'] = annotations
    coco['categories'] = categories
    with open(output_path, 'w') as f:
        json.dump(coco, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', required=True)
    parser.add_argument('--segmentation', default='none',
                        help='Type of segmentation, choose between none, simple or full')
    parser.add_argument('--output_path', default='instances.json',
                        help='json file path')
    parser.add_argument('--category_attribute', default=None)
    args = parser.parse_args()
    create_coco_annotations(args.image_dir,
                            args.category_attribute,
                            args.preset_categories)
