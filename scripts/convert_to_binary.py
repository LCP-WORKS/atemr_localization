#! /usr/bin/env python3

import argparse, os
import rospkg
import cv2 # Import OpenCV

parser = argparse.ArgumentParser(description='Optional app description')
# Required positional argument
parser.add_argument('filename', help='PNG to convert to binary')
args = parser.parse_args()
dirname = os.path.splitext(args.filename)

rospack = rospkg.RosPack()
pkgpath = rospack.get_path('atemr_localization') + '/maps/'
if( not os.path.exists(os.path.join(pkgpath, dirname[0]))):
	os.mkdir(os.path.join(pkgpath, dirname[0]))

   
# read the image file
img = cv2.imread(args.filename)
bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# converting to its binary form
_, bin_img = cv2.threshold(bw, 240, 255, cv2.THRESH_BINARY)
  
# Display and save image 
#cv2.imshow("Binary", bw_img)
cv2.imwrite(os.path.join(pkgpath, dirname[0], args.filename), bin_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
