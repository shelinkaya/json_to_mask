#below code is able to convert colored(RGB(0-255)) images to the black and white image.

import cv2

#read image
img_grey = cv2.imread('image15.png', cv2.IMREAD_GRAYSCALE)

# define a threshold, 128 is the middle of black and white in grey scale
thresh = 254

# threshold the image
img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]

#save image
cv2.imwrite('image15_label.png',img_binary) 

****************************************

#below code is able to convert black and white images to the white and black images

from PIL import Image
import PIL.ImageOps    

image = Image.open('image15_label.png')

inverted_image = PIL.ImageOps.invert(image)

inverted_image.save('image15_mask.png')
