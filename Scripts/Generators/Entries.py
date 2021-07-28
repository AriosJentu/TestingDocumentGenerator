from . import Functional

class Entries:
	'''
	Entries - parent class for defining custom PageInformation readers by lines. By default it read StructList, which after that will be combine with Variant object, to generate then PageInformation object.
	This class suppose that there is no file needed. Only one parameter - count of random paths.
	No initial arguments
	Parameters:
	- 'ENTRIES_COUNT': count of the entries to generate
	'''

	ENTRIES_COUNT = 10

	def __init__(self):
		pass

	def generate_information(self) -> Functional.StructList:
		'''Empty function to override. Need to work with entries count information, and generate List of Structs (StructList object). Then this element will be used in generating variant with data presented in this StructList.'''
		pass

class EntryFromValues(Entries):
	'''
	EntriesFromValues - parent class for defining custom PageInformation readers by values. By default it read StructList, which after that will be combine with Variant object, to generate then PageInformation object.
	This class suppose that there is no file needed. Just dictionary of values, or just Struct.
	Initial arguments:
	- 'element': dictionary of Struct with information about entry
	Don't need to overload method 'generate_information'
	'''

	def __init__(self, element: (dict, Functional.Struct)):
		if isinstance(element, dict):
			element = Functional.Struct(**element)
		
		self.element = element

	def generate_information(self) -> Functional.StructList:
		return Functional.StructList([self.element])

class EntriesReader(Entries):
	'''
	EntriesReader - parent class for defining custom PageInformation readers by lines. By default it read StructList, which after that will be combine with Variant object, to generate then PageInformation object.
	This class suppose to read file
	Initial arguments:
	- 'filepath': Path of the file where information will be read
	'''

	def __init__(self, filepath: str):
		self.filepath = filepath

	def read(self):
		'''Function to read file'''
		string = ""
		with open(self.filepath) as file:
			string = file.read()

		return string

	def readlines(self):
		'''Function to read lines'''
		lines = []
		with open(self.filepath) as file:
			lines = file.readlines()

		for index, line in enumerate(lines):
			lines[index] = line.replace("\n", "")

		return lines
