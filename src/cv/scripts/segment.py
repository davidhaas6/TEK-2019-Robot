import cv2
import time
import argparse
import glob
import numpy as np

# global variable to keep track of
show = False


def onTrackbarActivity(x):
    global show
    show = True
    pass


if __name__ == '__main__':

    # Get the filename from the command line
    files = glob.glob('../data/*.jpg')
    files.sort()
    # load the image
    original = cv2.imread(files[0])
    # Resize the image
    rsize = 300
    original = cv2.resize(original, (rsize, rsize))

    # position on the screen where the windows start
    initialX = 50
    initialY = 50

    # creating windows to display images
    cv2.namedWindow('P-> Previous, N-> Next', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('SelectHSV', cv2.WINDOW_AUTOSIZE)

    # moving the windows to stack them horizontally
    cv2.moveWindow('P-> Previous, N-> Next', initialX, initialY)
    cv2.moveWindow('SelectHSV', initialX + 2*(rsize + 5), initialY)

    # creating trackbars to get values for HSV
    cv2.createTrackbar('HMin', 'SelectHSV', 0, 180, onTrackbarActivity)
    cv2.createTrackbar('HMax', 'SelectHSV', 0, 180, onTrackbarActivity)
    cv2.createTrackbar('SMin', 'SelectHSV', 0, 255, onTrackbarActivity)
    cv2.createTrackbar('SMax', 'SelectHSV', 0, 255, onTrackbarActivity)
    cv2.createTrackbar('VMin', 'SelectHSV', 0, 255, onTrackbarActivity)
    cv2.createTrackbar('VMax', 'SelectHSV', 0, 255, onTrackbarActivity)

    # show all images initially
    cv2.imshow('SelectHSV', original)
    i = 0
    while(1):

        cv2.imshow('P-> Previous, N-> Next', original)
        k = cv2.waitKey(1) & 0xFF

        # check next image in folder
        if k == ord('n'):
            i += 1
            original = cv2.imread(files[i % len(files)])
            original = cv2.resize(original, (rsize, rsize))
            show = True

        # check previous image in folder
        elif k == ord('p'):
            i -= 1
            original = cv2.imread(files[i % len(files)])
            original = cv2.resize(original, (rsize, rsize))
            show = True
        # Close all windows when 'esc' key is pressed
        elif k == 27:
            break

        if show:  # If there is any event on the trackbar
            show = False

            # Get values from the HSV trackbar
            HMin = cv2.getTrackbarPos('HMin', 'SelectHSV')
            SMin = cv2.getTrackbarPos('SMin', 'SelectHSV')
            VMin = cv2.getTrackbarPos('VMin', 'SelectHSV')
            HMax = cv2.getTrackbarPos('HMax', 'SelectHSV')
            SMax = cv2.getTrackbarPos('SMax', 'SelectHSV')
            VMax = cv2.getTrackbarPos('VMax', 'SelectHSV')
            minHSV = np.array([HMin, SMin, VMin])
            maxHSV = np.array([HMax, SMax, VMax])

            print("\nmin:", minHSV)
            print("max:", maxHSV)

            # Convert the BGR image to other color spaces
            imageHSV = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)

            # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results
            maskHSV = cv2.inRange(imageHSV, minHSV, maxHSV)
            resultHSV = cv2.bitwise_and(original, original, mask=maskHSV)

            # Show the results
            cv2.imshow('SelectHSV', resultHSV)

    cv2.destroyAllWindows()
