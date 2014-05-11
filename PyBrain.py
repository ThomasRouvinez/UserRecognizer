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
		 
class PyBrain:
	
	def computeModel(self, path, users, digit):
		# Create a supervised dataset for training.
		trndata = SupervisedDataSet(24, 1)
		tstdata = SupervisedDataSet(24, 1)
		
		#Fill the dataset.
		for user in users:
			for variation in range(0,7):
				# Pass all the features as inputs.
				trndata.addSample((user.features[digit].presence[variation], 
				user.features[digit].width[variation],
				user.features[digit].height[variation],
				user.features[digit].CoG[variation].x,
				user.features[digit].CoG[variation].y,
				user.features[digit].h1[variation],
				user.features[digit].h2[variation],
				user.features[digit].h3[variation],
				user.features[digit].h4[variation],
				user.features[digit].h5[variation],
				user.features[digit].h6[variation],
				user.features[digit].h7[variation],
				user.features[digit].h8[variation],
				user.features[digit].v1[variation],
				user.features[digit].v2[variation],
				user.features[digit].v3[variation],
				user.features[digit].v4[variation],
				user.features[digit].v5[variation],
				user.features[digit].v6[variation],
				user.features[digit].v7[variation],
				user.features[digit].v8[variation],
				user.features[digit].c1[variation],
				user.features[digit].c2[variation],
				user.features[digit].c3[variation]),(user.key,))
				
			for variation in range(7,10):
				# Pass all the features as inputs.
				tstdata.addSample((user.features[digit].presence[variation], 
				user.features[digit].width[variation],
				user.features[digit].height[variation],
				user.features[digit].CoG[variation].x,
				user.features[digit].CoG[variation].y,
				user.features[digit].h1[variation],
				user.features[digit].h2[variation],
				user.features[digit].h3[variation],
				user.features[digit].h4[variation],
				user.features[digit].h5[variation],
				user.features[digit].h6[variation],
				user.features[digit].h7[variation],
				user.features[digit].h8[variation],
				user.features[digit].v1[variation],
				user.features[digit].v2[variation],
				user.features[digit].v3[variation],
				user.features[digit].v4[variation],
				user.features[digit].v5[variation],
				user.features[digit].v6[variation],
				user.features[digit].v7[variation],
				user.features[digit].v8[variation],
				user.features[digit].c1[variation],
				user.features[digit].c2[variation],
				user.features[digit].c3[variation]),(user.key,))
		
		# Build the LSTM.
		n = buildNetwork(24, 30, 1, hiddenclass=LSTMLayer, recurrent=True, bias=True)

		# define a training method
		trainer = BackpropTrainer(n, dataset = trndata, momentum=0.9, learningrate=0.00001)

		# carry out the training
		trainer.trainOnDataset(trndata, 2000)
		valueA = trainer.testOnData(tstdata)
		print '\tMSE -> {0:.2f}'.format(valueA)
		
		return n
		
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