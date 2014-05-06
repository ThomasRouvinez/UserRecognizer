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

# Variables.
features = []
extractor = imagesLib()

# Extract features for each user.
features.append(extractor.features('didier_numbers.png', 'didier'))

# Classification (to be done).