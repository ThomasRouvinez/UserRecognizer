#!usr/bin/python

# ------------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.05.2014
# Last modified : 04.05.2014
#
# Description : point structure.
# ------------------------------------------------------------

class Point:

	def __init__(self, dx, dy):
		self.x = dx
		self.y = dy
		
	def printPoint(self):
		print 'X:', self.x, '- Y:', self.y,'|',