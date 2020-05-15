import glob
import os

import gdal
import geopandas as gpd
from shapely.geometry import box
from tqdm import tqdm

from solaris.tile.vector_tile import clip_gdf
from solaris.vector.polygon import convert_poly_coords


def rareplanes_tiler(untiled_image_dir,
                     untiled_geojson_dir,
                     image_tiles_out_dir,
                     geojson_tiles_out_dir,
                     tile_size=512,
                     overlap=0.2,
                     min_obj_area_m=100,
                     min_obj_perc=0.25):
    """Function to tile a set of images into smaller square chunks with embedded georeferencing info
    allowing an end user to specify the size of the tile, the overlap of each tile, and when to discard
    a tile if it contains blank datasets.
    :arg
        - untiled_image_dir (str): directory contained full untiled satellite images
        - untiled_geojson_dir (str): directory for full untiled geojson fukes
        - image_tiles_out_dir (str): output directory for tiled imagery.
        - geojson_tiles_out_dir (str): output directory for tiled geojson files
        - tile_size (int): tile height and width
        - overlap (float): amount of overlap of each tile in float format.  Should range between 0 and <1.
        - min_obj_area_m (float): minimum area in m^2 of truncated object to be keep as a valid annotation
        - min_obj_perc (float): minimum visible ratio of truncated object to be keep as a valid annotatio.
         Should range between 0 and 1.
    """
    # some hardcoded stuff
    output_channels = [1, 2, 3]
    ext = ".tif"

    # create the output directories
    os.makedirs(image_tiles_out_dir, exist_ok=True)
    os.makedirs(geojson_tiles_out_dir, exist_ok=True)
    os.chdir(untiled_image_dir)

    # list the images
    images = glob.glob("*" + ext)

    tile_size = int(tile_size)
    for im in tqdm(images):
        raster = gdal.Open(os.path.abspath(im))
        geojson = os.path.join(untiled_geojson_dir, im.split(ext)[0] + ".geojson")
        in_gdf = gpd.read_file(geojson)
        in_gdf['area'] = in_gdf['geometry'].apply(lambda x: x.area)

        width = int(raster.RasterXSize)
        height = int(raster.RasterYSize)
        count = 0
        # loop through the tiles
        for i in tqdm(range(0, width, int(tile_size * (1 - overlap)))):
            for j in range(0, height, int(tile_size * (1 - overlap))):
                srcWin_chip = [i, j, tile_size, tile_size]
                bbox = box(i, j, i + tile_size, j + tile_size)
                chip = convert_poly_coords(bbox, raster_src=im)
                gdf = clip_gdf(in_gdf, chip)
                # check if there is an object in that tile
                if len(gdf) > 0:
                    gdf['new_area'] = gdf['area'] * gdf['partialDec']
                    gdf = gdf[(((gdf['partialDec'] <= min_obj_perc) &
                                (gdf['new_area'] >= min_obj_area_m)) | (gdf['partialDec'] > min_obj_perc))]
                    gdf.drop(columns=['origarea', 'origlen'], inplace=True)
                    # remove small / highly truncated objects
                    if len(gdf) > 0:
                        count += 1
                        tileout = image_tiles_out_dir + "/" + \
                            im.split(ext)[0] + "_tile_" + str(count) + ".png"
                        geojson_out = geojson_tiles_out_dir + "/" + \
                            im.split(ext)[0] + "_tile_" + str(count) + ".geojson"
                        gdf.to_file(geojson_out, driver="GeoJSON")
                        output = gdal.Translate(tileout, im, srcWin=srcWin_chip, bandList=output_channels)
                        del output
