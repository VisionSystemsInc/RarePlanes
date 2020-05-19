# DATASETS

## Datasets
Rareplanes consists in two datasets: one dataset of observed satellite images ("real") and one dataset of computer 
generated images ("synthetic"). 

## S3 structure

The structure of the s3 bucket `rareplanes-public` is detailed in the user guide available here.
 [INSERT LINK TO USER GUIDE]

## Prerequisites
* install the [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
* run `aws configure`

## Download datasets

Download all the data using the command below. Both real and synthetic datasets account for over 500 GB
of data, so this command will take a while. 
```
python download_data.py --dataset_type real synthetic --split train test
```

If you only need data for training object detection algorithms, the command below will only pull 
the 512x512 observed tiles and the synthetic images.
```
python download_data.py --dataset_type real synthetic --split train test --training_only
```

You can also download any data of interest by using directly the AWS CLI. For example, the command 
below will only download the full resolution satellite images:
```
aws s3 sync s3://rareplanes-public/real/train/PS-RGB/ real/train/PS-RGB/ 
```
