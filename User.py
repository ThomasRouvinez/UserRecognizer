#!usr/bin/python

# ------------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.05.2014
# Last modified : 04.05.2014
#
# Description : user object to store target and features.
# ------------------------------------------------------------

from FeatureVector import *
from ImagesLib import *

class User:

	def __init__(self, targetName, pathFile, key):
		self.target = targetName
		self.key = key
		self.path = pathFile
		self.features = []
		self.extractor = ImagesLib()
			
	def getFeatures(self):
		self.extractor.features(self)
		
	def printUser(self, digit):
		print '\n\n>','=' * 110
		print '> FEATURES VECTOR: User', self.target, ', #',digit
		print '>','=' * 110
		
		print '\n\nPresence:\t'
		print self.features[digit].presence
			
		print '\n\nMean width:\t'
		print self.features[digit].width

		print '\n\nMean height:\t'
		print self.features[digit].height
			
		print '\n\nCoG:\t'
		print self.features[digit].CoG
		
		print '\nH1:\t'
		print self.features[digit].h1
		
		print '\nH2:\t'
		print self.features[digit].h2
		
		print '\nH3:\t'
		print self.features[digit].h3
		
		print '\nH4:\t'
		print self.features[digit].h4
		
		print '\nH5:\t'
		print self.features[digit].h5
		
		print '\nH6:\t'
		print self.features[digit].h6
		
		print '\nH7:\t'
		print self.features[digit].h7
		
		print '\nH8:\t'
		print self.features[digit].h8
		
		print '\nV1:\t'
		print self.features[digit].v1
		
		print '\nV2:\t'
		print self.features[digit].v2
		
		print '\nV3:\t'
		print self.features[digit].v3
		
		print '\nV4:\t'
		print self.features[digit].v4
		
		print '\nV5:\t'
		print self.features[digit].v5
		
		print '\nV6:\t'
		print self.features[digit].v6
		
		print '\nV7:\t'
		print self.features[digit].v7
		
		print '\nV8:\t'
		print self.features[digit].v8
		
		print '\nC1:\t'
		print self.features[digit].c1
		
		print '\nC2:\t'
		print self.features[digit].c2
		
		print '\nC3:\t'
		print self.features[digit].c3
				
		print '\n\n>','=' * 110, '\n'
