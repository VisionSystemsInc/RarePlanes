import argparse

from rareplanes.tiles import rareplanes_tiler


def create_tiles(untiled_image_dir,
                 untiled_geojson_dir,
                 image_tiles_out_dir,
                 geojson_tiles_out_dir,
                 tile_size,
                 overlap,
                 min_obj_area_m,
                 min_obj_perc):
    """ wrapper of the tiler function """
    rareplanes_tiler(untiled_image_dir,
                     untiled_geojson_dir,
                     image_tiles_out_dir,
                     geojson_tiles_out_dir,
                     tile_size=tile_size,
                     overlap=overlap,
                     min_obj_area_m=min_obj_area_m,
                     min_obj_perc=min_obj_perc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, required=True,
                        help='directory containing the satellite images')
    parser.add_argument('--geojson_dir', type=str, required=True,
                        help='directory containing the geojson files')
    parser.add_argument('--tile_image_dir', type=str, required=True,
                        help='output directory for the tiles')
    parser.add_argument('--tile_geojson_dir', type=str, required=True,
                        help='output directory for the geojson tiles')
    parser.add_argument('--tile_size', type=int, default=512,
                        help='dimensions of the tiles')
    parser.add_argument('--overlap', type=float, default=0.1,
                        help='overlap between adjacent tiles')
    parser.add_argument('--min_area', type=float, default=100,
                        help='minimum area of bbox')
    parser.add_argument('--min_ratio', type=float, default=0.2,
                        help='minimum ratio of bbox area when tiled')
    args = parser.parse_args()
    create_tiles(args.image_dir,
                 args.geojson_dir,
                 args.tile_image_dir,
                 args.tile_geojson_dir,
                 args.tile_size,
                 args.overlap,
                 args.min_area,
                 args.min_ratio)
