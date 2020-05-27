import argparse
import subprocess


def download(dataset_type, split, training_only):
    """
    :arg
       - dataset_type (str):
       - split (str):
       - training_only (bool):
    """
    for dt in dataset_type:
        assert dt in ['real', 'synthetic'], f'{dt} is not a valid dataset type.'
    for sp in split:
        assert sp in ['train', 'test'], f'{sp} is not a valid split.'

    prefix = "aws s3 sync s3://rareplanes-public"

    # download images
    if training_only:
        for sp in split:
            for dt in dataset_type:
                if dt == 'real':
                    location = 'PS-RGB_tiled'
                else:
                    location = 'images'
                cmd = f"{prefix}/{dt}/{sp}/{location}/ {dt}/{sp}/{location}/"
                _ = subprocess.call(cmd.split(" "))
    else:
        for sp in split:
            for dt in dataset_type:
                cmd = f"{prefix}/{dt}/{sp}/ {dt}/{sp}/"
                _ = subprocess.call(cmd.split(" "))

    # download metadata
    for dt in dataset_type:
        cmd = f"{prefix}/{dt}/metadata_annotations {dt}/metadata_annotations"
        _ = subprocess.call(cmd.split(" "))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_type', type=str, required=True, nargs='+',
                        help='real, synthetic.')
    parser.add_argument('--split', type=str, required=True, nargs='+',
                        help='train,- test')
    parser.add_argument('--training_only', action='store_true',
                        help='only download data for model training and validation')
    args = parser.parse_args()
    download(args.dataset_type, args.split, args.training_only)
