import cv2
import numpy as np
from cap import Cap
from feature_extractor import FeatureExtractor

# IDEA: Meanshift? https://docs.opencv.org/4.0.0/db/df8/tutorial_py_meanshift.html


class CapDetector:
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

        # Blurring the image helps with the red-blue intersections
        hsv_img = cv2.medianBlur(hsv_img, 5, 0)

        # IDEA: Adaptive color thresholding?
        BLUE_MIN = np.array([80, 70, 0], np.uint8)
        BLUE_MAX = np.array([144, 255, 255], np.uint8)

        RED1_MIN = np.array([150, 70, 0], np.uint8)
        RED1_MAX = np.array([180, 255, 255], np.uint8)
        RED2_MIN = np.array([0, 120, 0], np.uint8)
        RED2_MAX = np.array([6, 255, 255], np.uint8)

        blue_mask = cv2.inRange(hsv_img, BLUE_MIN, BLUE_MAX)
        red_mask = cv2.inRange(hsv_img, RED1_MIN, RED1_MAX) + \
            cv2.inRange(hsv_img, RED2_MIN, RED2_MAX)

        _, blue_cnts, _ = cv2.findContours(
            blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        _, red_cnts, _ = cv2.findContours(
            red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        num_cnts = 4
        red_cnts = sorted(red_cnts, key=cv2.contourArea,
                          reverse=True)[:num_cnts]
        blue_cnts = sorted(blue_cnts, key=cv2.contourArea,
                           reverse=True)[:num_cnts]

        # Finding the top-color

        # Assign a score to each contour based on its size, circularity, and closeness to
        # an oppositely colored contour
        circ_thresh = 0.5
        score_thresh = 500
        caps = []
        for cnt in blue_cnts:
            cnt_features = FeatureExtractor(self.CAMERA, cnt)
            circularity = cnt_features.get_circularity()
            if (circularity < circ_thresh):
                score = 0
            else:
                area = cnt_features.get_contour_area()
                red_distance = cnt_features.nearest_neighbor(red_cnts)[1]
                score = area * circularity - (2 * red_distance)
            if score > score_thresh:
                # dis = self.get_distance(cnt)
                # ang = self.get_angle(cnt)
                # caps.append(Cap(dis, ang))

                ellipse = cv2.fitEllipse(cnt)
                cv2.ellipse(resized_img, ellipse, (0, 255, 0), 2)
                print("blue")

            # cv2.putText(resized_img, str(round(score)), tuple(self.get_center(cnt)),
                #            cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 150, 150), 1)

        for cnt in red_cnts:
            cnt_features = FeatureExtractor(self.CAMERA, cnt)
            circularity = cnt_features.get_circularity()
            if (circularity < circ_thresh):
                score = 0
            else:
                area = cnt_features.get_contour_area()
                blue_distance = cnt_features.nearest_neighbor(red_cnts)[1]
                score = area * circularity - (2 * blue_distance)

            if score > score_thresh:
                # dis = self.get_distance(cnt)
                # ang = self.get_angle(cnt)
                # caps.append(Cap(dis, ang))
                ellipse = cv2.fitEllipse(cnt)
                cv2.ellipse(resized_img, ellipse, (0, 255, 0), 2)
                print("red")

            # cv2.putText(resized_img, str(round(score)), tuple(self.get_center(cnt)),
            #            cv2.FONT_HERSHEY_TRIPLEX, 1, (150, 150, 255), 1)

            # IDEA: Filter by inertia ratio? (elongation)

        cv2.imshow("img", resized_img)
        cv2.waitKey(0)
