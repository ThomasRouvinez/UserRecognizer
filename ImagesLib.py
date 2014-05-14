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
from FeatureVector import *
from SplitsLib import *
from Point import *
import matplotlib.pyplot as plt
import os


class ImagesLib:

	# --------------------------------------------------------
	# Variables.
	# --------------------------------------------------------

	original = None
	ndarr = None
	splitsProcessing = SplitsLib()
	vector = None
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

	def extractFeatures(self, user):
		# Variables.
		global original
		horizontalOffset = 4
		verticalOffset = 0
		size = 469
		
		# Attempts to create the new folder.
		if not os.path.exists(user.target):
			os.makedirs(user.target)
			
		# Splits and stores all samples (pre-processing).
		print '\n>Processing digits: ', user.target,
		for x in range (0,10):
			print '->', x,
			vector = FeatureVector()
			
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
				img.save(user.target + '/' + str(x) + str(y) + '.png', 'png')
				self.extractPresence_CoG(img, vector, x)
				self.extractWidthHeight(img, vector, x)
				self.extractSplits(img, vector, x)
				
			# Clear for next iteration.
			user.features.append(vector)
			vector = None
			self.splitsProcessing.process(user, x)
			
			verticalOffset = verticalOffset + size
			self.clearPresence_CoG()
			self.clearWidthHeight()
			self.clearSplits()
				
	# --------------------------------------------------------
	# Processing.
	# --------------------------------------------------------
	
	# Feature extraction WorkFlow.
	def features(self, user):
		self.open(user.path)
		self.extractFeatures(user)
		print
		
	# Function to automatically crop at the size of the digit.
	def autoCrop(self, image):
		bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
		diff = ImageChops.difference(image, bg)
		diff = ImageChops.add(diff, diff, 2.0, -200)
		bbox = diff.getbbox()
		if bbox:
			return image.crop(bbox)
	
	# Fetches and stores width and height for each number.
	def extractWidthHeight(self, image, vector, digit):
		(width, height) = image.size
		vector.width.append(width)
		vector.height.append(height)
	
	# Compute actual width and height features.
	def clearWidthHeight(self):
		self.widthArray = []
		self.HeightArray = []
		
	# Fetches and stores presence for each number.
	def extractPresence_CoG(self, image, vector, digit):
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
		vector.presence.append(percentage)
		vector.CoG.append(Point((horizontalSum / count), (verticalSum / count)))
		
	# Compute actual presence feature.
	def clearPresence_CoG(self):
		self.presence = []
		self.CoG = []
	
	# Prepares the tuple of 6 centers of gravity from horizontal splitting.
	def extractSplits(self, image, vector, digit):
		# HORIZONTAL.
		(width, height) = image.size
		middle = height / 2
		
		# Isolate v0 and v1.
		(h0_x, h0_y) = self.getCoG(image, 0, width, 0, middle)
		h0 = Point(h0_x, h0_y)
		(h1_x, h1_y) = self.getCoG(image, 0, width, middle, height)
		h1 = Point(h1_x, h1_y)
		
		# Isolate v2, v3, v4 and v5.
		(h2_x, h2_y) = self.getCoG(image, 0, h0.x, 0, middle)
		h2 = Point(h2_x, h2_y)
		(h3_x, h3_y) = self.getCoG(image, h0.x, width, 0, middle)
		h3 = Point(h3_x, h3_y)
		(h4_x, h4_y) = self.getCoG(image, 0, h1.x, middle, height)
		h4 = Point(h4_x, h4_y)
		(h5_x, h5_y) = self.getCoG(image, h1.x, width, middle, height)
		h5 = Point(h5_x, h5_y)
		
		# VERTICAL.
		middle = width / 2
		
		# Isolate v0 and v1.
		(v0_x, v0_y) = self.getCoG(image, 0, middle, 0, height)
		v0 = Point(v0_x, v0_y)
		(v1_x, v1_y) = self.getCoG(image, middle, width, 0, height)
		v1 = Point(v1_x, v1_y)
		
		# Isolate v2, v3, v4 and v5.
		(v2_x, v2_y) = self.getCoG(image, 0, middle, 0, v0.y)
		v2 = Point(v2_x, v2_y)
		(v3_x, v3_y) = self.getCoG(image, middle, width, 0, v1.y)
		v3 = Point(v3_x, v3_y)
		(v4_x, v4_y) = self.getCoG(image, 0, middle, v0.y, height)
		v4 = Point(v4_x, v4_y)
		(v5_x, v5_y) = self.getCoG(image, middle, width, v1.y, height)
		v5 = Point(v5_x, v5_y)
		
		# Store results for further processing.
		vector.hSplit.append((h0,h1,h2,h3,h4,h5))
		vector.vSplit.append((v0,v1,v2,v3,v4,v5))
		
	def clearSplits(self):
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
			
			# Append the the right list.
			v0_x.append(v0.x)
			v0_y.append(v0.y)
			v1_x.append(v1.x)
			v1_y.append(v1.y)
			v2_x.append(v2.x)
			v2_y.append(v2.y)
			v3_x.append(v3.x)
			v3_y.append(v3.y)
			v4_x.append(v4.x)
			v4_y.append(v4.y)
			v5_x.append(v5.x)
			v5_y.append(v5.y)
			
		# Reconstruct mean Tuple.
		p0 = Point(np.mean(v0_x),np.mean(v0_y))
		p1 = Point(np.mean(v1_x),np.mean(v1_y))
		p2 = Point(np.mean(v2_x),np.mean(v2_y))
		p3= Point(np.mean(v3_x),np.mean(v3_y))
		p4 = Point(np.mean(v4_x),np.mean(v4_y))
		p5 = Point(np.mean(v5_x),np.mean(v5_y))
		
		return (p0,p1,p2,p3,p4,p5)
