#!usr/bin/python

# --------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.04.2014
# Last modified : 04.04.2014
#
# Description : test of the image library.
# --------------------------------------------------------

from imagesLib import *
import sys
from pylab import *


# Create new instance of library and load the full grid.
s = imagesLib()

s.features('didier_numbers.png', 'didier')