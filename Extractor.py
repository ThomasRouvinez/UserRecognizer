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
mode = raw_input(">RETRAIN NEURAL NETWORKS ? (y/n) -> ")

if mode == 'y':
	# Compute features for all the users.
	user01 = User('.\Users\didier', '.\Users\didier_numbers.png', 1)
	user01.getFeatures()
	users.append(user01)

	user02 = User('.\Users\sabine', '.\Users\sabine_numbers.png', 2)
	user02.getFeatures()
	users.append(user02)
	
	user03 = User('.\Users\jerome', '.\Users\jerome_numbers.png', 3)
	user03.getFeatures()
	users.append(user03)
	
	user04 = User('.\Users\pascal', '.\Users\pascal_numbers.png', 4)
	user04.getFeatures()
	users.append(user04)
	
	user05 = User('.\Users\david', '.\Users\david_numbers.png', 5)
	user05.getFeatures()
	users.append(user05)

	# Train the best models of Neural Networks for each user.
	for user in users:
		# Train neural networks for each digit.
		print '\n>Train model for user', (user.target)
		neuralNets.append(brain.computeModel('', user))
		
	# Serialize users for future use.
	fileObject = open('.\Users\users', 'w')
	pickle.dump(users, fileObject)
	fileObject.close()
		
	print
	print '-' * 75
	print 'PROCESS DONE !'
	
	print
		
elif mode == 'n':
	print '\n>Loading neural networks...'
	
	print '\n>Loading users...'
	fileObject = open('.\Users\users','r')
	temp = pickle.load(fileObject)
	users = temp
	print '>>>Users loaded'
	
	for user in users:
		neuralNets.append(brain.openModel('.\NeuralNets\SavedNet_%d'%(user.key)))
	print '>>>Neural networks loaded.'
	
	testMode = raw_input("(m)anual or (a)utomatic testing ? ->")
		
	# Clear console.
	tmp = sp.call('cls',shell = True)
	
	if testMode == 'm':

		print '-' * 75
		print 'MANUAL SYSTEM READY:\n'
		print '>Users loaded: ', len(users)
		print '>Neural Networks loaded : ', len(neuralNets)

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
						print '>>>User found'
						print '>Activating networks...'
						usrLoop = False
						
				if count >= len(users):
					print '>>> user not found ! Please retry'

			#Command.
			results = []
			
			for net in neuralNets:
				results.append(brain.recognize(net, int(digit_c), chosenUser, int(variation_c)))
				
			print 'Results: ', results 
			
			# Select the closest match.
			bias = chosenUser.key / 18.0
			print 'bias : ', bias
			rounded = min(results, key=lambda x:abs(x - (chosenUser.key+bias)))
			print 'Selected value', rounded
			rounded = round(rounded)
			
			if rounded == 0:
				rounded = 1
			
			for user in users:
				countRec += 1
				if user.key == rounded:
					print '>>> User recognized: ', user.target
					
			if countRec >= len(users):
				print '>>> No results, user is not recognized in DB.'
					
			restart = raw_input("\n\nAdd another input ? (y/n): ")
			
			if restart == 'n':
				recognitions = []
				cmdLoop = False
	else:
	
		print '-' * 75
		print 'AUTOMATIC SYSTEM READY:\n'
		print '>Users loaded: ', len(users)
		print '>Neural Networks loaded : ', len(neuralNets)
		
		for user in users:
			tmp_target = user.target
			percentage = 0.0
			bias = (user.key + (user.key / 12.0))
			print '\nUser: ', user.target, ' with target -> ', bias , '\n'
			
			for digit in range(0,10):
				print '\tDigit: ', digit, ': '
				for variation in range(7,10):
					print '\t\tVariation: ', variation, ': ',
					# Collect data.
					results = []
					lowestDiff = 1000.0
					iter = None
					
					for net in neuralNets:
						results.append(brain.recognize(net, digit, user, variation))
					
					# Compute best match.
					for i in results:
						diff = math.fabs(bias - i)
						
						if diff < lowestDiff:
							lowestDiff = diff
							iter = i
							
					print 'Selected: ', iter,
					
					# Match with best user.
					match = results.index(iter)+1
					
					for user in users:
						if user.key == match:
							if tmp_target == user.target:
								percentage += 3.3333333333
							print user.target
							
			print '\n\tRecognition rate: ', percentage
