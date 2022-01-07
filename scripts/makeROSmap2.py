#! /usr/bin/env python3

import argparse, os, math
import rospkg
import cv2 # Import OpenCV


class mapMaker:
	def __init__(self):
	  parser = argparse.ArgumentParser(description='Optional app description')
	  parser.add_argument('filename', help='PNG to convert to binary')
	  self.args = parser.parse_args()
	  self.dirname = os.path.splitext(self.args.filename)
	  rospack = rospkg.RosPack()
	  self.pkgpath = rospack.get_path('atemr_localization') + '/maps/'
	  if( not os.path.exists(os.path.join(self.pkgpath, self.dirname[0]))):
	    os.mkdir(os.path.join(self.pkgpath, self.dirname[0]))
	
	def develop_map(self, hx, hy, hdist, vx, vy, vdist):
	  dx = math.sqrt((hx[1] - hx[0])**2 + (hy[1] - hy[0])**2)*.05
	  sx = hdist / dx
	  dy = math.sqrt((vx[1] - vx[0])**2 + (vy[1] - vy[0])**2)*.05
	  sy = vdist/dy 
	  print('Scaling parameters: %f - %f' % (sx, sy))
	  img = cv2.imread(self.args.filename)
	  bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	  _, bin_img = cv2.threshold(bw, 240, 255, cv2.THRESH_BINARY)
	  res_img = cv2.resize(bin_img, None, fx=sx, fy=sy, interpolation = cv2.INTER_CUBIC)
	  cv2.imwrite(os.path.join(self.pkgpath, self.dirname[0], self.dirname[0] + '.pgm'), res_img)
	
	def create_yaml(self):
	  yaml = open(os.path.join(self.pkgpath, self.dirname[0], self.dirname[0] + '.yaml'), "w")
	  yaml.write("image: " + self.dirname[0] + ".pgm\n")
	  yaml.write("resolution: 0.050000\n")
	  yaml.write("origin: [0.0, 0.00, 0.00]\n")
	  yaml.write("negate: 0\noccupied_thresh: 0.65\nfree_thresh: 0.196")
	  yaml.close()
	    
	def run(self):
	  font = cv2.FONT_HERSHEY_SIMPLEX
	  hxparams = (289, 500)
	  hyparams = (220, 220)
	  vxparams = (237, 227)
	  vyparams = (380, 232)
	  hdist = 10 #meters
	  vdist = 5 #meters
	  self.develop_map(hxparams, hyparams, hdist, vxparams, vyparams, vdist)
	  self.create_yaml()





if __name__ == '__main__':
  mmap = mapMaker()
  mmap.run()
