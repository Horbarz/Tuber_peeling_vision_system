import cv2


def get_cropped_images2(img_height, img_width, crop_height):
    crops = [[0, img_width, h - crop_height, h] for h in range(0 + crop_height, img_height + crop_height, crop_height)]
    return crops

def max_rect_contour(image,thresh):
    # find contour of image
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    # sort contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # Draw contour
    image_copy = image.copy()
    # final = cv2.drawContours(image_copy,contours,contourIdx=-1, color=(255,0,0), thickness=2)

    c_0 = contours[0]

    # get 4 point of the rectangle
    x, y, w, h = cv2.boundingRect(c_0)

    # Get the 4 points of the bounding rectangle with the minimum area
    rect = cv2.minAreaRect(c_0)
    box = cv2.boxPoints(rect)
    box = box.astype('int')

    # Draw  a contour with this points
    #image_box = cv2.drawContours(image_copy, contours=[box], contourIdx=-1, color=(0, 0, 255), thickness=2)
    image_box = cv2.rectangle(image_copy, (x, y), (x + w, y + (h)), color=(0, 0, 255), thickness=2)
    rect_width = x + w
    return image_box,h,x,rect_width

def least_rect_contour(thresh, image):
    # find contour of image
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    # sort contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Draw contour
    image_copy = image.copy()
    # final = cv2.drawContours(image_copy,contours,contourIdx=-1, color=(255,0,0), thickness=2)

    c_0 = contours[0]
    M = cv2.moments(c_0)
    # print(M.keys())

    # Other Shapes of the contours
    # c_0 = contours[0] 	#The first order of the contours

    # get 4 point of the rectangle
    x, y, w, h = cv2.boundingRect(c_0)

    # Get the 4 points of the bounding rectangle with the minimum area
    rect = cv2.minAreaRect(c_0)
    box = cv2.boxPoints(rect)
    box = box.astype('int')

    # b = box.astype('array')
    #print(box[[1][0]][0])
    if (box[[0][0]][0] == box[[1][0]][0]):
        x_len = min([box[0][0], box[2][0]])
        x2_len = max([box[0][0], box[2][0]])
    else:
        x_len = min([box[0][0], box[1][0]])
        x2_len = max([box[0][0], box[1][0]])



    # Draw  a contour with this points
    image_box = cv2.drawContours(image_copy,contours=[box],contourIdx=-1,color=(0,0,255),thickness=2)



    return image_box, x_len, x2_len


if __name__ == '__main__':
    print(get_cropped_images2(10, 5, 2))
