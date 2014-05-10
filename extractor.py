#!usr/bin/python

# --------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.04.2014
# Last modified : 04.04.2014
#
# Description : test of the image library.
# --------------------------------------------------------

import sys
import subprocess as sp
from pylab import *
from User import *
from PyBrain import *
import pickle
import numpy as np

# Variables.
users = []
chosenUser = None
recognizedUser = -1

neuralNets = []
brain = PyBrain()
trainingSetSize = 7

recognitions = []

cmdLoop = True
usrLoop = True

# Features extraction and NN training.
print '-' * 75
mode = raw_input("RETRAIN NEURAL NETWORKS ? (y/n) -> ")

if mode == 'y':
	# Compute features for all the users.
	user01 = User('.\Users\didier', '.\Users\didier_numbers.png', 1)
	user01.getFeatures()
	users.append(user01)

	user02 = User('.\Users\sabine', '.\Users\sabine_numbers.png', 2)
	user02.getFeatures()
	users.append(user02)

	# Train the best models of Neural Networks for each type of digit.
	for number in range(0,10):
		# Train neural networks for each digit.
		print '\n>Train model for digit', (number)
		neuralNets.append(brain.computeModel('', users, number))
		
	# Serialize users for future use.
	fileObject = open('.\Users\users', 'w')
	pickle.dump(users, fileObject)
	fileObject.close()
		
	print
	print '-' * 75
	print 'PROCESS DONE !'
	print '-' * 75
		
elif mode == 'n':
	print 'Loading neural networks...'
	for i in range(0,10):
		neuralNets.append(brain.openModel('.\NeuralNets\SavedNet_%d' %(i)))
		
	print 'Loading users...'
	fileObject = open('.\Users\users','r')
	temp = pickle.load(fileObject)
	users = temp
	
	tmp = sp.call('cls',shell = True)
	print 'SYSTEM READY:\n'
		
	# Launch testing interface.
	while(cmdLoop):
		usrLoop = True
		
		# Find right user.
		while(usrLoop):
			print '-' * 75, '\n'
			count = -1
			countRec = -1
			digit_c = raw_input("SELECT number: ")
			user_c = raw_input("FROM user in database (name): ")
			variation_c = raw_input("ON variation: ")
			print

			for user in users:
				count += 1
				if user.target == user_c:
					chosenUser = user
					print '>>> User found'
					print '>>> Activating network...'
					usrLoop = False
					
			if count >= len(users):
				print '>>> user not found ! Please retry'

		#Command.
		result = brain.recognize(neuralNets[int(digit_c)], int(digit_c), chosenUser, int(variation_c))
		recognitions.append(result)
		print '>>> Factor : ', recognitions, '\n'

		# Identify closest user.
		sum = 0.0
		
		for factor in recognitions:
			sum += factor
			
		cumulatedScore = sum / len(recognitions)
		print '>>> AVG Score: ', cumulatedScore
		
		rounded = round(cumulatedScore)
		print '>>> Rounded', rounded

		for user in users:
			countRec += 1
			if user.key == rounded:
				print 'User recognized: ', user.target
				
		if countRec >= len(users):
			print '>>> No results, user is not recognized in DB.'
				
		restart = raw_input("\n\nAdd another input ? (y/n): ")
		
		if restart == 'n':
			recognitions = []
			cmdLoop = False