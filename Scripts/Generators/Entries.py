from . import Functional

class EntriesReader:
	'''
	EntriesReader - parent class for defining custom PageInformation readers by lines. By default it read StructList, which after that will be combine with Variant object, to generate then PageInformation object.
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

	def generate_information(self) -> Functional.StructList:
		'''Empty function to override. Need to work with reading information, and generate List of Structs (StructList object). Then this element will be used in generating variant with data presented in this StructList.'''
		pass

