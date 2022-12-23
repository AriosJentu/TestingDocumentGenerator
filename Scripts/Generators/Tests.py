from Scripts.Generators import Exercises

class GeneratedTest:
	'''
	GeneratedTest - class of generated test option with exercises
	Available arguments:
	- 'exercises': List of all generated exercises for this test option
	'''

	def __init__(self, exercises: list[Exercises.GeneratedExercise]):
		self.exercises = exercises


	#@Getters
	def get_exercises(self):
		'''Function to get all generated exercises for this test'''
		return self.exercises


	#@Override
	def __iter__(self):
		'''Iterate this class with exercises'''
		for exercise in self.exercises:
			yield exercise


class Test:
	'''
	Test - class which combine all available exercises to the one test option
	Available arguments:
	- 'exercises': List of all exercises (objects of class 'Exercise')
	- 'is_all_tasks': Key for creating all available tasks in files 
		(for debug, if True - generate ALL tasks from files, 
		by default it's False - generate tasks as default)
	'''

	def __init__(self, 
			exercises: list[Exercises.Exercise] = None, 
			is_all_tasks: bool = False
	):
		if not exercises:
			exercises = []

		self.exercises = exercises
		self.is_all_tasks = is_all_tasks
		self.set_all_tasks_generation(self.is_all_tasks)


	#@Setters
	def append(self, exercise: Exercises.Exercise):
		'''Function to add exercise into this test'''
		exercise.set_all_tasks_generation(self.is_all_tasks)
		self.exercises.append(exercise)

	def add_prefix_path(self, prefix_path: str):
		'''Function to add prefix path for exercises in this test'''
		for exercise in self.exercises:
			exercise.add_prefix_path(prefix_path)

	def set_all_tasks_generation(self, is_all_tasks: bool = False):
		'''Function to set variable of generating all tasks'''
		self.is_all_tasks = is_all_tasks
		for exercise in self.exercises:
			exercise.set_all_tasks_generation(self.is_all_tasks)


	#@Getters
	def get_exercises(self):
		'''Function to get all exercises formats for this test'''
		return self.exercises


	#@Generators
	def generate_test(self) -> GeneratedTest:
		'''Function to generate test option from available exercises'''
		
		exercises = []
		
		for exercise in self.exercises:
			generated_exercise = exercise.generate_exercise()
			exercises.append(generated_exercise)

		return GeneratedTest(exercises)

