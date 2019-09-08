import cv2
import imutils
from imutils import perspective
from imutils import contours
import numpy as np
import matplotlib.pyplot as plt
from imageCropper import get_cropped_images2, least_rect_contour, max_rect_contour


def metricPerPixel(widthpx,givenPx):
    unKnownLength =0
    width_of_frame = 23
    length_per_px = width_of_frame/widthpx
    unKnownLength = givenPx * length_per_px
    return int(unKnownLength)

def getDistance(n):
	if n == 1:
		new_img= "tuber/01.jpg"
	elif n == 2:
		new_img= "tuber/02.jpg"
	elif n == 3:
		new_img = "tuber/03.jpg"
	elif n == 4:
		new_img = "tuber/04.jpg"
	elif n == 5:
		new_img = "tuber/05.jpg"
	elif n == 6:
		new_img = "tuber/06.jpg"
	elif n == 7:
		new_img = "tuber/07.jpg"
	elif n == 8:
		new_img = "tuber/08.jpg"

	image = cv2.imread(new_img)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


	#Blurring the image
	img_blur = cv2.bilateralFilter(image, d=7,sigmaSpace=75,sigmaColor=75)

	#Convert to gray scale
	image_gray = cv2.cvtColor(img_blur,cv2.COLOR_RGB2GRAY)

	#Apply the thresholding
	a = image_gray.max()
	_, thresh = cv2.threshold(image_gray, a/2+60,
				  a,cv2.THRESH_BINARY_INV)

	max_img, image_height, x_cord,x2_cord = max_rect_contour(image,thresh)

	# show crops
	img_h, img_w, _ = image.shape
	crops = get_cropped_images2(image_height, img_w, 30)
	#print(crops)
	knife_starting_point = img_w - x2_cord

	first_img = []
	for crop in crops[::-1]:
		image_box = image.copy()
		thresh_copy = thresh.copy()
		img = image_box[crop[2]:crop[3], crop[0]:crop[1]]
		thresh_img = thresh_copy[crop[2]:crop[3], crop[0]:crop[1]]
		marked_img, x_len, x2_len = least_rect_contour(thresh_img, img)
		#cv2.imshow('{0}'.format(crop), marked_img)
		side1 = x_len-x_cord
		side2 = img_w - x2_len - knife_starting_point
		side1_cm = metricPerPixel(img_w,side1)
		side2_cm = metricPerPixel(img_w,side2)
		#if knife starting point is at LHS
		# print("Side1: The knife has to go {0} px deep".format(side1))
		# print("Side1: The knife has to go {0} cm deep".format(side1_cm))
		#if knife starting point is at RHS
		# print("Side2: The knife has to go {0} px deep".format(side2))
		# print("Side2: The knife has to go {0} cm deep".format(side2_cm))

		first_img.append(side1_cm)

		#cv2.waitKey(0)
		#cv2.waitKey(0)

	return first_img
x = 6
for i in range (1,11):
	print(i)
	if x == 8:
		continue
	else:
		break


