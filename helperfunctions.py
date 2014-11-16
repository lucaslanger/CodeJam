#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
import numpy as np
import pickle
import os

from eyes import leftfacegraph
from eyes import rightfacegraph

def testJawlineOnPhoto(jawline, photo):
	photo = mpimg.imread("dataset/" + photo)

	for r in range( len(jawline) ):
		photo[r][jawline[r]] = 0

	imgplot = plt.imshow(photo, cmap = mpimg.cm.Greys_r)
	plt.show()
	


def getIDS():
	ids = {}
	for f in os.listdir('dataset'):
		try:
			underscore_location = f.index("_")
			key = int(f[:underscore_location])
			if ids.has_key(key) == False:
				ids[key] = True
		except:
			print "Not an ID" , f
	return ids
