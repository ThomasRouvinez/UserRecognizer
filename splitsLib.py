#!usr/bin/python

# ------------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.05.2014
# Last modified : 04.05.2014
#
# Description : splits features computation helpers.
# ------------------------------------------------------------

from math import atan2, degrees, pi, acos, sqrt
import numpy as np
from Point import *

class SplitsLib:
	def process(self, user, digit):
		self.compileHorizontal(user, digit)
		self.compileVertical(user, digit)
		self.compileCombined(user, digit)
	
	def compileHorizontal(self, user, digit):
		# Prepare vectors for horizontal lines.
		hVector_x = Point(0,0)
		hVector_y = Point(1,0)
	
		# Foreach digit in the grid.
		for value in user.features[digit].hSplit:
			(h0, h1, h2, h3, h4, h5) = value
			
			# Compute features.
			user.features[digit].h1.append(self.getAngleVectors(h0, h1, h2, h3))
			user.features[digit].h2.append(self.getAngleVectors(h0, h1, h4, h5))
			user.features[digit].h3.append(self.getAngleVectors(h2, h3, h4, h5))
			
			user.features[digit].h4.append(self.getAngleVectors(h2, h3, hVector_x, hVector_y))
			user.features[digit].h5.append(self.getAngleVectors(h4, h5, hVector_x, hVector_y))
			
			user.features[digit].h6.append(self.getAngle(h0,h1))
			user.features[digit].h7.append(self.getAngle(h2,h3))
			user.features[digit].h8.append(self.getAngle(h4,h5))
			
	def compileVertical(self, user, digit):
		# Prepare vectors for vertical lines.
		vVector_x = Point(0,0)
		vVector_y = Point(0,1)
	
		# Foreach digit in the grid.
		for value in user.features[digit].vSplit:
			(v0, v1, v2, v3, v4, v5) = value
			
			# Compute feature h6.
			user.features[digit].v1.append(self.getAngleVectors(v0, v1, v2, v3))
			user.features[digit].v2.append(self.getAngleVectors(v0, v1, v4, v5))
			user.features[digit].v3.append(self.getAngleVectors(v2, v3, v4, v5))
			
			user.features[digit].v4.append(self.getAngleVectors(v2, v3, vVector_x, vVector_y))
			user.features[digit].v5.append(self.getAngleVectors(v4, v5, vVector_x, vVector_y))
			
			user.features[digit].v6.append(self.getAngle(v0,v1))
			user.features[digit].v7.append(self.getAngle(v2,v3))
			user.features[digit].v8.append(self.getAngle(v4,v5))
			
	def compileCombined(self, user, digit):
	
		# Foreach digit in the grid.
		for x in range(0,len(user.features[0].hSplit)):
			(h0, h1, h2, h3, h4, h5) = user.features[digit].hSplit[x]
			(v0, v1, v2, v3, v4, v5) = user.features[digit].vSplit[x]
			
			# Compute feature h6.
			user.features[digit].c1.append(self.getAngleVectors(h0, h1, v0, v1))
			user.features[digit].c2.append(self.getAngleVectors(h2, h3, v2, v3))
			user.features[digit].c3.append(self.getAngleVectors(h4, h5, v4, v5))
			
	# Helper to compute the angle between two points.
	def getAngle(self, dx, dy):
		xDiff = dy.x - dx.x
		yDiff= dy.y - dx.y
		
		return degrees(atan2(yDiff,xDiff))
	
	# Helper to compute the angle between two vectors.
	def getAngleVectors(self, p0, p1, p2, p3):
		vector0 = [p1.x - p0.x, p1.y - p0.y]
		vector1 = [p3.x - p2.x, p3.y - p2.y]
		
		vectorLength = (self.getVectorLength(vector0) * self.getVectorLength(vector1))
		
		# We clip values going beyond [-1,1].
		if vectorLength != 0:
			return degrees(acos(max(min(self.getDotProduct(vector0, vector1), 1), -1) / vectorLength))
		else:
			return degrees(acos(0.0))
	
	def getDotProduct(self, vector1, vector2):
		return sum((a*b) for a, b in zip(vector1, vector2))
		
	def getVectorLength(self, vector):
		return sqrt(self.getDotProduct(vector, vector))