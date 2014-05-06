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
from User import *
from NeuralGen import *

# Variables.
users = []
classifier = NeuralGen()
trainingSetSize = 7

# Extract features for each user.
user01 = User('didier', 's_didier_numbers.png')
user01.getFeatures()
users.append(user01)

#user02 = User('sabine', 's_sabine_numbers.png')
#user02.getFeatures()
#users.append(user02)

# Train the best models of Neural Networks for each type of digit.
for number in range(0,1):
	# Train a full neural network.
	print '\n>Train model for digit', (number)
	classifier.computeModel('', users, number)