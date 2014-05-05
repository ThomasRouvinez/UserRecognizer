#!usr/bin/python

# ------------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 01.05.2014
# Last modified : 01.05.2014
#
# Description : feature vector object.
# ------------------------------------------------------------

from Point import *

class FeatureVector:
	def __init__(self):
		self.hSplit = []
		self.vSplit = []
		
		# Statistical features.
		self.presence = []	# Black color percentage.
		self.width = []		# Mean digit width.
		self.height = []	# Mean digit height.
		self.CoG = []		# Center of gravity.
		
		# Horizontal split features.
		self.h1 = [] 		# Angle difference (h0,h1),(h2,h3))
		self.h2 = [] 		# Angle difference (h0,h1),(h4,h5))
		self.h3 = []		# Angle difference (h2,h3),(h4,h5))
		self.h4 = []		# Angle difference (h2,h3), horizontal)
		self.h5 = []		# Angle difference (h4,h5), horizontal)
		self.h6 = []		# h0 and h1 alignment.
		self.h7 = []		# h2 and h3 alignment.
		self.h8 = []		# h4 and h5 alignment.
		
		# Vertical split features.
		self.v1 = []		# Angle difference (v0,v1),(v2,v3))
		self.v2 = []		# Angle difference (v0,v1),(v4,v5))
		self.v3 = []		# Angle difference (v2,v3),(v4,v5))
		self.v4 = []		# Angle difference (v2,v3), vertical)
		self.v5 = []		# Angle difference (v4,v5), vertical)
		self.v6 = []		# v0 and v1 alignment.
		self.v7 = []		# v2 and v3 alignment.
		self.v8 = []		# v4 and v5 alignment.
		
		# Combined split features.
		self.c1 = []		# Angle difference (h0,h1),(v0,v1))
		self.c2 = []		# Angle difference (h2,h3),(v2,v3))
		self.c3 = []		# Angle difference (h4,h5),(v4,v5))