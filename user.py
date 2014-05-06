#!usr/bin/python

# ------------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.05.2014
# Last modified : 04.05.2014
#
# Description : user object to store target and features.
# ------------------------------------------------------------

from featureVector import *
from imagesLib import *

class user:
	
	target = None
	path = None
	features = []
	extractor = imagesLib()
	
	def __init__(self, targetName, pathFile):
		self.target = targetName
		self.path = pathFile
		
		for x in range(0, 10):
			vector = featureVector()
			features.append(vector)
			
	def getFeatures(self):
		extractor.features(didier)