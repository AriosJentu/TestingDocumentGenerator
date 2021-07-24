import random
from . import Tasks

class GeneratedExcercise:
	'''
	GeneratedExcercise - class with generated tasks and updated title for the excercise
	Inital arguments:
	- 'tasks': List of tasks (objects of 'Task' class)
	- 'title': Title of the excercise
	Available attributes:
	- 'tasks': List of tasks (objects of 'Task' class)
	- 'title': Title of the excercise
	'''

	def __init__(self, tasks: list[Tasks.Task], title: str):
		self.tasks = tasks
		self.title = title

	def shuffle_tasks(self):
		'''Function to shuffle tasks'''
		random.seed()
		random.shuffle(self.tasks)

	def get_title(self) -> str:
		'''Function to get ecxercise title'''
		return self.title

	def get_tasks(self) -> list[Tasks.Task]:
		'''Function to get ecxercise tasks'''
		return self.tasks

	def __iter__(self):
		'''Iterate this class with tasks'''
		for task in self.tasks:
			yield task

	def __str__(self):
		'''Return excercise title as string of this class'''
		return self.title

	def __repr__(self):
		return f"GeneratedExcercise('{self.title}')"


class Excercise:
	'''
	Excercise - class for working with excercises of the document. Containing list of tasks for the excercise and title of the question. Tasks can be mix in different order.
	Initial arguments:
	- 'tasks_info_list': List of the tasks information (list of objects of class 'TasksInformation')
	- 'title': Title string of the excercise. Can be empty in case of specific tasks, for example
	- 'shuffle': Shuffle generated tasks for this excercise
	Available attributes:
	- 'tasks_info_list': List of the tasks information
	- 'title': Title string of the excercise
	- 'updater': Function which updates titles of the excercise. It's argument is 'title' of the excercise, and function must return string with updated text
	'''
	def __init__(self, 
			tasks_info_list: list[Tasks.TasksInformation] = None, 
			title: str = "",
			shuffle: bool = False
	):
		if not tasks_info_list:
			tasks_info_list = []

		self.tasks_info_list = tasks_info_list
		self.title = title
		self.shuffle = shuffle

		#Updating title string function
		self.updater = lambda titlestring: titlestring

	def append(self, tasks_info: Tasks.TasksInformation):
		'''Function to append task information into excercise'''
		self.tasks_info_list.append(tasks_info)

	def get_tasks_information_list(self):
		'''Function to get tasks information list'''
		return self.tasks_info_list

	def set_title_updater_function(self, updater = lambda titlestring: titlestring):
		'''Function to set updating excercise title string function. Without arguments it reseting function to default - nothing to update'''
		self.updater = updater

	def set_shuffle_state(self, shuffle: bool = False):
		'''Function to set excercises shuffled when generate'''
		self.shuffle = shuffle

	def generate_tasks(self) -> GeneratedExcercise:
		'''Function to generate list of tasks for this excercise. Also this function updating title of the excercise. Returns object of 'GeneratedExcercise' class'''

		tasks = []
		for tasks_info in self.tasks_info_list:
			#Add to the current tasks list a list of generated tasks
			tasks += tasks_info.generate_tasks()

		#Update title of the excercise
		title = self.updater(self.title)

		generated = GeneratedExcercise(tasks, title)
		if self.shuffle:
			generated.shuffle_tasks()

		return generated
