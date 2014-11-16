#import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pickle
import os
import sys

from eyes import *

from helperfunctions import *


def getPixelStatistics(A, interval):
	leftcoords = leftfacegraph(A)
	rightcoords = rightfacegraph(A)

	leftcoordAVG = sum([l for l in leftcoords])/len(leftcoords)
	rightcoordAVG = sum([r for r in rightcoords])/len(rightcoords)

	TEST = list(A)

	categories = 256/interval

	I = [0 for i in range(categories)]

	for r in range(len(A)):
		for c in range( len(A[r]) ):
			if c > leftcoords[r] and c < rightcoords[r]:
				pixInterval = A[r][c]/interval - 1
				I[pixInterval] += 1
				#TEST[r][c] = 0

	#imgplot = plt.imshow(TEST, cmap = mpimg.cm.Greys_r)
	#plt.show()
	
	pixProportions = [ I[j]/float(sum(I)) for j in range(len(I) ) ]

	return pixProportions

def computeStandardDeviation(imagevalues, historical):
	sum_of_squares = sum([ (imagevalues[i] - historical[i])**2 for i in range( len(imagevalues) - 1 )])
	return (sum_of_squares)**0.5
	

def getAverageStats(images):
	values = []
	average = [0 for i in range(256/10) ]
	count_of_elements_in_avg = 0
	
	for f in images:
		print f
		img = mpimg.imread("dataset/" + f)
		values.append( getPixelStatistics(img, 10) )

	for line in values:
		for i in range(len(line) ): #-1
			average[i] += line[i]				
	
	        count_of_elements_in_avg += 1

	if count_of_elements_in_avg == 0:
		print "0 Elements for id number ", images

	for j in range(len(average)):
		average[j] = average[j]/(count_of_elements_in_avg) 

	#print "Length of avg before ", len(average) 
	#average.pop()
	#print "Length of avg after ", len(average) 
	
	return average

def getIDSToImages():
	images = {}
	for f in os.listdir('dataset'):
		try:
			underscore_location = f.index("_")
			personId = int(f[:underscore_location])
			if personId in images:
				images[personId].append(f)
			else:	
				images[personId] = [f]
	
		except:
			underscore_location = None
			#print "no underscore", f
		
	return images

def createPixelStatsDict(idToImages):
	pixelStatsDict = {}
	for i in idToImages:
		print "Computing Averages for Id number " ,i
		pixelStatsDict[i] = getAverageStats(idToImages[i])

	return pixelStatsDict


def assignIdToImage( sd_pixels, jtp ): #add jawline statistic
	#sd_avg = sum(sd_pixels.values() )/len(sd_pixels.values() )

	sd_total = sum(sd_pixels.values() )
	pixel_scores = {i: sd_pixels[i]/float(sd_total) for i in sd_pixels  }
	#print pixel_scores

	mp = min(pixel_scores.values() )
	for key in pixel_scores:
		if pixel_scores[key] == mp:
			#print "Pixel Assessment: ", key 
			pass
			

	jaw_total = sum(jtp.values() )
	jaw_scores = {i: jtp[i]/float(jaw_total) for i in jtp }
	#print jaw_scores

	mj = min(jaw_scores.values() )
	for key in jaw_scores:
		if jaw_scores[key] == mj:
			#print "Jaw Assessment: ", key 
			pass
			

	ready_to_rumble = {i: (jaw_scores[i] + pixel_scores[i])/2 for i in jtp}
	#print sum(ready_to_rumble.values())

	m = min(ready_to_rumble.values() )
	
	for key in ready_to_rumble:
		if ready_to_rumble[key] == m:
			return key 


def jawToPersonScore(idToJawline, img):
	jtp = {}
	for compareID in idToJawline:
		ljaw = leftfacegraph(img)
		rjaw = rightfacegraph(img)
		s = scoreJaws(ljaw,rjaw, idToJawline[compareID]["leftjaw"] , idToJawline[compareID]["rightjaw"] )
		jtp[compareID] = s

	return jtp
	

def getIDSToJawLine(idToImages):

	idToJawline = {}
	
	for iD in idToImages:
		avg_L = []
		avg_R = []
		for loc in idToImages[iD]:
			print loc
			img = mpimg.imread("dataset/" + loc)
			left_jawline = leftfacegraph(img)
			right_jawline = rightfacegraph(img)
			if avg_L == []:
				avg_L = left_jawline
				avg_R = right_jawline

			else:
				for i in range( len(left_jawline) ):
					avg_L[i] = avg_L[i] + left_jawline[i]
					avg_R[i] = avg_R[i] + right_jawline[i]

		idToJawline[iD] = {"leftjaw": [ avg_L[k]/len( idToImages[iD] )  for k in range(len(avg_L) ) ], "rightjaw": [ avg_R[k]/len( idToImages[iD] ) for k in range(len(avg_R) ) ] }
	
	return idToJawline



	
def examFaces(): #need to uncomment pixelStat debug
	idToImages = getIDSToImages()

	for key in idToImages:
		for v in idToImages[key]:
			print v
			img = mpimg.imread("dataset/" + v)
			imgstats = getPixelStatistics(img, 10) #need to uncomment pixelStat debug!!!


def PHOTOVSALGORITHM(loc):


	idToImages = getIDSToImages()

	try:
		pixelStatsDict = pickle.load( open("pixelStatsDict.txt","r" ) )	
	except Exception, e:
		print str(e)
		pixelStatsDict = createPixelStatsDict(idToImages)
		with open("pixelStatsDict.txt", "w+") as f:
			pickle.dump(pixelStatsDict, f)
	
	try:
		idToJawline = pickle.load(open("jawLinesDict.txt" , "r"))
	except:	
		idToJawline = getIDSToJawLine(idToImages)
		with open("jawLinesDict.txt" , "w+") as f2:
			pickle.dump(idToJawline, f2)

	photo = mpimg.imread(loc)
	photoStats = getPixelStatistics(photo , 10)
	
	jtp = jawToPersonScore(idToJawline, photo)
	sd_pixels = {i: computeStandardDeviation(photoStats, pixelStatsDict[i]) for i in pixelStatsDict }

	answer = assignIdToImage( sd_pixels, jtp )
	return int(answer)


	

def testWITHHALFDB(): 

	correctcount = 0
	total = 0
	for f in os.listdir('dataset'):
		if f[-4:] == ".gif":
			print "This is the file: ", f
			a = PHOTOVSALGORITHM("dataset/" + f)
			print "Answer was ", a
			if a == int(f[:f.index("_")]):
				correctcount += 1
			total += 1
		
	print total, correctcount
	

	#testJawlineOnPhoto(idToJawline[1]['leftjaw'], "1_9_.gif")

photoinput = sys.argv[1]
print PHOTOVSALGORITHM( photoinput )

#testWITHHALFDB()

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

		



