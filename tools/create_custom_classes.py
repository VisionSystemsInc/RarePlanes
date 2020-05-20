import argparse
import geopandas as gpd
import pandas as pd
import os
import glob
from tqdm import tqdm


def count_unique_index(df, by):
    return df.groupby(by).size().reset_index().rename(columns={0: 'count'})


def create_custom_classes(all_annotations_geojson, geojson_dir, output_path, category_attributes):
    """ parse the geojson files and create custom classes based upon
    unique variatons of the RarePlanes attributes.
        -all_annotations_geojson (str): The path to the
        `RarePlanes_Public_All_Annotations.geojson` file.
        - geojson_dir (str): directory containing the geojson files
        for individual images or tiles
        - output_path (str): directory to output the customized geojsons
        - category_attributes (list): A list of attributes to combine
        to create a custom class.  Choose any combintaion of the following:
        ['role','num_engines', 'propulsion', 'canards', 'num_tail_fins',
       'wing_position', 'wing_type', 'faa_wingspan_class']
    :returns
        - new geojsons with a custom_id for each combination of unique
        attributes.
        -A lookup table for each classes custom_id.
    """
    os.makedirs(output_path, exist_ok=True)
    gdf = gpd.read_file(all_annotations_geojson)
    lookup_gdf = count_unique_index(gdf, category_attributes)
    lookup_gdf['custom_id'] = list(range(1, len(lookup_gdf) + 1))
    lookup_gdf.drop(columns=['count'], inplace=True)
    lookup_gdf.to_csv(os.path.join(output_path, "custom_class_lookup.csv"))
    os.chdir(geojson_dir)
    geojsons = glob.glob("*.geojson")
    for geojson in tqdm(geojsons):
        gdf = gpd.read_file(geojson)
        gdf = pd.merge(gdf, lookup_gdf, on=category_attributes, how='left')
        gdf.to_file(os.path.join(output_path, geojson), driver="GeoJSON")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--all_annotations_geojson', required=True)
    parser.add_argument('--geojson_dir', required=True)
    parser.add_argument('--output_path', default='./')
    parser.add_argument('--category_attribute', default=['role', 'num_engines'])
    args = parser.parse_args()
    create_custom_classes(args.all_annotations_geojson,
                          args.geojson_dir,
                          args.output_path,
                          args.category_attribute)
