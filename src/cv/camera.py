import cv2
import pickle
import os
import numpy as np
import random


class Camera:
    def __init__(self, disable_video=False, virtual=False, virtual_source="./", video_channel=1, calibration_path=False):
        # Load the undistortion parameters
        if calibration_path:
            self.CALIBRATED = True
            with open(calibration_path, 'rb') as f:
                self.DIMS, camera_matrix, dist = pickle.load(f)
                self.map1, self.map2 = cv2.fisheye.initUndistortRectifyMap(
                    camera_matrix, dist, np.eye(3), camera_matrix, DIMS, cv2.CV_16SC2)

            self.FOCAL_LEN_X = camera_matrix[0][0]  # The X focal length

        else:
            self.DIMS = (-1, -1)
            self.CALIBRATED = False

        if not disable_video:
            self.VIDEO = True
            self.video_capture = cv2.VideoCapture(video_channel)
            _, frame = self.video_capture.read()
            self.DIMS = frame.shape
            self.IMG_WIDTH = self.DIMS[1]
            self.IMG_HEIGHT = self.DIMS[0]
        else:
            self.VIDEO = False
            self.DIMENSIONS = self.DIMS
            self.IMG_WIDTH = -1
            self.IMG_HEIGHT = -1

        if virtual:
            self.VIRTUALIZED = True
            self.virtual_img_path = virtual_source
            img_dir = os.listdir(virtual_source)
            self.src_images = [
                im for im in img_dir if '.png' in im or '.jpg' in im]
            if(len(self.src_images) == 0):
                print("* WARNING: Could not find any images in source directory")

        if self.CALIBRATED:
            fov_rad = 2 * \
                np.arctan((self.IMG_WIDTH/(2 * self.FOCAL_LEN_X)))
            self.FOV_X = np.degrees(fov_rad)

    def get_frame(self, mirrored=False, undistorted=True, img_name=False):
        frame = False
        if self.VIDEO and self.video_capture.isOpened():
            retval, frame = self.video_capture.read()
            if retval:
                if mirrored:
                    frame = cv2.flip(frame, 1)
                if undistorted and self.CALIBRATED:
                    frame = self.undistort(frame)
        elif self.VIRTUALIZED and len(self.src_images) > 0:
            if img_name:
                try:
                    frame = cv2.imread(self.virtual_img_path + img_name)
                except Exception as e:
                    print("* ERROR:", e)
                    return False
            else:
                frame = cv2.imread(self.virtual_img_path +
                                   random.choice(self.src_images))
            if undistorted and self.CALIBRATED:
                frame = self.undistort(frame)
        return frame

    def undistort(self, img):
        if not self.CALIBRATED:
            print("NO CALIBRATION PATH PASSED INTO IMAGE. RETURNING BASE IMAGE")
            return img
        return cv2.remap(img, self.map1, self.map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
