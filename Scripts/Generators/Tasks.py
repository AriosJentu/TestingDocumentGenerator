import random
from . import Functions

class TasksException(Exception):
	pass

class Tasks:
	'''
	Tasks - parent class to define all possible types of tasks, with all methods which must be presented in task generator
	By default there is no initial arguments
	Available attributes:
	- 'tasks_count': Available tasks count
	- 'cache_used': List of cached tasks. For child classes also method '__push_in_cache__' can be replaced
	- 'updater': Function for updating task string on generation step. Must return string with updated task info, if replace (with method 'set_updater_function')
	'''
	CACHE_SIZE = 5	#Maximal cache size, after this iterations when unused tasks regenerates, they will not be the same

	def __init__(self):

		self.tasks_count = 0	#Count of tasks
		self.cache_used = []	#Cached tasks for not repeating after regeneration (like queue)
		
		#For scripts
		self.updater = self.__update_task__

	def __update_task__(self, taskstring: str) -> str:
		'''Function to update task string (question) with some script. Must return updates string of tasks'''
		return taskstring

	def __push_in_cache__(self, taskindex: int):
		'''Function to push tasks in cache of used tasks'''

		#If cache is full, decrease cache size. Maximal cache size must be minimal value between defined cache size, and count of tasks minus one (because if count of tasks less than cache size, it can overflow when searching tasks)
		max_cache_size = max(0, min(self.tasks_count-1, self.CACHE_SIZE))	#Lowest border is 0, because if tasks count is 0, negative value may give all array except last item
		if len(self.cache_used) > max_cache_size:
			self.cache_used = self.cache_used[:max_cache_size]

		if len(self.cache_used) == max_cache_size:
			self.cache_used = self.cache_used[1:]

		self.cache_used.append(taskindex)

	def set_updater_function(self, updater = lambda taskstring: taskstring):
		'''Function to set updating task string function. Without arguments it reseting function to default - nothing to update'''
		self.updater = updater

	def read_information(self):
		'''Function to read all information about tasks. Must be callable only ones'''
		return

	def generate_task(self):
		'''Function to choose random task from list of tasks'''
		return

class BasicTasks(Tasks):
	'''
	BasicTasks - Class to work with basic tasks with choosing them from file. This kind of tasks just get one string (for example, one equation) from file of task. 
	Tasks are trying not to repeat.
	Also tasks can contain parts of replacement via some scripts. Information about it also can be passed here with specific method.
	Initial arguments:
	- 'file_path': Path (as string) of the tasks file
	Available attributes:
	- 'filepath': Path of the tasks file
	- 'all_tasks': Strings of task equations
	- 'unused_tasks': Numbers of tasks in all_tasks list
	'''

	def __init__(self, file_path: str):

		super().__init__()
		self.filepath = file_path

		#For generating
		self.all_tasks = []		#Strings of task equations
		self.unused_tasks = []	#Numbers of tasks in all_tasks list

	def read_information(self):
		'''Function to save all information about tasks. Must be callable only ones'''
		
		with open(self.filepath) as file:
			#Read tasks with non-comment lines, and only if them non-empty
			self.all_tasks = [i for i in file.readlines() if not Functions.Functions.is_empty_string(i)]
			self.tasks_count  = len(self.all_tasks)
			self.unused_tasks = list(range(self.tasks_count))
			self.cache_used = []

	def __refresh_unused_tasks__(self):
		'''Function to refresh list of unused tasks. Must be used only when this list is empty'''
		self.unused_tasks = list(range(self.tasks_count))

	def __get_unused_random_index__(self):
		'''Function to gen random index from unused tasks, and this index isn't appeared in cache'''
		randindex = random.randrange(len(self.unused_tasks))

		#If this task in cache already, then choose task again
		if self.unused_tasks[randindex] in self.cache_used:
			return self.__get_unused_random_index__()
		else:
			return randindex

	def generate_task(self):
		'''Function to choose random task from list of tasks'''

		#Throw exception if there is no tasks (by task count)
		if self.tasks_count == 0:
			raise TasksException("There is no tasks. Maybe you need to generate them with 'read_information'?")

		#If there is already no unused tasks, regenerate them
		if len(self.unused_tasks) == 0:
			self.__refresh_unused_tasks__()

		#Get task index in all available tasks list from unused tasks
		task_index = self.unused_tasks.pop(self.__get_unused_random_index__())
		self.__push_in_cache__(task_index)

		#Update task string from updater function
		task = self.updater(self.all_tasks[task_index])

		#Remove \n from task
		task = task.replace("\n", "")

		#Return task string
		return task


class SpecificTaskInfo:
	'''
	SpecificTaskInfo - Class to work with information of specific tasks with choosing them from file. Contains file location and count of possible appearings.
	Also tasks can contain parts of replacement via some scripts. Information about it also can be passed here with specific method.
	Initial arguments:
	- 'file_path': Path (as string) of the task file
	- 'appear_count': count of possible appearings this task in all tasks in generation. -1 means it can appear every cycle. By default it's -1
	Available attributes:
	- 'filepath': Path of the task file
	- 'appear_count': count of possible appearings this task in all tasks in generation. -1 means it can appear every cycle. By default it's -1
	- 'fixed_appear_count': same as 'appear_count', but fixed for regeneration
	- 'updater': Function for updating task string on generation step. Must return string with updated task info, if replace (with method 'set_updater_function')
	'''

	def __init__(self, file_path: str, appear_count: int = -1):
		self.filepath = file_path
		self.appear_count = appear_count
		self.fixed_appear_count = appear_count

		#Update task information function
		self.updater = lambda taskstring: taskstring

	def set_updater_function(self, updater = lambda taskstring: taskstring):
		'''Function to set updating task string function. Without arguments it reseting function to default - nothing to update'''
		self.updater = updater

	def is_possible_to_generate(self):
		'''Function to check possibility to use this kind of tasks'''
		return self.appear_count != 0

	def regenerate_possibility(self):
		'''Function to recover possibility to generate this kind of tasks'''
		self.appear_count = self.fixed_appear_count

	def get_task(self):
		'''Function to get task from this filepath'''

		if self.appear_count == 0:
			return None

		#Specific tasks contain all title and questions inside in combined form
		with open(self.filepath) as file:
			taskinfo = file.read()

		#Decrease appearing count, if it's not infinitely many possibilities
		if self.appear_count > 0:
			self.appear_count -= 1

		taskinfo = self.updater(taskinfo)
		return taskinfo

class SpecificTasks(Tasks):
	'''
	SpecificTasks - Class to work with specific tasks with choosing them from list of files. This kind of tasks choose one file of task from list of them. Files containing title and specific task inside. 
	Also tasks can contain parts of replacement via some scripts. Information about it also can be passed here with specific method. And tasks may appears only for some times.
	Initial args:
	- 'list_tasks': List of specific tasks informations (as objects of SpecificTaskInfo class)
	Available attributes:
	- 'tasks': List of specific tasks informations
	- 'unused_tasks': Numbers of tasks in all_tasks list
	'''

	def __init__(self, list_tasks: list[SpecificTaskInfo]):

		super().__init__()
		self.tasks = list_tasks
		self.available_tasks = []
		self.unused_tasks = []

	def read_information(self):
		'''Function to read all information about tasks. Must be callable only ones'''
		self.tasks_count = len(self.tasks)
		self.available_tasks = list(range(self.tasks_count))
		self.unused_tasks = list(range(self.tasks_count))

	def __refresh_possibilities__(self):
		'''Function to refresh possibility to use tasks with fixed count of appearing again. Must be used only when there is no available tasks for generate'''
		for task in self.tasks:
			task.regenerate_possibility()

		self.available_tasks = list(range(self.tasks_count))

	def __refresh_unused_tasks__(self):
		'''Function to refresh list of unused tasks. Must be used only when this list is empty'''
		if len(self.available_tasks) == 0:
			self.__refresh_possibilities__()

		self.unused_tasks = self.available_tasks.copy()

	def __get_unused_random_index__(self):
		'''Function to gen random index from unused tasks, and this index isn't appeared in cache'''

		randindex = random.randrange(len(self.unused_tasks))

		#If this task in cache already, then choose task again
		if self.unused_tasks[randindex] in self.cache_used:
			return self.__get_unused_random_index__()
		else:
			return randindex

	def __push_in_cache__(self, taskindex: int):
		'''Function to push tasks in cache of used tasks'''

		#If cache is full, decrease cache size. Maximal cache size must be minimal value between defined cache size, and count of tasks minus one (because if count of tasks less than cache size, it can overflow when searching tasks)
		max_cache_size = max(0, min(len(self.available_tasks)-1, self.CACHE_SIZE))	#Lowest border is 0, because if tasks count is 0, negative value may give all array except last item
		if len(self.cache_used) > max_cache_size:
			self.cache_used = self.cache_used[:max_cache_size]

		if len(self.cache_used) == max_cache_size:
			self.cache_used = self.cache_used[1:]

		self.cache_used.append(taskindex)
		
	def generate_task(self):
		'''Function to choose random task from list of tasks'''

		#Throw exception if there is no tasks (by task count)
		if self.tasks_count == 0:
			raise TasksException("There is no tasks. Maybe you need to generate them with 'read_information'?")
		
		#If there is already no unused tasks, regenerate them
		if len(self.unused_tasks) == 0:
			self.__refresh_unused_tasks__()

		task_index = self.unused_tasks.pop(self.__get_unused_random_index__())
		self.__push_in_cache__(task_index)

		#Update task string from updater function
		task = self.tasks[task_index].get_task()

		#If there is no possibilities to use this task anymore, remove it from available 
		if not self.tasks[task_index].is_possible_to_generate():
			self.available_tasks.pop(self.available_tasks.index(task_index))

		#Return task string
		return task

		


