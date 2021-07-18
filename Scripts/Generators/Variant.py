from . import Excercises

class GeneratedVariant:
	'''
	GeneratedVariant - class of generated variant with excercises
	Available arguments:
	- 'excercises': List of all generated excercises for this variant
	'''

	def __init__(self, excercises: list[Excercises.GeneratedExcercise]):
		self.excercises = excercises

	def get_excercises(self):
		'''Function to get all generated excercises for this variant'''
		return self.excercises

	def __iter__(self):
		'''Iterate this class with excercises'''
		for excercise in self.excercises:
			yield excercise

class Variant:
	'''
	Variant - class which combine all available excercises to the one variant
	Available arguments:
	- 'excercises': List of all excercises (objects of class 'Excercise')
	'''

	def __init__(self, excercises: list[Excercises.Excercise]):
		self.excercises = excercises

	def generate_variant(self) -> GeneratedVariant:
		'''Function to generate variant from available excercises'''
		
		excercises = []
		
		for excercise in self.excercises:
			generated_excercise = excercise.generate_tasks()
			excercises.append(generated_excercise)

		return GeneratedVariant(excercises)
