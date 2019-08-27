# EMedAI

## object detect and crop 
This folder mainly crops and processes the image after detecting PMS's front part.

The code is [object_detection_and_crop.ipynb](https://github.com/kristine4658/EMedAI/blob/master/object%20detect%20and%20crop/object_detection_and_crop.ipynb), 
which is a modified version of [object_detection_tutorial.ipynb](https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb).
I just added few parts from the original code to extract characters from images more conveniently.
If you already trained data with model and have graph to use for object detection, place the file to 'models/research/object_detection.'
Keep in mind to set MODEL_NAME and PATH_TO_LABELS in your own as well as PATH_TO_TEST_IMAGES_DIR.

<p align="center">
  <img src="doc/pic1.PNG">
</p>

In order to use this code, you should move [visualization_utils.py](https://github.com/kristine4658/EMedAI/blob/master/object%20detect%20and%20crop/utils/visualization_utils.py)
also to 'models/research/object_detection/utils' as I newly add get_coordinates function to get coordinates of bounding box detected. 
The function will return list of 4 points, [ymin, xmin, ymax, xmax] in order.

The code appended can be explained mainly by 3 parts, Extract Coordinates and Crop, Filter and Image registration.

The first part simply obtain coordinates and apply those points to crop the image. 
To reduce the time spent for cropping images, you can use commented code instead, which use smaller image to extract the coordinates 
and then crop original image by multiplying rate from resized image to width and height of original. 

The second part is for filtering the image to make image registration more successful, unsharping method is applied. 
The third and last part is just image registration using orb algorithm. 

Unfortunately, as accuracy of filter and image registration part of this code is not high enough, use those two part only for the brief test.
Instead, follow the image processing tutorial explained below to improve image registration quality as well as character recognition level.
