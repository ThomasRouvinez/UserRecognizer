#!usr/bin/python

# ------------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.04.2014
# Last modified : 04.04.2014
#
# Description : image library with split and feature extraction
# functions.
# ------------------------------------------------------------

from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
import os


class imagesLib:

	# --------------------------------------------------------
	# Variables.
	# --------------------------------------------------------

	original = None
	ndarr = None
	
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
			print ">Image loaded"
		except:
			print "Unable to load image"

	def export(self):
		global ndarr
		
		try:
			imported = Image.fromarray(ndarr)
			imported.save('export.png', 'png')
		except:
			print "\n\n>Export failed !"

	def split(self, folderName):
		# Variables.
		global original
		horizontalOffset = 4
		verticalOffset = 0
		size = 469
		
		# Attempts to create the new folder.
		if not os.path.exists(folderName):
			os.makedirs(folderName)
			
		# Split and store all samples.
		for x in range (0,10):
			for y in range (0,10):
				# For each cell, split it.
				box = (horizontalOffset, verticalOffset, (horizontalOffset+size), (verticalOffset+size))
				horizontalOffset = (4 + y * size)
				copy = original
				cropped = copy.crop(box)
				
				# Perform actions on each digit.
				cropped.save(folderName+ '/' + str(x) + str(y) + '.png', 'png')
			verticalOffset = verticalOffset + size
	# --------------------------------------------------------
	# Processing.
	# --------------------------------------------------------
	
	def features(self, path, folderName):
		self.open(path)
		self.split(folderName)