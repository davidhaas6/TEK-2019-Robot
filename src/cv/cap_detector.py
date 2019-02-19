import cv2
import numpy as np
from cap import Cap

# https://stackoverflow.com/questions/8076889/how-to-use-opencv-simpleblobdetector#28573944


class CapDetector:
    def __init__(self, camera):
        self.CAMERA = camera

    def scan(self, raw_img=False):
        if not raw_img:
            raw_img = self.CAMERA.get_frame()

        resized_img = cv2.resize(raw_img, (0, 0), fx=.75, fy=.75)
        hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)

        # Blurring the image helps with the red-blue intersections
        hsv_img = cv2.medianBlur(hsv_img, 5, 0)

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

        num_cnts = 3
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
            circularity = self.get_circularity(cnt)
            if (circularity < circ_thresh):
                score = 0
            else:
                score = cv2.contourArea(
                    cnt) * circularity - 2*self.nearest_neighbor(cnt, red_cnts)[1]
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
            circularity = self.get_circularity(cnt)
            if (circularity < circ_thresh):
                score = 0
            else:
                score = cv2.contourArea(
                    cnt) * circularity - 2*self.nearest_neighbor(cnt, blue_cnts)[1]

            if score > score_thresh:
                # dis = self.get_distance(cnt)
                # ang = self.get_angle(cnt)
                # caps.append(Cap(dis, ang))
                ellipse = cv2.fitEllipse(cnt)
                cv2.ellipse(resized_img, ellipse, (0, 255, 0), 2)
                print("red")

            # cv2.putText(resized_img, str(round(score)), tuple(self.get_center(cnt)),
            #            cv2.FONT_HERSHEY_TRIPLEX, 1, (150, 150, 255), 1)

            # TODO: Filter my inertia ratio? (elongation)

        cv2.imshow("img", resized_img)
        cv2.waitKey(0)

    def get_distance(self, cnt):
        width_pixels = cv2.minAreaRect(cnt)[1][0]
        return Cap.WIDTH_CM * self.CAMERA.FOCAL_LEN_X / width_pixels

    def get_angle(self, cnt):
        # TODO: Pretty sure this is wrong but not sure why... sin/cos?
        cx = self.get_center(cnt)[0]
        percent_offset = (cx - self.CAMERA.IMG_WIDTH/2) / \
            (self.CAMERA.IMG_WIDTH/2)
        return percent_offset * self.CAMERA.FOV_X

    def nearest_neighbor(self, src_cnt, target_cnts):
        src_center = self.get_center(src_cnt)

        min_distance = np.linalg.norm(
            src_center-self.get_center(target_cnts[0]))
        min_cnt = target_cnts[0]
        for cnt in target_cnts[1:]:
            dist = np.linalg.norm(src_center-self.get_center(cnt))
            if(dist < min_distance):
                min_distance = dist
                min_cnt = cnt

        return (min_cnt, min_distance)

    def get_circularity(self, cnt):
        area = cv2.contourArea(cnt)
        circum = cv2.arcLength(cnt, True)
        return (4 * np.pi * area) / (circum ** 2)

    def get_center(self, cnt):
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return np.array([cx, cy])
