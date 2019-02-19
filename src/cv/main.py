import cv2
import numpy as np
import os
from cap_detector import CapDetector
from camera import Camera

print("working directory: ", os.getcwd())

# Grabs and shuffles the images

# img = cv2.imread(data_path + "backg1.jpg")
# center, width = bcv.get_buoy_size(img, True, "backg")

cam = Camera(disable_video=True, virtual=True, virtual_source="./data/")
cd = CapDetector(cam)
while(1):
    cd.scan()
