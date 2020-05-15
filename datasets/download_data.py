import argparse
import subprocess


def download(dataset_type, split, tiles_only):
    """
    :arg
       - dataset_type (str):
       - split (str):
       - tiles_only (bool):
    """
    assert dataset_type in ['all', 'real', 'synthetic'], 'Wrong dataset type'
    assert split in ['all', 'train', 'test']

    prefix = "aws s3 sync s3://rareplanes-public"
    # literally downloads all the available data. Be patient.
    if dataset_type == 'all':
        cmd = f"{prefix} ."
        _ = subprocess.call(cmd.split(" "))
    else:
        if tiles_only:
            cmd = f"{prefix}/{dataset_type}/{split}/PS-RGB_tiled/ {dataset_type}/{split}/PS-RGB_tiled/"
            _ = subprocess.call(cmd.split(" "))
            cmd = f"{prefix}/{dataset_type}/{split}/geojson_aircraft_tiled/ {dataset_type}/{split}/geojson_aircraft_tiled"
            _ = subprocess.call(cmd.split(" "))
        else:
            cmd = f"{prefix}/{dataset_type}/{split}/ ."
            _ = subprocess.call(cmd.split(" "))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_type', type=str, default='all',
                        help='either all, real or synthetic.')
    parser.add_argument('--split', type=str, default='all',
                        help='either train, test or all')
    parser.add_argument('--tiles_only', action='store_true',
                        help='only download data for model training and validation')
    args = parser.parse_args()
    download(args.dataset_type, args.split, args.tiles_only)
