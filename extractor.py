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
user01 = User('didier', 'didier_numbers.png')
user01.getFeatures()
users.append(user01)

# Train the best models of Neural Networks for each type of digit.
for number in range(0,trainingSetSize):
	# Train a full neural network.
	print '\n>Train model for digit', (number+1)
	classifier.computeModel('', users, number)