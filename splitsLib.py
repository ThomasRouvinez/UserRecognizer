#!usr/bin/python

# ------------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.05.2014
# Last modified : 04.05.2014
#
# Description : splits features computation helpers.
# ------------------------------------------------------------

from math import atan2, degrees, pi, acos, sqrt
from point import *

class splitsLib:
	def process(self, vector):
		print '\n>Process splits'
		self.compileHorizontal(vector)
		self.compileVertical(vector)
		self.compileCombined(vector)
	
	def compileHorizontal(self, vector):
		# Prepare vectors for horizontal lines.
		hVector_x = point(0,0)
		hVector_y = point(1,0)
	
		# Foreach digit.
		for digit in vector.hSplit:
			(h0, h1, h2, h3, h4, h5) = digit
			
			# Compute features.
			vector.h1.append(self.getAngleVectors(h0, h1, h2, h3))
			vector.h2.append(self.getAngleVectors(h0, h1, h4, h5))
			vector.h3.append(self.getAngleVectors(h2, h3, h4, h5))
			
			vector.h4.append(self.getAngleVectors(h2, h3, hVector_x, hVector_y))
			vector.h5.append(self.getAngleVectors(h4, h5, hVector_x, hVector_y))
			
			vector.h6.append(self.getAngle(h0,h1))
			vector.h7.append(self.getAngle(h2,h3))
			vector.h8.append(self.getAngle(h4,h5))
			
	def compileVertical(self, vector):
		# Prepare vectors for vertical lines.
		vVector_x = point(0,0)
		vVector_y = point(0,1)
	
		# Foreach digit.
		for digit in vector.vSplit:
			(v0, v1, v2, v3, v4, v5) = digit
			
			# Compute feature h6.
			vector.v1.append(self.getAngleVectors(v0, v1, v2, v3))
			vector.v2.append(self.getAngleVectors(v0, v1, v4, v5))
			vector.v3.append(self.getAngleVectors(v2, v3, v4, v5))
			
			vector.v4.append(self.getAngleVectors(v2, v3, vVector_x, vVector_y))
			vector.v5.append(self.getAngleVectors(v4, v5, vVector_x, vVector_y))
			
			vector.v6.append(self.getAngle(v0,v1))
			vector.v7.append(self.getAngle(v2,v3))
			vector.v8.append(self.getAngle(v4,v5))
			
	def compileCombined(self, vector):
		# Foreach digit.
		for digit in range(0,len(vector.hSplit)):
			(h0, h1, h2, h3, h4, h5) = vector.hSplit[digit]
			(v0, v1, v2, v3, v4, v5) = vector.vSplit[digit]
			
			# Compute feature h6.
			vector.c1.append(self.getAngleVectors(h0, h1, v0, v1))
			vector.c2.append(self.getAngleVectors(h2, h3, v2, v3))
			vector.c3.append(self.getAngleVectors(h4, h5, v4, v5))
			
	# Helper to compute the angle between two points.
	def getAngle(self, dx, dy):
		xDiff = dy.x - dx.x
		yDiff= dy.y - dx.y
		
		return degrees(atan2(yDiff,xDiff))
	
	# Helper to compute the angle between two vectors.
	def getAngleVectors(self, p0, p1, p2, p3):
		vector0 = [p1.x - p0.x, p1.y - p0.y]
		vector1 = [p3.x - p2.x, p3.y - p2.y]
		
		return degrees(acos(self.getDotProduct(vector0, vector1) / (self.getVectorLength(vector0) * self.getVectorLength(vector1))))
	
	def getDotProduct(self, vector1, vector2):
		return sum((a*b) for a, b in zip(vector1, vector2))
		
	def getVectorLength(self, vector):
		return sqrt(self.getDotProduct(vector, vector))