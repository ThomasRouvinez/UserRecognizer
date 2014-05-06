#!usr/bin/python

# ------------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 01.05.2014
# Last modified : 01.05.2014
#
# Description : feature vector object.
# ------------------------------------------------------------

from point import *

class featureVector:
	# Statistical features.
	presence = []	# Black color percentage.
	width = []		# Mean digit width.
	height = []		# Mean digit height.
	CoG = []		# Center of gravity.
	
	# Horizontal split features.
	h1 = [] 		# Angle difference (h0,h1),(h2,h3))
	h2 = [] 		# Angle difference (h0,h1),(h4,h5))
	h3 = []			# Angle difference (h2,h3),(h4,h5))
	h4 = []			# Angle difference (h2,h3), horizontal)
	h5 = []			# Angle difference (h4,h5), horizontal)
	h6 = []			# h0 and h1 alignment.
	h7 = []			# h2 and h3 alignment.
	h8 = []			# h4 and h5 alignment.
	
	# Vertical split features.
	v1 = []			# Angle difference (v0,v1),(v2,v3))
	v2 = []			# Angle difference (v0,v1),(v4,v5))
	v3 = []			# Angle difference (v2,v3),(v4,v5))
	v4 = []			# Angle difference (v2,v3), vertical)
	v5 = []			# Angle difference (v4,v5), vertical)
	v6 = []			# v0 and v1 alignment.
	v7 = []			# v2 and v3 alignment.
	v8 = []			# v4 and v5 alignment.
	
	# Combined split features.
	c1 = []			# Angle difference (h0,h1),(v0,v1))
	c2 = []			# Angle difference (h2,h3),(v2,v3))
	c3 = []			# Angle difference (h4,h5),(v4,v5))