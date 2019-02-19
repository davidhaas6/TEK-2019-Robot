import cv2
import numpy as np


class BallDetector:
    def __init__(self, camera):
        self.CAMERA = camera

    def scan(self, src_img=False, resize_img=True):
        if not src_img:
            src_img = self.CAMERA.get_frame()

        if resize_img:
            resized_img = cv2.resize(src_img, (0, 0), fx=.75, fy=.75)
        else:
            resize_img = src_img

        hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)

        # Reduce noise
        hsv_img = cv2.gaussianBlur(hsv_img, (11, 11), 0)

        # TODO: Determine yellow in and max
        YELLOW_MIN = np.array([80, 70, 0], np.uint8)
        YELLOW_MAX = np.array([144, 255, 255], np.uint8)

        masked = cv2.inRange(hsv_img, YELLOW_MIN, YELLOW_MAX)

        _, cnts, _ = cv2.findContours(
            masked, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        num_cnts = 5
        cnts = sorted(cnts, key=cv2.contourArea,
                      reverse=True)[:num_cnts]
