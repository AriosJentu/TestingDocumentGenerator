import random
import os
import os.path

class TestingException(Exception):
	NoTasks = "There is no tasks. Maybe you need to generate them with 'read_information'?"
	NoTasksSpecific = "There is no tasks. Maybe you need to generate them with 'read_information' or append some SpecificTaskInfo here?"
	NoTasksMulti = "There is no tasks. Maybe you need to generate them with 'read_information' or append some Tasks into this class?"
	NoModule = "There is no module"

class Struct:
	'''
	Struct - class with Struct format. Used for creating structure-like objects with possible to work with dictionaries
	'''

	def __init__(self, **entries):
		self.__dict__.update(entries)

	def __iter__(self):
		return iter(vars(self).values())

	def __len__(self):
		return len(vars(self).keys())

	def __getitem__(self, item):
		return self.__dict__.get(item)

	def add(self, **entries):
		for key, value in entries.items():
			self.__dict__[key] = value

	@staticmethod
	def from_struct(struct: 'Struct'):
		'''Function to generate new struct from available struct'''
		return Struct(**struct.dict())

	def dict(self):
		'''Function to get struct as dictionary values'''
		return dict(vars(self))

	def __str__(self):
		string = ", ".join([key + ": " +repr(self.__dict__.get(key)) for key in self.__dict__.keys()])
		return f"Struct({string})"

	def __repr__(self):
		return self.__str__()

class StructList:
	'''
	StructList - class which containing infromation about some list of structs
	'''
	def __init__(self, structlist: list[Struct] = None):
		#in case of 'bug' of duplicating default argument
		if structlist == None:
			structlist = []
		self.structlist = structlist

	def append(self, struct: Struct):
		'''Function to append struct into this list'''
		self.structlist.append(struct)

	def join(self, structlist: 'StructList'):
		'''Function to add another struct list into this (join two structs)'''
		self.structlist += structlist.structlist

	def __len__(self):
		return len(self.structlist)

	def __iter__(self):
		for struct in self.structlist:
			yield struct

class Functions:

	@staticmethod
	def is_empty_string(string) -> bool:
		'''Function to check is string empty or is it starts from a comment operator (% for LaTeX)'''
		return string[0] == "%" or string == "" or string == " "

	@staticmethod
	def get_unused_index(from_list: list, cache_list: list) -> int:
		'''Function to get random index from unused tasks, and this index isn't appeared in cache'''
		random.seed()
		randindex = random.randrange(len(from_list))

		#If this element in cache already, then choose another element again
		if from_list[randindex] in cache_list:
			return Functions.get_unused_index(from_list, cache_list)
		else:
			return randindex

	@staticmethod
	def remove_new_lines(string):
		'''Function to remove new lines'''
		return string.replace("\n", "")

	@staticmethod
	def crop_list_size(plist: list, size: int):
		'''Function to crop list size to fixed'''

		if len(plist) < size:
			plist = plist + [None]*(size-len(plist))

		return plist[:size]

class Path:
	'''
	Path - class to work with path
	'''
	def __init__(self, output_file: str):
		self.output_file = output_file

	def get_full_path(self):
		return self.output_file

	def add_path(self, path: str):
		'''Function to append some folders befor current output file'''
		self.output_file = os.path.join(path, self.output_file)
	
	def add_file_prefix(self, prefix: str):
		'''Function to add prefix to file'''
		head, tail = os.path.split(self.output_file)
		tail = prefix + tail
		self.output_file = os.path.join(head, tail)

	@staticmethod
	def isfile(path: str):
		return os.path.isfile(path)

	@staticmethod
	def isdir(path: str):
		return os.path.isdir(path)

	@staticmethod
	def listdir(path: str):
		return os.listdir(path)

	@staticmethod
	def list_dirs(path: str):
		return [directory for directory in os.listdir(path) if os.path.isdir(os.path.join(path, directory))]

	@staticmethod
	def join(*paths: list[str]):
		return os.path.join(*paths)

	@staticmethod
	def replace_separator(path: str, replacement: str = "."):
		return path.replace(os.sep, replacement)
