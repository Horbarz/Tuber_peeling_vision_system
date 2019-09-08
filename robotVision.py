from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import serial
import numpy as np
import argparse
import imutils
import cv2
from imageCropper import get_cropped_images2, least_rect_contour, max_rect_contour

port_string = '/dev/ttyACM0'


def encode(message):
    a = b'%d' % message
    return a


def readPort():
    ser = serial.Serial(port=port_string, baudrate=9600, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

    while True:
        if ser.inWaiting() > 0:
            inputValue = ser.readline()
            return inputValue.strip().decode()
    return


def writePort(message):
    usbCom = serial.Serial(port_string, 9600)

    usbCom.write(encode(message))
    # time.sleep(1)
    print(message)
    return


def previewCamera():
    camera = PiCamera()
    camera.start_preview()
    time.sleep(5)
    camera.stop_preview()


def triggerCamera(n):
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    time.sleep(0.5)
    camera.capture(rawCapture, format="bgr")
    captured = rawCapture.array
    if (n == 1):
        cv2.imshow("image", captured)
        img1 = "/home/pi/Desktop/pythonCodes/CassavaImages/1.jpg"
        cv2.imwrite(img1, captured)

    elif (n == 2):
        img2 = "/home/pi/Desktop/pythonCodes/CassavaImages/2.jpg"
        cv2.imwrite(img2, captured)
    elif (n == 3):
        img3 = "/home/pi/Desktop/pythonCodes/CassavaImages/3.jpg"
        cv2.imwrite(img3, captured)
    elif (n == 4):
        img4 = "/home/pi/Desktop/pythonCodes/CassavaImages/4.jpg"
        cv2.imwrite(img4, captured)
    elif (n == 5):
        img5 = "/home/pi/Desktop/pythonCodes/CassavaImages/5.jpg"
        cv2.imwrite(img5, captured)
    elif (n == 6):
        img6 = "/home/pi/Desktop/pythonCodes/CassavaImages/6.jpg"
        cv2.imwrite(img6, captured)
    elif (n == 7):
        img7 = "/home/pi/Desktop/pythonCodes/CassavaImages/7.jpg"
        cv2.imwrite(img7, captured)
    elif (n == 8):
        img8 = "/home/pi/Desktop/pythonCodes/CassavaImages/8.jpg"
        cv2.imwrite(img8, captured)

        # cv2.waitKey(0)
    # return


def resizedImage(img, scale_percent):
    # scale_percent = 70 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    # cv2.imshow("Resized image", resized)
    return resized


def metricPerPixel(widthpx, givenPx):
    unKnownLength = 0
    width_of_frame = 23
    length_per_px = width_of_frame / widthpx
    unKnownLength = givenPx * length_per_px
    return int(unKnownLength)


def getDistance(n):
    if n == 1:
        new_img = "/home/pi/Desktop/pythonCodes/CassavaImages/1.jpg"
    elif n == 2:
        new_img = "/home/pi/Desktop/pythonCodes/CassavaImages/2.jpg"
    elif n == 3:
        new_img = "/home/pi/Desktop/pythonCodes/CassavaImages/3.jpg"
    elif n == 4:
        new_img = "/home/pi/Desktop/pythonCodes/CassavaImages/4.jpg"
    elif n == 5:
        new_img = "/home/pi/Desktop/pythonCodes/CassavaImages/5.jpg"
    elif n == 6:
        new_img = "/home/pi/Desktop/pythonCodes/CassavaImages/6.jpg"
    elif n == 7:
        new_img = "/home/pi/Desktop/pythonCodes/CassavaImages/7.jpg"
    elif n == 8:
        new_img = "/home/pi/Desktop/pythonCodes/CassavaImages/8.jpg"

    image = cv2.imread(new_img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Blurring the image
    img_blur = cv2.bilateralFilter(image, d=7, sigmaSpace=75, sigmaColor=75)

    # Convert to gray scale
    image_gray = cv2.cvtColor(img_blur, cv2.COLOR_RGB2GRAY)

    # Apply the thresholding
    a = image_gray.max()
    _, thresh = cv2.threshold(image_gray, a / 2 + 60,
                              a, cv2.THRESH_BINARY_INV)

    # get image height
    max_img, tuber_height, x_cord, x2_cord = max_rect_contour(image, thresh)
    mImg = resizedImage(max_img, 50)

    # show cropped images
    img_h, img_w, _ = image.shape
    crops = get_cropped_images2(tuber_height, img_w, 25)

    tuber_height_cm = metricPerPixel(img_w, tuber_height);

    # if knife is at the LHS of the tuber
    # knife_starting_point = x_cord

    # if knife is at the RHS of the tuber
    knife_starting_point = img_w - x2_cord

    first_img = []

    for crop in crops[::-1]:
        image_box = image.copy()
        thresh_copy = thresh.copy()
        img = image_box[crop[2]:crop[3], crop[0]:crop[1]]
        thresh_img = thresh_copy[crop[2]:crop[3], crop[0]:crop[1]]
        marked_img, x_len, x2_len = least_rect_contour(thresh_img, img)
        # cv2.imshow('{0}'.format(crop), marked_img)

        # if knife is at LHS of tuber
        side1_px = x_len - x_cord

        # if knife is at RHS of the tuber
        side2_px = img_w - x2_len - knife_starting_point

        side1_cm = metricPerPixel(img_w, side1_px)
        side2_cm = metricPerPixel(img_w, side2_px)
        # print("Side1: The knife has to go {0} cm deep".format(side1_cm))
    #       print("Side2: The knife has to go {0} px deep".format(side2))
    return first_img, tuber_height_cm


# Trigger Camera

writePort()

trigger_value = int(readPort())

if trigger_value == 1:
    triggerCamera(1)
    writePort(11)
    # Rotate tuber 45 degrees
elif trigger_value == 2:
    triggerCamera(2)
    writePort(22)
    # Rotate tuber 90 degrees
elif trigger_value == 3:
    triggerCamera(3)
    writePort(33)
    # Rotate tuber 135 degrees
elif trigger_value == 4:
    triggerCamera(4)
    writePort(44)
    # Rotate tuber 180 degrees
elif trigger_value == 5:
    triggerCamera(5)
    writePort(55)
    # Rotate tuber 225 degrees
elif trigger_value == 6:
    triggerCamera(6)
    writePort(66)
    # Rotate tuber 270 degrees
elif trigger_value == 7:
    triggerCamera(7)
    writePort(77)
    # Rotate tuber 315 degrees
elif trigger_value == 8:
    triggerCamera(8)
    writePort(88)
    # Rotate tuber 360 degrees

# Distance from knife in centimeters
[sideOne, t_height] = getDistance(1)
[sideTwo, t_height2] = getDistance(2)
[sideThree, t_height3] = getDistance(3)
[sideFour, t_height4] = getDistance(4)
[sideFive, t_height5] = getDistance(5)
[sideSix, t_height6] = getDistance(6)
[sideSeven, t_height7] = getDistance(7)
[sideEight, t_height8] = getDistance(8)

length_of_sides = len(sideOne)

knife_movement = t_height / length_of_sides

# send knife movement to arduino
writePort(knife_movement);

for i in range(len(sideOne)):
    writePort(sideOne[i])
    writePort(sideTwo[i])
    writePort(sideThree[i])
    writePort(sideFour[i])
    writePort(sideFive[i])
    writePort(sideSix[i])
    writePort(sideSeven[i])
    writePort(sideEight[i])
    # Send value to pi after slicing first step
    if trigger_value == 21:
        continue
    else:
        break