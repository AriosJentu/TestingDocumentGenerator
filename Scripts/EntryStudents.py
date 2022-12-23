from Scripts import Functions
from Scripts import Globals

from Scripts.Generators import Entries

CurrentConfiguration = Globals.CurrentConfiguration.get_configuration()

class EmptyStudents(Entries.Entries):
	'''
	EmptyStudents - class with generating struct with specific entries count 
		based on class parameter. No need to open files
	'''

	def __init__(self):
		self.group = ""

	#@Getters
	def get_group_name(self, default: str = None) -> str:
		if not default:
			default = CurrentConfiguration.EmptyStudentsSubstring.format(
				count=self.ENTRIES_COUNT,
				group=self.group
			)
		return default

	#@Generators
	def generate_information(self) -> Functions.StructList:
		'''
		Function to generate information with StudentsReader-like pattern
		'''

		structs = Functions.StructList()
		for index in range(self.ENTRIES_COUNT):
			#Append indicies for student names
			group = (
				self.group 
				if self.group != "" 
				else CurrentConfiguration.EntriesGroupName
			)
			structs.append(Functions.Struct(
				student=CurrentConfiguration.EntriesElementSubstring.format(
					value=index+1
				),
				group=group
			))

		return structs


class StudentFromValues(Entries.EntryFromValues):
	'''
	StudentsFromValues - class with using information about students 
		from struct
	Initial arguments:
	- 'element': dictionary or Struct of student format 
	'''

	#@Getters
	def get_group_name(self, default: str = None) -> str:
		if not default:
			student = self.element.student.split(" ")[0]
			default = f"{self.element.group}-{student}".replace(" ", "_")
		return default


class StudentsReader(Entries.EntriesReader):
	'''
	StudentsReader - class with reading information about students 
		in specific format
	First line of the file is Group Number (or Group Name), all next lines 
		after first are Student Names (list of students)
	Initial arguments:
	- 'filepath': Path of the students file
	'''

	#@Getters
	def get_group_name(self, default: str = None) -> str:
		return self.readlines()[0]


	#@Generators
	def generate_information(self) -> Functions.StructList:
		'''
		Function to generate information. Pattern: fist line 
			is 'group' string, all next lines are 'student' names
		'''
		lines = self.readlines()

		structs = Functions.StructList()
		for line in lines[1:]:
			if not Functions.Functions.is_empty_string(line):
				structs.append(Functions.Struct(
					student=line, 
					group=lines[0]
				))

		return structs
