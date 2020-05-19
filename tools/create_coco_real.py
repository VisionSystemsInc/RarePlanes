import argparse
import json

from solaris.data.coco import geojson2coco


def create_coco_annotations(image_dir, geojson_dir, output_path, category_attribute, preset_categories):
    """ parse the geojson files and create the coco annotations file
    Args:
        - image_dir (str): directory containing the tiled images
        - geojson_dir (str): directory containing the geojson files
        - output_path (str): json file containing the coco annotations
        - category_attribute (str):
        - preset_categories (str):
    Returns
        - annotations (list): list of coco annotations
    """
    _ = geojson2coco(image_dir,
                     geojson_dir,
                     output_path=output_path,
                     image_ext='.png',
                     category_attribute=category_attribute,
                     preset_categories=preset_categories,
                     verbose=1)

    # rename the category to aircraft instead of other
    if category_attribute is None:
        with open(output_path, 'r') as f:
            coco = json.load(f)

        coco['categories'] = [{'id': 1, 'name': 'aircraft'}]
        with open(output_path, 'w') as f:
            json.dump(coco, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', required=True)
    parser.add_argument('--geojson_dir', required=True)
    parser.add_argument('--output_path', default='instances.json')
    parser.add_argument('--category_attribute', default=None)
    parser.add_argument('--preset_categories', default=None)
    args = parser.parse_args()
    create_coco_annotations(args.image_dir,
                            args.geojson_dir,
                            args.output_path,
                            args.category_attribute,
                            args.preset_categories)
