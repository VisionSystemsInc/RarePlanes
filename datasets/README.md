# DATASETS

## Datasets
Rareplanes consists in two datasets: one dataset of observed satellite images ("real") and one dataset of computer 
generated images ("synthetic")

## Prerequisites
* install [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
* run `aws configure`

## Download datasets

Download all the data using:
```
python download_data.py
```

Only download tiled data:
```
python download_data.py --dataset_type real --split train --tiles_only
```

