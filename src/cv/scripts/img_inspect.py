import cv2
import numpy as np
import sys
import os

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = .75
fontColor = (255, 0, 255)
lineType = 2


def mos_pos(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        (info_type, img, window_name) = param

        inspect_img = img.copy()
        if info_type == 'hsv':
            inspect_img = cv2.cvtColor(inspect_img, cv2.COLOR_BGR2HSV)
        elif info_type == 'lab':
            inspect_img = cv2.cvtColor(inspect_img, cv2.COLOR_BGR2LAB)

        value = inspect_img[y, x]

        draw_img = img.copy()
        cv2.arrowedLine(draw_img, (x+13, y-13), (x, y), fontColor, 1)
        cv2.putText(draw_img, info_type+str(value), (x+15, y-15), font,
                    fontScale, fontColor, lineType)
        cv2.imshow(window_name, draw_img)
        print((x, y), " -> ", info_type, value)


def main(argv):
    if(len(argv) != 2):
        print("use: img_inspect.py image_path.png colorspace")
        sys.exit(1)

    image_path = argv[0]
    info_type = argv[1].lower()

    if info_type not in ['bgr', 'hsv', 'lab']:
        print("colorspace must be one of: bgr, hsv, lab")
        sys.exit(1)

    img = cv2.imread(image_path)
    img = cv2.resize(img, (0, 0), fx=.75, fy=.75)
    cv2.namedWindow(image_path)
    cv2.setMouseCallback(image_path, mos_pos, [info_type, img, image_path])

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
    print("*** Please wait about 3 seconds for OpenCV to initialize ***")
    print("*** Clicking will display the value of that pixel ***")
    print("*** Enter any key on the image window to quit ***")
    cv2.imshow(image_path, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    pass


if __name__ == "__main__":
    main(sys.argv[1:])
