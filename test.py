#!usr/bin/python

# --------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.04.2014
# Last modified : 04.04.2014
#
# Description : test of the image library.
# --------------------------------------------------------

import sys
from pylab import *
from user import *

# Extract features for each user.
didier = user('didier', 'didier_numbers.png')
didier.getFeatures()