#!/usr/bin/env python

import math
import random
import matplotlib
from pylab import plot, legend, subplot, grid, xlabel, ylabel, show, title

from pyneurgen.grammatical_evolution import GrammaticalEvolution
from pyneurgen.fitness import FitnessElites, FitnessTournament
from pyneurgen.fitness import ReplacementTournament, MAX, MIN, CENTER
from pyneurgen.neuralnet import NeuralNet

class NeuralGen:
		
	def computeModel(self, path, users, digit):
		bnf =   """
		<model_name>        ::= digit<member_no>.nn
		<max_hnodes>        ::= 40
		<node_type>         ::= sigmoid | linear | tanh
		<positive-real>     ::= 0.<int-const>
		<int-const>         ::= <int-const> | 1 | 2 | 3 | 4 | 5 | 6 |
								7 | 8 | 9 | 0
		<sign>              ::= + | -
		<max_epochs>        ::= 1000
		<starting_weight>   ::= <sign> 0.<int-const> | <sign> 1.<int-const> |
								<sign> 2.<int-const> | <sign> 3.<int-const> |
								<sign> 4.<int-const> | <sign> 5.<int-const>
		<learn_rate>        ::= 0.<int-const>
		<saved_name>        ::= None
		<S>                 ::=
		
		import math
		import random
		from pyneurgen.neuralnet import NeuralNet
		from pyneurgen.nodes import Node, BiasNode, CopyNode, Connection
		from pyneurgen.layers import Layer
		from pyneurgen.recurrent import JordanRecurrent

		net = NeuralNet()
		hidden_nodes = max(int(round(<positive-real> * float(<max_hnodes>))), 1)

		net.init_layers(len(self.all_inputs[0]),[hidden_nodes], len(self.all_targets[0]))
		net.layers[1].set_activation_type('<node_type>')
		net.output_layer.set_activation_type('<node_type>')

		# Use the genotype to get starting weights
		for layer in net.layers[1:]:
			for node in layer.nodes:
				for conn in node.input_connections:
					# Every time it is asked, another starting weight is given.
					conn.set_weight(self.runtime_resolve('<starting_weight>', 'float'))

		# Note the injection of data from the genotype
		net.set_all_inputs(self.all_inputs)
		net.set_all_targets(self.all_targets)

		length = len(self.all_inputs)
		learn_end_point = int(length * .6)
		validation_end_point = int(length * .8)

		net.set_learn_range(0, learn_end_point)

		net.set_validation_range(0, learn_end_point)
		net.set_validation_range(learn_end_point + 1, validation_end_point)
		net.set_test_range(validation_end_point + 1, length - 1)

		net.set_learnrate(<learn_rate>)
		epochs = int(round(<positive-real> * float(<max_epochs>)))

		if epochs > 0:
			# Use learning to further set the weights
			net.learn(epochs=epochs, show_epoch_results=True, random_testing=False)

		#   Use validation for generating the fitness value
		mse = net.validate(show_sample_interval=0)
		print "mse", mse
		modelname = self.runtime_resolve('<model_name>', 'str')
		net.save(modelname)
		self.set_bnf_variable('<saved_name>', modelname)

		self.net = net
		fitness = mse
		self.set_bnf_variable('<fitness>', fitness)
					"""
		
		# Prepare the parameters of the Genetic Algorithm.
		ges = GrammaticalEvolution()
		ges.set_bnf(bnf)
		ges.set_genotype_length(start_gene_length=5, max_gene_length=24)
		ges.set_population_size(len(users)*10)
		ges.set_max_generations(20)
		ges.set_fitness_type('center', 0.01)
		ges.set_max_program_length(4000)
		ges.set_wrap(True)
		ges.set_fitness_fail(2.0)
		ges.set_mutation_type('m')
		ges.set_max_fitness_rate(.25)
		ges.set_mutation_rate(.025)
		ges.set_fitness_selections(FitnessElites(ges.fitness_list, .05), FitnessTournament(ges.fitness_list, tournament_size=2))
		ges.set_crossover_rate(.2)
		ges.set_children_per_crossover(2)
		ges.set_replacement_selections(ReplacementTournament(ges.fitness_list, tournament_size=3))
		ges.set_maintain_history(True)
		ges.set_timeouts(10, 360)
		
		# Create the genotypes.
		ges.create_genotypes()

		# Initialize input buffers for the Neural Network.
		all_inputs = []
		all_targets = []
	
		# Create inputs for the given digit.
		for user in users:
			for variation in range(0,10):
				# Pass all the features as inputs.
				all_inputs.append([float(user.features[digit].presence[variation]),
									float(user.features[digit].width[variation]),
									float(user.features[digit].height[variation]),
									float(user.features[digit].CoG[variation].x),
									float(user.features[digit].CoG[variation].y),
									float(user.features[digit].h1[variation]),
									float(user.features[digit].h2[variation]),
									float(user.features[digit].h3[variation]),
									float(user.features[digit].h4[variation]),
									float(user.features[digit].h5[variation]),
									float(user.features[digit].h6[variation]),
									float(user.features[digit].h7[variation]),
									float(user.features[digit].h8[variation]),
									float(user.features[digit].v1[variation]),
									float(user.features[digit].v2[variation]),
									float(user.features[digit].v3[variation]),
									float(user.features[digit].v4[variation]),
									float(user.features[digit].v5[variation]),
									float(user.features[digit].v6[variation]),
									float(user.features[digit].v7[variation]),
									float(user.features[digit].v8[variation]),
									float(user.features[digit].c1[variation]),
									float(user.features[digit].c2[variation]),
									float(user.features[digit].c3[variation])])
				
				# Set the right target for training.
				all_targets.append(user.target)
	
		# Give the inputs to the Genetic Algorithm.
		for g in ges.population:
			g.all_inputs = all_inputs
			g.all_targets = all_targets
			
		# Start the training.
		ges.run()
		print ges.fitness_list.sorted(),'\n'
		
		g = ges.population[ges.fitness_list.best_member()]
		program = g.local_bnf['program']
		
		saved_model = g.local_bnf['<saved_name>'][0]
		
		# Create a new Neural Network from the trained model.
		#net = NeuralNet()
		#net.load(saved_model)
		#
		#net.set_all_inputs(all_inputs)
		#net.set_all_targets(all_targets)
		#
		#test_start_point = int(pop_len * .8) + 1
		#net.set_test_range(test_start_point, pop_len - 1)
		#mse = net.test()