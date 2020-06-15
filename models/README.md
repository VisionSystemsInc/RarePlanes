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

### Faster RCNN

| Name        | Attribute | box mAP | download |
|-------------|-----------|:------:|:--------:|
| real        | aircraft  |   73.32  |   [model](https://rareplanes-public.s3.amazonaws.com/weights/fasterrcnn/real/aircraft/model_0043999.pth)  |
| synthetic   | aircraft  |   54.86  |   [model](https://rareplanes-public.s3.amazonaws.com/weights/fasterrcnn/synthetic/aircraft/model_0077999.pth)  |
| fine_tuning | aircraft  |   69.16  |   [model](https://rareplanes-public.s3.amazonaws.com/weights/fasterrcnn/finetune/aircraft/model_0079999.pth)  |
| real        | role      |   68.21  |   [model](https://rareplanes-public.s3.amazonaws.com/weights/fasterrcnn/real/role/model_0023999.pth)  |
| synthetic   | role      |   35.88  |   [model](https://rareplanes-public.s3.amazonaws.com/weights/fasterrcnn/synthetic/role/model_0021999.pth)  |
| fine_tuning | role      |   63.10  |   [model](https://rareplanes-public.s3.amazonaws.com/weights/fasterrcnn/finetune/role/model_0024999.pth)  |

### Mask RCNN

| Name        | Attribute | mask mAP | download |
|-------------|-----------|:-------:|:--------:|
| real        | aircraft  |  73.67   |   [model](https://rareplanes-public.s3.amazonaws.com/weights/maskrcnn/real/aircraft/model_0033999.pth)  |
| synthetic   | aircraft  |  56.28   |   [model](https://rareplanes-public.s3.amazonaws.com/weights/maskrcnn/synthetic/aircraft/model_0049999.pth)  |
| fine_tuning | aircraft  |  70.51   |   [model](https://rareplanes-public.s3.amazonaws.com/weights/maskrcnn/finetune/aircraft/model_0053999.pth)  |
| real        | role      |  69.57   |   [model](https://rareplanes-public.s3.amazonaws.com/weights/maskrcnn/real/role/model_0027999.pth)  |
| synthetic   | role      |  39.46   |   [model](https://rareplanes-public.s3.amazonaws.com/weights/maskrcnn/synthetic/role/model_0043999.pth)  |
| fine_tuning | role      |  67.11   |   [model](https://rareplanes-public.s3.amazonaws.com/weights/maskrcnn/finetune/role/model_0045999.pth)  |