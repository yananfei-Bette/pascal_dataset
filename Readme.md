# several python code for pascal dataset processing

## prepare_car_image_crop_without_padding.py

Choose car image and crop them into 300 by 300

## mxl2png.py

This is used for scribble segmentation. The label dataset link is [here]. (https://www.dropbox.com/s/9vh3kvtd742red8/scribble_annotation.zip?dl=0#)

Also **xml.etree.ElementTree** is used to paser xml file and [**Bresnham algorithm**] is taken to draw lines. (http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python)

![orignial image](image\ori.jpg)

![label](image\demo.jpg)

![result](image\demo_.png)