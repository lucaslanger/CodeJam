#import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pickle

def leftfacecol(image, row):		#helper function		input: image array,row
					#				output: column
	leftbackgroundAv = sum(int(image[row][k+5]) for k in range(5))/5
	rightbackgroundAv = sum(int(image[row][314-k]) for k in range(5))/5
	leftcrit = 50 if leftbackgroundAv >=150 else 30
	rightcrit = 50 if rightbackgroundAv >= 150 else 30
	movingAv = sum(int(image[row][j+5]) for j in range(10))/10
	for i in range(5,310):	
		if image[row][i+9] >= 225 and i<300:
			i+=10
			movingAv = sum(int(image[row][j+i]) for j in range(10))/10
		if abs(movingAv - leftbackgroundAv) > leftcrit and abs(movingAv - rightbackgroundAv) > rightcrit: #and all(image[row][k] <225 for k in range(i,i+10)):
			return i+5
		movingAv = movingAv + (int(image[row][i+9]) - int(image[row][i-1]))/10
	return 319


def leftfacegraph(image):				#input: image
	res = []				#output: a bunch of points on the jaw outline
	for i in range(243):
		res.append(leftfacecol(image,i))
	return res

def rightfacecol(image, row):
	leftbackgroundAv = sum(int(image[row][k+5]) for k in range(5))/5
	rightbackgroundAv = sum(int(image[row][314-k]) for k in range(5))/5
	leftcrit = 50 if leftbackgroundAv >=150 else 25
	rightcrit = 50 if rightbackgroundAv >= 150 else 25
	movingAv = sum(int(image[row][315-j]) for j in range (10))/10	
	for i in range(5,310):	
		if image[row][310-i] >= 225 and i<300:
			i+=10
			movingAv = sum(int(image[row][315-j-i]) for j in range(10))/10
		if abs(movingAv-rightbackgroundAv) > rightcrit and abs(movingAv - leftbackgroundAv) > leftcrit and all(image[row][320-k] <225 for k in range(i+1,i+10+1)):
			return 319-i
		movingAv = movingAv + (int(image[row][310-i]) - int(image[row][320-i]))/10	 
	return 0

def rightfacegraph(image):
	res = []
	for i in range(243):
		res.append(rightfacecol(image,i))
	return res


def leftgraphonface(image):					#input: image
	graph = leftfacegraph(image)			#output: image with black line on face
	for i in range(242):
		image[i][graph[i]] = 0
	imgplot = plt.imshow(image, cmap = mpimg.cm.Greys_r)
	plt.show()

def rightgraphonface(image):
	graph = rightfacegraph(image)			#output: image with black line on face
	for i in range(243):
		image[i][graph[i]] = 0
	imgplot = plt.imshow(image, cmap = mpimg.cm.Greys_r)
	plt.show()
	
def translate(array):								#input: array of jaw points
	crop = [array[i] for i in range(30,170)]				#output: cropped and shifted array of jaw points
	translate = [crop[i] - min(crop) for i in range(len(crop)-1)]
	return translate

def compare(array1,array2):							#input: 2 arrays of same length
	diff = [(array1[i]-array2[i])**2 for i in range(len(array1)-1)]		#outpu: difference of each element squared
	return diff


def img_to_leftarray(image):						#input: image
								#output: left array 
	return translate(leftfacegraph(image))
	
def img_to_rightarray(image):						#input: image
								#output: right array 
	return translate(rightfacegraph(image))

def getjawdiff(image1,image2):
	left1, left2 = img_to_leftarray(image1),  img_to_leftarray(image2)
	right1, right2  = img_to_rightarray(image1), img_to_rightarray(image2)		
	diffleft = compare(left1,left2)
	diffright=compare(right1,right2)
	numleft = sum(i for i in diffleft)
	numright = sum(i for i in diffright)
	if numleft < numright:
		return diffleft
	else:
		return diffright

def getnumjawdiff(image1,image2):							#input: 2 images
	left1, left2 = img_to_leftarray(image1),  img_to_leftarray(image2)		#output: min numerical jaw line diff
	right1, right2  = img_to_rightarray(image1), img_to_rightarray(image2)		
	diffleft = compare(left1,left2)
	diffright=compare(right1,right2)
	numleft = sum(i for i in diffleft)
	numright = sum(i for i in diffright)
	return min(numleft,numright)

def scoreJaws(left1,right1,left2,right2):
	array1l = translate(left1)
	array1r = translate(right1)
	array2l = translate(left2)
	array2r = translate(right2)
	diffleft = compare(array1l,array2l)
	diffright= compare(array1r,array2r)
	numleft = sum(i for i in diffleft)
	numright = sum(i for i in diffright)
	val = min(numleft,numright)
	return val	

def identify(image1,image2):
	if getnumjawdiff(image1,image2) < 3000:
		return True
	return False

