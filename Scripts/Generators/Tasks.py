from . import Functional

class TasksException(Exception):
	pass

class Task:
	'''
	Task - class of task string. Containing only string of generated task
	Initial arguments:
	- 'task_string': String of the task text
	Available attributes:
	- 'string': Task text
	'''
	def __init__(self, task_string: str):
		self.string = task_string

	def get_task(self):
		return self.string

	def copy(self):
		return Task(self.string)

	def update_task_string(self, string):
		'''Function to update task to new string'''
		self.string = string

	def remove_new_lines(self):
		'''Function to remove new lines on the task'''
		self.string = Functional.Functions.remove_new_lines(self.string)

	def task_from_update_function(self, update_function):
		'''Function to generate new Task from current with updating it with function in terms of string. Function must contain argument of string, and must return string. This function returns a new copy of the task'''
		return Task(update_function(self.string))

	def update_task_string_with(self, update_function):
		'''Function to update task string with function in terms of string. Function must contain argument of string, and must return string. This function updates this task string'''
		self.string = update_function(self.string)

	#Classic overloading of string functions
	def __str__(self):
		return f"Task:\n\t{self.string}"

	def __repr__(self):
		result = self.string
		if len(result) > 80:
			result = result[:80]+"..."
		if result.find("\n") > 0:
			result = result[:result.find("\n")]+"..."
		return f"Task('{self.string}')"

class TasksGetter:
	'''
	TasksGetter - class to get tasks from file with caching
	Initial arguments:
	- 'filepath' - path of the file with tasks
	Available arguments:
	- 'tasks' - list of strings of tasks
	- 'cache_list' - list of integers - numbers of the tasks in 'tasks' list which already used
	- 'unused_tasks' - list of integers of the tasks which are unused at the moment 
	'''

	CACHE_SIZE = 5

	def __init__(self, filepath: str = ""):
		self.filepath = filepath

		self.tasks = []

		self.cache_list = []
		self.unused_tasks = []

	def __push_in_cache__(self, taskindex: int):
		'''Function to push tasks in cache of used tasks'''

		#If cache is full, decrease cache size. Maximal cache size must be minimal value between defined cache size, and count of tasks minus one (because if count of tasks less than cache size, it can overflow when searching tasks)
		max_cache_size = max(0, min(len(self.tasks)-1, self.CACHE_SIZE))	#Lowest border is 0, because if tasks count is 0, negative value may give all array except last item

		self.cache_list.append(taskindex)
		if len(self.cache_list) >= max_cache_size:
			#If increased size is greater than possible maxinal cache size, decreace cache size
			start = len(self.cache_list) - max_cache_size + 1
			self.cache_list = self.cache_list[start:]

	def __refresh_unused_tasks__(self):
		'''Function to refresh list of unused tasks. Must be used only when this list is empty'''
		self.unused_tasks = list(range(len(self.tasks)))

	def __get_unused_random_index__(self) -> int:
		'''Function to get random index from unused tasks, and this index isn't appeared in cache'''
		return Functional.Functions.get_unused_index(self.unused_tasks, self.cache_list)

	def update_filepath(self, filepath):
		'''Function to set new filepath of the tasks, with removing all infomration about tasks'''
		self.filepath = filepath

		self.tasks = []

		self.cache_list = []
		self.unused_tasks = []

	def read_information(self):
		'''Function to read all information about tasks. Must be callable only ones'''
		
		with open(self.filepath) as file:
			self.tasks = [
				Functional.Functions.remove_new_lines(i) 
				for i in file.readlines() 
				if not Functional.Functions.is_empty_string(i)
			]
			self.unused_tasks = list(range(len(self.tasks)))
			self.cache_list = []

	def generate_task_index(self) -> int:
		'''Function to choose random task from list of tasks. Returns index of the chosen task'''

		#Throw exception if there is no tasks (by task count)
		if len(self.tasks) == 0:
			raise TasksException("There is no tasks. Maybe you need to generate them with 'read_information'?")

		#If there is already no unused tasks, regenerate them
		if len(self.unused_tasks) == 0:
			self.__refresh_unused_tasks__()

		#Get task index in all available tasks list from unused tasks
		task_index = self.unused_tasks.pop(self.__get_unused_random_index__())
		self.__push_in_cache__(task_index)

		return task_index

	def generate_task_string(self) -> str:
		'''Function to choose random task from list of tasks. Returns string of the task'''
		task_index = self.generate_task_index()
		return self.tasks[task_index]

class Tasks(TasksGetter):
	'''
	Tasks - parent class to define all possible types of tasks, with all methods which must be presented in task generator. Based on class TasksGetter
	By default there is no initial arguments
	Available attributes:
	- 'updater': Function for updating task string on generation step. Must return string with updated task info, if replace (with method 'set_updater_function')
	'''

	def __init__(self):
		super().__init__()

		#Function to update task string (question) with some script. Must return updates string of tasks
		self.updater = lambda taskstring: taskstring

	def set_updater_function(self, updater = lambda taskstring: taskstring):
		'''Function to set updating task string function. Without arguments it reseting function to default - nothing to update'''
		self.updater = updater

	def generate_task(self) -> Task:
		'''Function to choose random task from list of tasks. Default generator overrided to generate tasks from path'''

		task = Task(self.generate_task_string())
		task.update_task_string_with(self.updater)
		return task

class BasicTasks(Tasks):
	'''
	BasicTasks - Class to work with basic tasks with choosing them from file. This kind of tasks just get one string (for example, one equation) from file of task. 
	Tasks are trying not to repeat.
	Also tasks can contain parts of replacement via some scripts. Information about it also can be passed here with specific method.
	Initial arguments:
	- 'filepath': Path (as string) of the tasks file
	'''

	def __init__(self, filepath: str):
		super().__init__()
		self.update_filepath(filepath)

class SpecificTaskInfo:
	'''
	SpecificTaskInfo - Class to work with information of specific tasks with choosing them from file. Contains file location and count of possible appearings.
	Also tasks can contain parts of replacement via some scripts. Information about it also can be passed here with specific method.
	Initial arguments:
	- 'file_path': Path (as string) of the task file
	- 'appear_count': count of possible appearings this task in all tasks in generation. -1 means it can appear every cycle. By default it's -1
	Available attributes:
	- 'filepath': Path of the task file
	- 'available_appear_count': count of possible appearings this task in all tasks in generation. -1 means it can appear every cycle. By default it's -1
	- 'fixed_appear_count': same as 'appear_count', but fixed for regeneration
	- 'updater': Function for updating task string on generation step. Must return string with updated task info, if replace (with method 'set_updater_function')
	'''

	def __init__(self, file_path: str, appear_count: int = -1):
		self.filepath = file_path
		self.available_appear_count = appear_count
		self.fixed_appear_count = appear_count

		#Update task information function
		self.updater = lambda taskstring: taskstring

	def set_updater_function(self, updater = lambda taskstring: taskstring):
		'''Function to set updating task string function. Without arguments it reseting function to default - nothing to update'''
		self.updater = updater

	def get_possible_appear_count(self) -> int:
		'''Function to get count of available appearing possibilities'''
		return self.available_appear_count

	def is_possible_to_generate(self) -> bool:
		'''Function to check possibility to use this kind of tasks'''
		return self.available_appear_count != 0

	def regenerate_possibility(self):
		'''Function to recover possibility to generate this kind of tasks'''
		self.available_appear_count = self.fixed_appear_count

	def get_task(self) -> Task:
		'''Function to get task from this filepath. Must return object of Task class'''

		if self.available_appear_count == 0:
			return None

		#Specific tasks contain all title and questions inside in combined form
		with open(self.filepath) as file:
			taskinfo = file.read()

		#Decrease appearing count, if it's not infinitely many possibilities
		if self.available_appear_count > 0:
			self.available_appear_count -= 1

		taskinfo = self.updater(taskinfo)
		return Task(taskinfo)

class SpecificTasks(Tasks):
	'''
	SpecificTasks - Class to work with specific tasks with choosing them from list of files. This kind of tasks choose one file of task from list of them. Files containing title and specific task inside. 
	Also tasks can contain parts of replacement via some scripts. Information about it also can be passed here with specific method. And tasks may appears only for some times.
	Initial arguments:
	- 'list_tasks': List of specific tasks informations (as objects of SpecificTaskInfo class)
	Available attributes:
	- 'tasks': List of specific tasks informations
	- 'unused_tasks': Numbers of tasks in all_tasks list
	'''

	def __init__(self, tasks_list: list[SpecificTaskInfo] = None):
		if tasks_list == None:
			tasks_list = []

		super().__init__()
		self.all_tasks = tasks_list

	def append(self, taskinfo: SpecificTaskInfo):
		'''Special method for this class - it's possible to append paths of tasks into this class of tasks'''
		self.all_tasks.append(taskinfo)

	def read_information(self):
		self.tasks = list(range(len(self.all_tasks)))
		self.unused_tasks = list(range(len(self.all_tasks)))
		self.cache_list = []

	def __refresh_possibilities__(self):
		'''Function to refresh possibility to use tasks with fixed count of appearing again. Must be used only when there is no available tasks for generate'''
		for task in self.all_tasks:
			task.regenerate_possibility()

		self.tasks = list(range(len(self.all_tasks)))

	def __refresh_unused_tasks__(self):
		'''Function to refresh list of unused tasks. Must be used only when this list is empty'''
		self.unused_tasks = self.tasks.copy()

	def generate_task(self) -> Task:
		'''Function to choose random task from list of tasks. Must return object of Task class'''

		#Throw exception if there is no tasks (by task count)
		if len(self.all_tasks) == 0:
			raise TasksException("There is no tasks. Maybe you need to generate them with 'read_information' or append some SpecificTaskInfo here?")
		
		#If there is no possibility to generate task, refresh all tasks possibilities
		if len(self.tasks) == 0:
			self.__refresh_possibilities__()

		task_index = self.generate_task_index()

		#Get task which updates from it's updater function
		task = self.all_tasks[task_index].get_task()

		#If there is no possibilities to use this task anymore, remove it from available 
		if not self.all_tasks[task_index].is_possible_to_generate():
			self.tasks.pop(self.tasks.index(task_index))

		#Return task string
		return task

class MultiTasks(Tasks):
	'''
	MultiTasks - Class to work with tasks which containing a list of files of Basic Tasks. This kind of tasks choose one file of task from lists from tasks files randomly. 
	Also tasks can contain parts of replacement via some scripts. Information about it also can be passed here with specific method. And tasks may appears only for some times.
	Initial arguments:
	- 'list_tasks': List of tasks (as objects of Tasks class)
	'''

	def __init__(self, list_basic_tasks: list[Tasks] = None):
		if list_tasks == None:
			list_tasks = []

		super().__init__()
		self.list_tasks = list_tasks

	def append(self, basic_tasks: Tasks):
		'''Special method for this class - it's possible to append basic tasks into this class of tasks'''
		self.list_tasks.append(basic_tasks)

	def read_information(self):
		self.tasks = list(range(len(self.list_tasks)))
		self.unused_tasks = list(range(len(self.list_tasks)))
		self.cache_list = []
		
		for basictasks in self.list_tasks:
			basictasks.read_information()

	def generate_task(self) -> Task:
		'''Function to choose random task from list of tasks. Must return object of Task class'''

		#Throw exception if there is no tasks (by task count)
		if len(self.list_tasks) == 0:
			raise TasksException("There is no tasks. Maybe you need to generate them with 'read_information' or append some Tasks into this class?")

		tasks_index = self.generate_task_index()

		return self.list_tasks[tasks_index].generate_task()

class TasksInformation:
	'''
	TasksInformation - Class to work with tasks information. Containing object of Tasks class with it's repeating count.
	Initial arguments:
	- 'tasks': Tasks object (as objects of Tasks class and it's subclasses)
	- 'repeating': Count of repeating tasks of this type in question
	'''

	def __init__(self, tasks: Tasks, repeating: int = 1):
		self.tasks = tasks
		self.repeating = max(1, int(repeating))

	def get_tasks(self):
		'''Function to get list of all tasks in this information object'''
		return self.tasks

	def generate_tasks(self) -> list[Task]:
		'''Function to generate list of tasks for this 'Tasks' class. Returns list of objects of Task class'''

		tasks = []
		for _ in range(self.repeating):
			tasks.append(self.tasks.generate_task())

		return tasks

	def __str__(self):
		return f"TasksInformation:\nR - {self.repeating}: {self.tasks}"

	def __repr__(self):
		return f"TasksInformation({self.repeating}, {self.tasks})"

