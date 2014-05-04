#!usr/bin/python

# ------------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.04.2014
# Last modified : 04.04.2014
#
# Description : image library with split and feature extraction
# functions.
# ------------------------------------------------------------

from PIL import Image, ImageChops
import numpy as np 
from featureVector import *
import matplotlib.pyplot as plt
import os


class imagesLib:

	# --------------------------------------------------------
	# Variables.
	# --------------------------------------------------------

	original = None
	ndarr = None
	vector = featureVector()
	presence = []
	widthArray = []
	heightArray = []
	CoG = []
	horizontalSplit = []
	verticalSplit = []
	
	# --------------------------------------------------------
	# Image import/export.
	# --------------------------------------------------------
	
	def open(self, path):
		global ndarr
		global original
		
		try:
			original = Image.open(path)
			converted = original.convert('L')
			ndarr = np.array(converted)
			print "\n>Image loaded"
		except:
			print "Unable to load image"

	def export(self):
		global ndarr
		
		try:
			imported = Image.fromarray(ndarr)
			imported.save('export.png', 'png')
		except:
			print "\n\n>Export failed !"

	def extractFeatures(self, folderName):
		# Variables.
		global original
		horizontalOffset = 4
		verticalOffset = 0
		size = 469
		
		# Attempts to create the new folder.
		if not os.path.exists(folderName):
			os.makedirs(folderName)
			
		# Splits and stores all samples (pre-processing).
		print 'Processing digits:',
		for x in range (0,10):
			print '->', x,
			for y in range (0,10):
				# For each cell, split it.
				box = (horizontalOffset, verticalOffset, (horizontalOffset+size), (verticalOffset+size))
				horizontalOffset = (4 + y * size)
				copy = original
				
				# Trim to remove any traces of cells' borders.
				cropped = copy.crop(box)
				trim = (4, 4, size-4, size-4)
				cropped = cropped.crop(trim)
				
				# Remove all unnecessary white.
				img = self.autoCrop(cropped)
				
				# Perform actions on each digit.
				img.save(folderName+ '/' + str(x) + str(y) + '.png', 'png')
				self.extractPresence_CoG(img)
				self.extractWidthHeight(img)
				self.extractHorizontalSplit(img)
				self.extractVerticalSplit(img)
				
			verticalOffset = verticalOffset + size
			
			# Compile results for all 10 version of each digit.
			self.compilePresence_CoG()
			self.compileWidthHeight()
			self.compileSplits()
			
	# --------------------------------------------------------
	# Processing.
	# --------------------------------------------------------
	
	# Feature extraction WorkFlow.
	def features(self, path, folderName):
		self.open(path)
		self.extractFeatures(folderName)
		self.displayFeatures()
		
	# Function to automatically crop at the size of the digit.
	def autoCrop(self, image):
		bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
		diff = ImageChops.difference(image, bg)
		diff = ImageChops.add(diff, diff, 2.0, -200)
		bbox = diff.getbbox()
		if bbox:
			return image.crop(bbox)
	
	# Fetches and stores width and height for each number.
	def extractWidthHeight(self, image):
		(width, height) = image.size
		self.widthArray.append(width)
		self.heightArray.append(height)
	
	# Compute actual width and height features.
	def compileWidthHeight(self):
		self.vector.width.append(np.mean(self.widthArray))
		self.vector.height.append(np.mean(self.heightArray))
		self.widthArray = []
		self.HeightArray = []
		
	# Fetches and stores presence for each number.
	def extractPresence_CoG(self, image):
		(width, height) = image.size
		count = 0
		horizontalSum = 0
		verticalSum = 0
		
		# Count number of pixel under RGB(50,50,50).
		for i in range(width):
			for j in range(height):
				if((image.getpixel((i,j)))[0] < 50):
					count += 1
					horizontalSum += i
					verticalSum += j
					
		percentage = (count * 100) / (width * height)			
		self.presence.append(percentage)
		
		self.CoG.append(((horizontalSum / count), (verticalSum / count)))
		
	# Compute actual presence feature.
	def compilePresence_CoG(self):
		self.vector.presence.append(np.mean(self.presence))
		self.vector.CoG.append(tuple(map(np.mean, zip(*self.CoG))))
		self.presence = []
		self.CoG = []
	
	# Prepares the tuple of 6 centers of gravity.
	def extractHorizontalSplit(self, image):
		(width, height) = image.size
		middle = height / 2
		
		# Isolate v0 and v1.
		v0 = self.getCoG(image, 0, width, 0, middle)
		v1 = self.getCoG(image, 0, width, middle, height)
		
		# Get new horizontal centers of gravity.
		(v0_x, v0_y) = v0
		(v1_x, v1_y) = v1
		
		# Isolate v2, v3, v4 and v5.
		v2 = self.getCoG(image, 0, v0_x, 0, middle)
		v3 = self.getCoG(image, v0_x, width, 0, middle)
		v4 = self.getCoG(image, 0, v1_x, middle, height)
		v5 = self.getCoG(image, v1_x, width, middle, height)
		
		self.horizontalSplit.append((v0, v1, v2, v3, v4, v5))
		
	def extractVerticalSplit(self, image):
		(width, height) = image.size
		middle = width / 2
		
		# Isolate v0 and v1.
		v0 = self.getCoG(image, 0, middle, 0, height)
		v1 = self.getCoG(image, middle, width, 0, height)
		
		# Get new horizontal centers of gravity.
		(v0_x, v0_y) = v0
		(v1_x, v1_y) = v1
		
		# Isolate v2, v3, v4 and v5.
		v2 = self.getCoG(image, 0, middle, 0, v0_y)
		v3 = self.getCoG(image, middle, width, 0, v1_y)
		v4 = self.getCoG(image, 0, middle, v0_y, height)
		v5 = self.getCoG(image, middle, width, v1_y, height)
		
		self.verticalSplit.append((v0, v1, v2, v3, v4, v5))
		
	def compileSplits(self):
		self.vector.hSplit.append(self.computeMeanClusters(self.horizontalSplit))
		self.vector.vSplit.append(self.computeMeanClusters(self.verticalSplit))
		self.horizontalSplit = []
		self.verticalSplit = []
		
	# --------------------------------------------------------
	# Helpers.
	# --------------------------------------------------------

	def getCoG(self, image, widthStart, widthEnd, heightStart, heightEnd):
		count = 0
		horizontalSum = 0
		verticalSum = 0
		
		for i in range(widthStart, widthEnd):
			for j in range(heightStart, heightEnd):
				if((image.getpixel((i,j)))[0] < 50):
					count += 1
					horizontalSum += i
					verticalSum += j
		
		return ((horizontalSum / count), (verticalSum / count))
		
	def computeMeanClusters(self, clusterList):
		v0_x = []
		v0_y = []
		v1_x = []
		v1_y = []
		v2_x = []
		v2_y = []
		v3_x = []
		v3_y = []
		v4_x = []
		v4_y = []
		v5_x = []
		v5_y = []
		
		for tuple in clusterList:
			(v0, v1, v2, v3, v4, v5) = tuple
			(a,b) = v0
			(c,d) = v1
			(e,f) = v2
			(g,h) = v3
			(i,j) = v4
			(k,l) = v5
			
			# Append the the right list.
			v0_x.append(a)
			v0_y.append(b)
			v1_x.append(c)
			v1_y.append(d)
			v2_x.append(e)
			v2_y.append(f)
			v3_x.append(g)
			v3_y.append(h)
			v4_x.append(i)
			v4_y.append(j)
			v5_x.append(k)
			v5_y.append(l)
			
		# Reconstruct mean tuple.
		return ((np.mean(v0_x),np.mean(v0_y)),
				(np.mean(v1_x),np.mean(v1_y)),
				(np.mean(v2_x),np.mean(v2_y)),
				(np.mean(v3_x),np.mean(v3_y)),
				(np.mean(v4_x),np.mean(v4_y)),
				(np.mean(v5_x),np.mean(v5_y)))
	
	# --------------------------------------------------------
	# Printing results.
	# --------------------------------------------------------

	# Compiles features for display.
	def displayFeatures(self):
		print '\n\n>','=' * 110
		print '\n> FEATURES VECTOR.'
		print '\n>','=' * 110
		
		print '\n\nPresence:\t'
		for value in self.vector.presence:
			print ' {0:0.1f}% |'.format(value),
			
		print '\n\nMean width:\t'
		for value in self.vector.width:
			print ' {0:0.3f} |'.format(value),
			
		print '\n\nMean height:\t'
		for value in self.vector.height:
			print ' {0:0.3f} |'.format(value),
			
		print '\n\nCoG:\t'
		print self.vector.CoG
			
		print '\n\nHorizontal Splits:\t'
		print self.vector.hSplit
			
		print '\n\nVertical Splits:\t'
		print self.vector.vSplit
				
		print '\n\n>','=' * 110, '\n'