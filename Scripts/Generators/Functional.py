import random

class Struct:
	'''
	Struct - class with Struct format. Used for creating structure-like objects with possible to work with dictionaries
	'''

	def __init__(self, **entries):
		self.__dict__.update(entries)
		self.__keys__ = list(entries.keys())

	def __iter__(self):
		for i in self.__keys__:
			yield self.__dict__.get(i)

	def __len__(self):
		return len(self.__keys__)

	def __getitem__(self, item):
		if item in self.__keys__:
			return self.__dict__.get(item)
		else:
			return None

	def add(self, **entries):
		for key, value in entries.items():
			if key not in self.__keys__:
				self.__keys__.append(key)
			self.__dict__[key] = value

	@staticmethod
	def from_struct(struct: 'Struct'):
		'''Function to generate new struct from available struct'''
		return Struct(**struct.dict())

	def dict(self):
		'''Function to get struct as dictionary values'''
		return {key: self.__dict__.get(key) for key in self.__keys__}

	def __str__(self):
		string = ", ".join([key + ": " +repr(self.__dict__.get(key)) for key in self.__keys__ ])
		return f"Struct({string})"

	def __repr__(self):
		return self.__str__()

class StructList:
	'''
	StructList - class which containing infromation about some list of structs
	'''
	def __init__(self, structlist: list[Struct] = []):
		self.structlist = structlist

	def append(self, struct: Struct):
		'''Function to append struct into this list'''
		self.structlist.append(struct)

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