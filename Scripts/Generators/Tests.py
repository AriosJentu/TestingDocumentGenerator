from Scripts.Generators import Excercises

class GeneratedTest:
	'''
	GeneratedTest - class of generated test option with excercises
	Available arguments:
	- 'excercises': List of all generated excercises for this test option
	'''

	def __init__(self, excercises: list[Excercises.GeneratedExcercise]):
		self.excercises = excercises


	#@Getters
	def get_excercises(self):
		'''Function to get all generated excercises for this test'''
		return self.excercises


	#@Override
	def __iter__(self):
		'''Iterate this class with excercises'''
		for excercise in self.excercises:
			yield excercise


class Test:
	'''
	Test - class which combine all available excercises to the one test option
	Available arguments:
	- 'excercises': List of all excercises (objects of class 'Excercise')
	- 'is_all_tasks': Key for creating all available tasks in files 
		(for debug, if True - generate ALL tasks from files, 
		by default it's False - generate tasks as default)
	'''

	def __init__(self, 
			excercises: list[Excercises.Excercise] = None, 
			is_all_tasks: bool = False
	):
		if not excercises:
			excercises = []

		self.excercises = excercises
		self.is_all_tasks = is_all_tasks
		self.set_all_tasks_generation(self.is_all_tasks)


	#@Setters
	def append(self, excercise: Excercises.Excercise):
		'''Function to add excercise into this test'''
		excercise.set_all_tasks_generation(self.is_all_tasks)
		self.excercises.append(excercise)

	def add_prefix_path(self, prefix_path: str):
		'''Function to add prefix path for excercises in this test'''
		for excercise in self.excercises:
			excercise.add_prefix_path(prefix_path)

	def set_all_tasks_generation(self, is_all_tasks: bool = False):
		'''Function to set variable of generating all tasks'''
		self.is_all_tasks = is_all_tasks
		for excercise in self.excercises:
			excercise.set_all_tasks_generation(self.is_all_tasks)


	#@Getters
	def get_excercises(self):
		'''Function to get all excercises formats for this test'''
		return self.excercises


	#@Generators
	def generate_test(self) -> GeneratedTest:
		'''Function to generate test option from available excercises'''
		
		excercises = []
		
		for excercise in self.excercises:
			generated_excercise = excercise.generate_excercise()
			excercises.append(generated_excercise)

		return GeneratedTest(excercises)

