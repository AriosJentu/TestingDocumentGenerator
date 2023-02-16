import random

from Scripts.Generators import Tasks

class GeneratedExercise:
	'''
	GeneratedExercise - class with generated tasks and updated title 
		for the exercise
	Inital arguments:
	- 'tasks': List of tasks (objects of 'Task' class)
	- 'title': Title of the exercise
	- 'exercise_format': Format string for exercise if it needs
	Available attributes:
	- 'tasks': List of tasks (objects of 'Task' class)
	- 'title': Title of the exercise
	'''

	def __init__(self, 
			tasks: list[Tasks.Task], 
			title: str, 
			exercise_format: str = None
	):
		self.tasks = tasks
		self.title = title
		self.exercise_format = exercise_format


	#@Setters
	def shuffle_tasks(self):
		'''Function to shuffle tasks'''
		random.seed()
		random.shuffle(self.tasks)


	#@Getters
	def get_title(self) -> str:
		'''Function to get ecxercise title'''
		return self.title

	def get_tasks(self) -> list[Tasks.Task]:
		'''Function to get ecxercise tasks'''
		return self.tasks

	def get_exercise_format(self) -> [str, None]:
		'''Function to get exercise format'''
		return self.exercise_format


	#@Override
	def __iter__(self):
		'''Iterate this class with tasks'''
		for task in self.tasks:
			yield task

	def __str__(self):
		'''Return exercise title as string of this class'''
		return self.title

	def __repr__(self):
		return f"GeneratedExercise('{self.title}')"


class Exercise:
	'''
	Exercise - class for working with exercises of the document. 
		Containing list of tasks for the exercise and title of the question. 
		Tasks can be mix in different order.
	Initial arguments:
	- 'tasks_info_list': List of the tasks information 
		(list of objects of class 'TasksInformation')
	- 'title': Title string of the exercise. Can be empty in case of 
		specific tasks, for example
	- 'shuffle': Shuffle generated tasks for this exercise
	- 'is_all_tasks': Key for creating all available tasks in files 
		(for debug, if True - generate ALL tasks from files, 
		by default it's False - generate tasks as default)
	- 'exercise_format': String with format exercise's page style layout 
		(Contains '{title}' and '{tasks}' substrings, 
		if this value is 'None', it generates exercise format by default 
		with PageStyle class)
	Available attributes:
	- 'tasks_info_list': List of the tasks information
	- 'title': Title string of the exercise
	- 'updater': Function which updates titles of the exercise. 
		It's argument is 'title' of the exercise, and function 
		must return string with updated text
	'''
	def __init__(self, 
			tasks_info_list: list[Tasks.TasksInformation] = None, 
			title: str = "",
			shuffle: bool = False,
			is_all_tasks: bool = False,
			exercise_format: str = None,
	):
		if not tasks_info_list:
			tasks_info_list = []

		self.tasks_info_list = tasks_info_list
		self.title = title
		self.shuffle = shuffle
		self.is_all_tasks = is_all_tasks
		self.exercise_format = exercise_format
		self.set_all_tasks_generation(self.is_all_tasks)

		#Updating title string function
		self.updater = lambda titlestring: titlestring


	#@Setters
	def append(self, tasks_info: Tasks.TasksInformation):
		'''Function to append task information into exercise'''
		tasks_info.set_all_tasks_generation(self.is_all_tasks)
		self.tasks_info_list.append(tasks_info)

	def add_prefix_path(self, prefix_path: str):
		'''Function to add prefix path for tasks in this exercise'''
		for tasksinfo in self.tasks_info_list:
			tasksinfo.add_prefix_path(prefix_path)

	def set_all_tasks_generation(self, is_all_tasks: bool = False):
		'''Function to set variable of generating all tasks'''
		self.is_all_tasks = is_all_tasks

		#Set all tasks generation for tasks information
		for tasks_info in self.tasks_info_list:
			tasks_info.set_all_tasks_generation(self.is_all_tasks)

	def set_exercise_format(self, exercise_format: str = None):
		'''Function to set exercise's format string'''
		self.exercise_format = exercise_format

	def set_title_updater_function(self, 
			updater = lambda titlestring: titlestring
	):
		'''
		Function to set updating exercise title string function. 
		Without arguments it reseting function to default - nothing to update
		'''
		self.updater = updater

	def set_shuffle_state(self, shuffle: bool = False):
		'''Function to set exercises shuffled when generate'''
		self.shuffle = shuffle


	#@Getters
	def get_tasks_information_list(self) -> list:
		'''Function to get tasks information list'''
		return self.tasks_info_list

	def get_exercise_format(self) -> [str, None]:
		'''Function to get exercise's format string'''
		return self.exercise_format


	#@Generators
	def generate_exercise(self) -> GeneratedExercise:
		'''
		Function to generate list of tasks for this exercise. 
		Also this function updating title of the exercise. 
		Returns object of 'GeneratedExercise' class
		'''

		tasks = []
		for tasks_info in self.tasks_info_list:
			#Add to the current tasks list a list of generated tasks
			tasks += tasks_info.generate_tasks()

		#Update title of the exercise
		title = self.updater(self.title)

		generated = GeneratedExercise(tasks, title, self.exercise_format)

		#Shuffle tasks if it's available to shuffle, 
		# and tasks generating as exercise (not debug all tasks)
		if self.shuffle and not self.is_all_tasks:
			generated.shuffle_tasks()

		return generated

