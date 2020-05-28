# Rareplanes model weights:

## Models
We are using two models, Faster-RCNN and Mask-RCNN. The models configurations
are available [here](https://github.com/facebookresearch/detectron2/blob/master/configs/COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml) 
and [here](https://github.com/facebookresearch/detectron2/blob/master/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_1x.yaml).
  

## Codebase

We are using the [Detectron2](https://github.com/facebookresearch/detectron2)
library for our experiments. Using the weights file and the `COCOEvaluator` class of
the detectron2, one can replicate the results of the paper.

## Performances   

[NEED TO ADD URLS]

### Faster RCNN

| Name        | Attribute | box AP | download |
|-------------|-----------|:------:|:--------:|
| real        | aircraft  |   0.0  |   model  |
| synthetic   | aircraft  |   0.0  |   model  |
| fine_tuning | aircraft  |   0.0  |   model  |
| real        | role      |   0.0  |   model  |
| synthetic   | role      |   0.0  |   model  |
| fine_tuning | role      |   0.0  |   model  |

### Mask RCNN

| Name        | Attribute | box AP | mask AP | download |
|-------------|-----------|:------:|:-------:|:--------:|
| real        | aircraft  |   0.0  |   0.0   |   model  |
| synthetic   | aircraft  |   0.0  |   0.0   |   model  |
| fine_tuning | aircraft  |   0.0  |   0.0   |   model  |
| real        | role      |   0.0  |   0.0   |   model  |
| synthetic   | role      |   0.0  |   0.0   |   model  |
| fine_tuning | role      |   0.0  |   0.0   |   model  |