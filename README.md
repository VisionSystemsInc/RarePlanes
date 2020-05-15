# RarePlanes

This repository contains scripts for inspection, preparation and evaluation of the RarePlanes dataset. 

Details are available at [LINK TO USER GUIDE].

## Paper

[PAPER LINK HERE]

Please cite our paper if you find it useful for your research.


## Getting Started

### Using docker

We highly recommend using the available docker image as some of the dependencies can be strenous 
to install.

` docker pull aireverie/rareplanes:latest`


### Without docker

Follow the installation guidelines of [solaris](https://github.com/CosmiQ/solaris). 

## Download data

Instructions are available in the user guide and [here](datasets/README.md).


## Create tiles from satellite images
```
test
```
## Create coco files

Using the `create_coco.py` script, the user can select the attribute that he wants to use as a category.

### For aircraft detection

For example, to create a coco file where each object is labeled as aircraft, the following script is ran:
```
python tools/create_coco.py --image_dir datasets/observed/train/PS-RGB_tiled
                            --geojson_dir datasets/observed/train/geojson_aircraft_tiled
```

### For other attributes
If we want to classify the aircraft by number of engines instead:
```
python tools/create_coco.py --image_dir datasets/observed/train/PS-RGB_tiled
                            --geojson_dir datasets/observed/train/geojson_aircraft_tiled
                            --category_attribute num_engines
```

### With preset categories

```
python tools/create_coco.py --image_dir datasets/observed/train/PS-RGB_tiled
                            --geojson_dir datasets/observed/train/geojson_aircraft_tiled
                            --category_attribute role
                            --preset_categories
```

## Authors

* **Thomas Hossler** 
* **Jake Shermeyer**

