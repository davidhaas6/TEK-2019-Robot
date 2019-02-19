import cv2
import numpy as np


class FeatureExtractor:
    def __init__(self, camera, contour):
        self.CAMERA = camera
        self.my_contour = contour

        # Private variables... Do not directly access
        self._CENTER = None
        self._ANGLE = None
        self._CIRCULARITY = None
        self._CONTOUR_AREA = None

    def get_distance(self, physical_width):
        width_pixels = cv2.minAreaRect(self.my_contour)[1][0]
        return physical_width * self.CAMERA.FOCAL_LEN_X / width_pixels

    def get_angle(self, img_width):
        # REVIEW: Pretty sure this algorithm is wrong but not sure why... sin/cos?
        if self._ANGLE is None:
            cx = self.get_center()[0]
            percent_offset = (cx - img_width/2) / \
                (img_width/2)
            self._ANGLE = percent_offset * self.CAMERA.FOV_X/2
        return self._ANGLE

    def nearest_neighbor(self, target_cnts):
        src_center = self.get_center()

        # Get features for each of the contours for comparison
        target_features = [FeatureExtractor(
            self.CAMERA, cnt) for cnt in target_cnts]

        min_distance = np.linalg.norm(
            src_center - target_features[0].get_center())
        min_cnt = target_features[0].get_contour()

        for cnt_feature in target_features[1:]:
            dist = np.linalg.norm(src_center - cnt_feature.get_center())
            if(dist < min_distance):
                min_distance = dist
                min_cnt = cnt_feature.get_contour()

        return (min_cnt, min_distance)

    def get_circularity(self):
        if self._CIRCULARITY is None:
            area = self.get_contour_area()
            circum = cv2.arcLength(self.my_contour, True)
            self._CIRCULARITY = (4 * np.pi * area) / (circum ** 2)
        return self._CIRCULARITY

    def get_center(self):
        if self._CENTER is None:
            M = cv2.moments(self.my_contour)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            self._CENTER = np.array([cx, cy])
        return self._CENTER

    def get_contour(self):
        return self.my_contour

    def get_contour_area(self):
        if self._CONTOUR_AREA is None:
            self._CONTOUR_AREA = cv2.contourArea(self.my_contour)
        return self._CONTOUR_AREA
