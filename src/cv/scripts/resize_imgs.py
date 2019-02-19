import cv2
import numpy as np
import os

print("working directory: ", os.getcwd())
# Grabs and shuffles the images
data_path = "../data/"
img_dir = os.listdir(data_path)
img_dir = [im for im in img_dir if '.png' in im or '.jpg' in im]
# np.random.shuffle(img_dir)

# img = cv2.imread(data_path + "backg1.jpg")
# center, width = bcv.get_buoy_size(img, True, "backg")

#cam = Camera(disable_video=True)

for img_path in img_dir:
    img = cv2.imread(data_path + img_path)
    img = cv2.resize(img, (0, 0), fx=.2, fy=.2)
    cv2.imwrite(data_path + img_path, img)
