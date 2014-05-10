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

# Launch testing interface.
while(cmdLoop):
	tmp = sp.call('cls',shell=True)

	print 'SYSTEM READY:\n'
	
	# Find right user.
	while(usrLoop):
		count = -1
		digit_c = raw_input("SELECT a number: ")
		user_c = raw_input("FROM user in database (name): ")
		variation_c = raw_input("ON variation: ")
		print

		for user in users:
			count += 1
			if user.target == user_c:
				chosenUser = count
				print 'RETURN: user found'
				
		if count >= len(user):
			'RETURN: user not found ! Please retry'

	#Command.
	result = brain.recognize(neuralNets[digit_c], digit_c, chosenUser, variation_c)

	# Identify closest user.
	round = round(result)

	for user in users:
		if user.key == round:
			print 'User recognized: ', user.target
			
	restart = raw_input("\n\nRestart ? (y/n): ")
	if restart == n:
		cmdLoop = False
