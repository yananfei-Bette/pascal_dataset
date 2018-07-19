# several python code for pascal dataset processing

## prepare_car_image_crop_without_padding.py

Choose car image and crop them into 300 by 300

## mxl2png.py

This is used for scribble segmentation. The label dataset link is [here](https://www.dropbox.com/s/9vh3kvtd742red8/scribble_annotation.zip?dl=0#).

Also **xml.etree.ElementTree** is used to paser xml file and [**Bresnham algorithm**](http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python) is taken to draw lines.

A sample from PASCAL Dataset.

![orignial image](https://github.com/yananfei-Bette/pascal_dataset/blob/master/image/ori.jpg)

The demo given by [paper](https://arxiv.org/pdf/1604.05144.pdf).

![label](https://github.com/yananfei-Bette/pascal_dataset/blob/master/image/demo.jpg)

My result.

![result](https://github.com/yananfei-Bette/pascal_dataset/blob/master/image/demo_.png)
