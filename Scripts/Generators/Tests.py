from . import Excercises

class GeneratedTest:
	'''
	GeneratedTest - class of generated test option with excercises
	Available arguments:
	- 'excercises': List of all generated excercises for this test option
	'''

	def __init__(self, excercises: list[Excercises.GeneratedExcercise]):
		self.excercises = excercises

	def get_excercises(self):
		'''Function to get all generated excercises for this test'''
		return self.excercises

	def __iter__(self):
		'''Iterate this class with excercises'''
		for excercise in self.excercises:
			yield excercise

class Test:
	'''
	Test - class which combine all available excercises to the one test option
	Available arguments:
	- 'excercises': List of all excercises (objects of class 'Excercise')
	'''

	def __init__(self, excercises: list[Excercises.Excercise] = []):
		self.excercises = excercises

	def add(self, excercise: Excercises.Excercise):
		'''Function to add excercise into this test'''
		self.excercises.append(excercise)

	def get_excercises(self):
		'''Function to get all excercises formats for this test'''
		return self.excercises

	def generate_test(self) -> GeneratedTest:
		'''Function to generate test option from available excercises'''
		
		excercises = []
		
		for excercise in self.excercises:
			generated_excercise = excercise.generate_tasks()
			excercises.append(generated_excercise)

		return GeneratedTest(excercises)

	def add_prefix_path(self, prefix_path: str):
		'''Function to add prefix path for excercises in this test'''
		for excercise in self.excercises:
			excercise.add_prefix_path(prefix_path)
