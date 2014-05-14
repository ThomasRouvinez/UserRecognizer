#!usr/bin/python

# --------------------------------------------------------
# Author : Thomas Rouvinez
# Creation date : 04.05.2014
# Last modified : 04.05.2014
#
# Description : neural networks for training and validation.
# --------------------------------------------------------

from pylab import plot, hold, show
from scipy import sin, rand, arange
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets import SequenceClassificationDataSet
from pybrain.structure.modules import LSTMLayer, SoftmaxLayer
from pybrain.supervised import RPropMinusTrainer
from pybrain.tools.validation import testOnSequenceData
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SequentialDataSet
from pybrain.structure import SigmoidLayer
from pybrain.structure import LSTMLayer
import pickle
		 
class PyBrain:
	
	def computeModel(self, path, user):
		# Create a supervised dataset for training.
		trndata = SupervisedDataSet(24, 1)
		tstdata = SupervisedDataSet(24, 1)
		
		#Fill the dataset.
		for number in range(0,10):
			for variation in range(0,7):
				# Pass all the features as inputs.
				trndata.addSample(self.getSample(user, number, variation),(user.key,))
				
			for variation in range(7,10):
				# Pass all the features as inputs.
				tstdata.addSample(self.getSample(user, number, variation),(user.key,))
				
		# Build the LSTM.
		n = buildNetwork(24, 50, 1, hiddenclass=LSTMLayer, recurrent=True, bias=True)

		# define a training method
		trainer = BackpropTrainer(n, dataset = trndata, momentum=0.99, learningrate=0.00002)

		# carry out the training
		trainer.trainOnDataset(trndata, 2000)
		valueA = trainer.testOnData(tstdata)
		print '\tMSE -> {0:.2f}'.format(valueA)
		self.saveModel(n, '.\NeuralNets\SavedNet_%d' %(user.key))
		
		return n
		
	# Function to save a model when computed.
	def saveModel(self, net, path):
		fileObject = open(path, 'w')
		pickle.dump(net, fileObject)
		fileObject.close()
	
	# Function to open a previously saved NN.
	def openModel(self, path):
		fileObject = open(path,'r')
		net = pickle.load(fileObject)
		return net
	
	# Function to query the created NN.
	def recognize(self, neuralNet, digit, user, variation):
		return neuralNet.activate(self.getSample(user, digit, variation))
		
	# Function to get a sample feature vector from the database.
	def getSample(self, user, digit, variation):
		data = []
	
		# Pass all the features as inputs.
		data.append(user.features[digit].presence[variation])
		data.append(user.features[digit].width[variation])
		data.append(user.features[digit].height[variation])
		data.append(user.features[digit].CoG[variation].x)
		data.append(user.features[digit].CoG[variation].y)
		data.append(user.features[digit].h1[variation])
		data.append(user.features[digit].h2[variation])
		data.append(user.features[digit].h3[variation])
		data.append(user.features[digit].h4[variation])
		data.append(user.features[digit].h5[variation])
		data.append(user.features[digit].h6[variation])
		data.append(user.features[digit].h7[variation])
		data.append(user.features[digit].h8[variation])
		data.append(user.features[digit].v1[variation])
		data.append(user.features[digit].v2[variation])
		data.append(user.features[digit].v3[variation])
		data.append(user.features[digit].v4[variation])
		data.append(user.features[digit].v5[variation])
		data.append(user.features[digit].v6[variation])
		data.append(user.features[digit].v7[variation])
		data.append(user.features[digit].v8[variation])
		data.append(user.features[digit].c1[variation])
		data.append(user.features[digit].c2[variation])
		data.append(user.features[digit].c3[variation])
		
		return data