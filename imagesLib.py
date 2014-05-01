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
		for x in range (0,10):
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
				self.extractPresence(img)
				self.extractWidthHeight(img)
				
			verticalOffset = verticalOffset + size
			
			# Compile results for all 10 version of each digit.
			self.compilePresence()
			self.compileWidthHeight()
			
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
	def extractPresence(self, image):
		count = 0
		(width, height) = image.size
		
		for i in range(width):
			for j in range(height):
				if((image.getpixel((i,j)))[0] < 50):
					count += 1
					
		percentage = (count * 100) / (width * height)			
		self.presence.append(percentage)
		
	# Compute actual presence feature.
	def compilePresence(self):
		self.vector.presence.append(np.mean(self.presence))
		self.presence = []
		
	# Fetches and stores naive Center-Of-Gravity for each number.
	def extractNaiveCOG(self, image):
		(width, height) = image.size

	# Compiles features for display.
	def displayFeatures(self):
		print '\n\n>','=' * 110
		print '\n> Feature Vector.'
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
			
		print '\n\n>','=' * 110, '\n'